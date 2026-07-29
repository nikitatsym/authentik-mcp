"""End-to-end tests against a dockerized Authentik.

Skipped unless AUTHENTIK_URL/AUTHENTIK_TOKEN are set (see conftest). Bring the
stack up with `uv run python scripts/bootstrap.py`, then `uv run pytest -m integration`.

The marquee test is `test_group_application_binding_gate`: it proves the v2.5
fix — a group→application access gate is one PolicyBinding with `group` set and
no `policy`, created straight through the MCP (no blueprint, policy not required).
"""

from __future__ import annotations

import uuid

import pytest

from authentik_mcp.client import APIError

pytestmark = pytest.mark.integration


def _uniq(prefix: str) -> str:
    return f"{prefix}-mcp-test-{uuid.uuid4().hex[:8]}"


def test_version(configure_env):
    """ROOT op: returns the MCP package version and the live service version."""
    from authentik_mcp.tools.version import authentik_version

    info = authentik_version()
    assert info["mcp"]
    assert isinstance(info["service"], dict)
    # The dockerized server answers /admin/version/, so we get a version string.
    assert info["service"].get("version_current") or info["service"].get("status")


def test_list_users_has_akadmin(agent):
    users = agent.call("list_users")
    assert isinstance(users, list)
    assert any(u.get("username") == "akadmin" for u in users), \
        f"akadmin not found among {[u.get('username') for u in users]}"


def test_user_crud(agent):
    username = _uniq("user")
    # Minimal args — the op defaults the `groups` field Authentik requires.
    created = agent.call("create_user", username=username, name="MCP Test User")
    uid = created["pk"]
    try:
        found = agent.call("list_users", search=username)
        assert any(u["pk"] == uid for u in found)
    finally:
        agent.call("delete_user", id=uid)
    # Gone after delete.
    assert not any(u["pk"] == uid for u in agent.call("list_users", search=username))


def test_group_application_binding_gate(agent):
    """Group → application access gate via one PolicyBinding, no policy/blueprint."""
    # Minimal args — the op defaults the users/parent fields Authentik requires.
    group = agent.call("create_group", name=_uniq("grp"))
    group_pk = group["pk"]
    app_slug = _uniq("app")
    app = agent.call("create_application", name=app_slug, slug=app_slug)
    app_pk = app["pk"]
    binding_pk = None
    try:
        # The whole point: bind a GROUP to the application with NO policy.
        # `negate` rides through **kwargs, exercising the v2.5 passthrough.
        binding = agent.call(
            "create_policy_binding", target=app_pk, group=group_pk, order=0, negate=True
        )
        binding_pk = binding["pk"]
        assert binding["group"] == group_pk
        assert binding["policy"] is None, \
            f"expected null policy on a group binding, got {binding['policy']!r}"
        assert binding["target"] == app_pk
        assert binding["negate"] is True  # kwargs reached the API

        # Readable back through show + list.
        shown = agent.call("show_policy_binding", id=binding_pk)
        assert shown["group"] == group_pk and shown["policy"] is None

        listed = agent.call("list_policy_bindings", limit=100)
        assert any(b["pk"] == binding_pk for b in listed)

        # update_policy_binding does read-modify-write via PUT (Authentik 405s
        # PATCH on bindings). A partial change preserves the bound subject.
        updated = agent.call("update_policy_binding", id=binding_pk, enabled=False)
        assert updated["enabled"] is False
        assert updated["group"] == group_pk  # subject preserved through update
    finally:
        if binding_pk:
            agent.call("delete_policy_binding", id=binding_pk)
        agent.call("delete_application", slug=app_slug)
        agent.call("delete_group", id=group_pk)


def test_create_policy_binding_validation(agent):
    """Missing required `target` is a Pydantic ValueError before any HTTP call."""
    with pytest.raises(ValueError) as exc:
        agent.call("create_policy_binding", order=0, group="whatever")
    assert "target" in str(exc.value)


def test_unknown_key_rejected(agent):
    """A non-**kwargs op rejects unknown keys (extra='forbid')."""
    with pytest.raises(ValueError) as exc:
        agent.call("show_application", slug="default", bogus="x")
    assert "bogus" in str(exc.value).lower() or "extra" in str(exc.value).lower()


def test_http_error_surfaces_as_apierror(agent):
    """A 404 from the API propagates as APIError, not a swallowed dict."""
    with pytest.raises(APIError):
        agent.call("show_application", slug=_uniq("does-not-exist"))


# ── Broad read smoke across resource types ─────────────────────────────

# One list op per major domain. Catches broken endpoints / slim crashes
# across the surface that the focused tests above never touch.
READ_SMOKE_OPS = [
    "list_providers", "list_flows", "list_stages", "list_sources",
    "list_policies", "list_certificates", "list_outposts", "list_events",
    "list_tokens", "list_brands", "list_property_mappings",
]


@pytest.mark.parametrize("op", READ_SMOKE_OPS)
def test_read_smoke(agent, op):
    """Every major list endpoint responds with a list of dict items."""
    result = agent.call(op)
    assert isinstance(result, list), f"{op} returned {type(result).__name__}, not a list"
    for item in result[:5]:
        assert isinstance(item, dict)


def test_list_is_slimmed(agent):
    """List views return only the slim field set, not full objects."""
    from authentik_mcp.tools.helpers import SLIM_USER

    users = agent.call("list_users", limit=5)
    assert users, "expected at least akadmin"
    for u in users:
        extra = set(u) - SLIM_USER
        assert not extra, f"list_users leaked non-slim fields: {extra}"


# ── Realistic scenario: OAuth2 provider → application → group gate ─────


def test_provider_application_group_gate(agent):
    """A real app fronts an OAuth2 provider and is gated to a group."""
    flows = agent.call("list_flows", limit=100)
    authz = next(f for f in flows if f["designation"] == "authorization")
    # Newer Authentik also requires an invalidation flow; pass it for portability.
    inval = next((f for f in flows if f["designation"] == "invalidation"), None)
    extra = {"invalidation_flow": inval["pk"]} if inval else {}
    provider = agent.call(
        "create_oauth2_provider", name=_uniq("oauth"),
        authorization_flow=authz["pk"], redirect_uris=[], **extra,
    )
    prov_pk = provider["pk"]
    group = agent.call("create_group", name=_uniq("grp"))
    slug = _uniq("app")
    app = None
    binding_pk = None
    try:
        app = agent.call("create_application", name=slug, slug=slug, provider=prov_pk)
        assert app["provider"] == prov_pk
        binding = agent.call(
            "create_policy_binding", target=app["pk"], group=group["pk"], order=0
        )
        binding_pk = binding["pk"]
        assert binding["group"] == group["pk"] and binding["policy"] is None
        # Reachable by slug and still bound to the provider.
        assert agent.call("show_application", slug=slug)["provider"] == prov_pk
    finally:
        if binding_pk:
            agent.call("delete_policy_binding", id=binding_pk)
        if app:
            agent.call("delete_application", slug=slug)
        agent.call("delete_group", id=group["pk"])
        agent.call("delete_oauth2_provider", id=prov_pk)


# ── Meta-tool boundary (the client-facing MCPServer surface) ───────────


def _meta_tools() -> dict:
    """The registered MCPServer meta-tool callables, keyed by group name."""
    from authentik_mcp.server import mcp

    return {t.name: t.fn for t in mcp._tool_manager._tools.values()}


def test_meta_tool_help_schema_dispatch(agent):
    """help / schema / dispatch all work through the registered meta-tool."""
    read = _meta_tools()["authentik_read"]

    help_text = read(operation="help")
    assert "ListUsers" in help_text
    assert "operation='schema'" in help_text

    filtered = read(operation="help", params={"search": "listusers"})
    assert "ListUsers" in filtered

    schema = read(operation="schema", params={"op": "ListUsers"})
    assert isinstance(schema, dict) and "properties" in schema

    listed = read(operation="ListUsers", params={"limit": 5})
    assert isinstance(listed, list)


def test_meta_tool_unknown_op_errors(agent):
    """An unknown operation raises (not a swallowed error dict)."""
    read = _meta_tools()["authentik_read"]
    with pytest.raises(ValueError):
        read(operation="NotARealOp", params={})
