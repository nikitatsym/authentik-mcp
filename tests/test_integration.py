"""End-to-end tests against a dockerized Authentik.

Skipped unless AUTHENTIK_URL/AUTHENTIK_TOKEN are set (see conftest). Bring the
stack up with `uv run python scripts/bootstrap.py`, then `uv run pytest -m integration`.

The marquee test is `test_group_application_binding_gate`: it proves the v2.5
fix — a group→application access gate is one PolicyBinding with `group` set and
no `policy`, created straight through the MCP (no blueprint, policy not required).
"""

from __future__ import annotations

import json
import time
import uuid

import httpx
import pytest
from mcp.types import TextContent

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
    group = agent.call("create_group", name=_uniq("grp"))
    group_pk = group["pk"]
    app_slug = _uniq("app")
    app = agent.call("create_application", name=app_slug, slug=app_slug)
    app_pk = app["pk"]
    binding_pk = None
    try:
        # The whole point: bind a GROUP to the application with NO policy.
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
        shown = agent.call("show_policy_binding", policy_binding_uuid=binding_pk)
        assert shown["group"] == group_pk and shown["policy"] is None

        listed = agent.call("list_policy_bindings", limit=100)
        assert any(b["pk"] == binding_pk for b in listed)

        updated = agent.call("update_policy_binding", policy_binding_uuid=binding_pk, enabled=False)
        assert updated["enabled"] is False
        assert updated["group"] == group_pk  # subject preserved through update
    finally:
        if binding_pk:
            agent.call("delete_policy_binding", policy_binding_uuid=binding_pk)
        agent.call("delete_application", slug=app_slug)
        agent.call("delete_group", group_uuid=group_pk)


def test_create_policy_binding_validation(agent):
    """Missing required `target` returns a Pydantic validation result before HTTP."""
    result = agent.call("create_policy_binding", order=0, group="whatever")
    assert "target" in result["error"]


def test_unknown_key_rejected(agent):
    """A non-**kwargs op returns a validation result for unknown keys."""
    result = agent.call("show_application", slug="default", bogus="x")
    assert "bogus" in result["error"].lower() or "extra" in result["error"].lower()


def test_http_error_returns_context(agent):
    """A 404 from the API is returned with its contextual API error."""
    result = agent.call("show_application", slug=_uniq("does-not-exist"))
    assert "404" in result["error"]


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
    inval = next(f for f in flows if f["designation"] == "invalidation")
    provider = agent.call(
        "create_oauth2_provider", name=_uniq("oauth"),
        authorization_flow=authz["pk"], invalidation_flow=inval["pk"], redirect_uris=[],
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
            agent.call("delete_policy_binding", policy_binding_uuid=binding_pk)
        if app:
            agent.call("delete_application", slug=slug)
        agent.call("delete_group", group_uuid=group["pk"])
        agent.call("delete_oauth2_provider", id=prov_pk)


# ── Meta-tool boundary (the client-facing MCPServer surface) ───────────


def _meta_tools() -> dict:
    """The registered MCPServer meta-tool callables, keyed by group name."""
    from authentik_mcp.server import mcp

    return {t.name: t.fn for t in mcp._tool_manager._tools.values()}


def _data(result):
    """Registered tools hand the SDK a one-line JSON text block, not a dict."""
    assert isinstance(result, TextContent)
    return json.loads(result.text)


def test_meta_tool_help_schema_dispatch(agent):
    """help / schema / dispatch all work through the registered meta-tool."""
    read = _meta_tools()["authentik_read"]

    help_text = read(operation="help")
    assert "ListUsers" in help_text
    assert "operation='schema'" in help_text

    filtered = read(operation="help", params={"search": "listusers"})
    assert "ListUsers" in filtered

    schema = _data(read(operation="schema", params={"op": "ListUsers"}))
    assert isinstance(schema, dict) and "properties" in schema

    listed = _data(read(operation="ListUsers", params={"limit": 5}))
    assert isinstance(listed, list)


def test_meta_tool_unknown_op_errors(agent):
    """An unknown operation returns an actionable validation result."""
    read = _meta_tools()["authentik_read"]
    result = _data(read(operation="NotARealOp", params={}))
    assert "Unknown operation" in result["error"]


def test_application_icon_patch_keeps_and_clears_value(agent):
    slug = _uniq("icon")
    app = agent.call("create_application", name=slug, slug=slug)
    assert app["slug"] == slug
    try:
        icon = "https://example.com/mcp-icon.svg"
        updated = agent.call("update_application", slug=slug, meta_icon=icon)
        assert updated["meta_icon"] == icon
        assert agent.call("show_application", slug=slug)["meta_icon"] == icon
        cleared = agent.call("update_application", slug=slug, meta_icon="")
        assert cleared["meta_icon"] == ""
        assert agent.call("show_application", slug=slug)["meta_icon"] == ""
    finally:
        agent.call("delete_application", slug=slug)


def test_group_parents_and_binding_null_semantics(agent):
    parent = agent.call("create_group", name=_uniq("parent"))
    child = agent.call("create_group", name=_uniq("child"), parents=[parent["pk"]])
    slug = _uniq("nullable")
    app = agent.call("create_application", name=slug, slug=slug)
    binding = None
    try:
        assert child["parents"] == [parent["pk"]]
        binding = agent.call("create_policy_binding", target=app["pk"], group=child["pk"], order=0)
        updated = agent.call("update_policy_binding", policy_binding_uuid=binding["pk"], enabled=False)
        assert updated["group"] == child["pk"]
        users = agent.call("list_users", search="akadmin")
        uid = next(user["pk"] for user in users if user["username"] == "akadmin")
        changed = agent.call("update_policy_binding", policy_binding_uuid=binding["pk"], group=None, user=uid)
        assert changed["group"] is None and changed["user"] == uid
    finally:
        if binding:
            agent.call("delete_policy_binding", policy_binding_uuid=binding["pk"])
        agent.call("delete_application", slug=slug)
        agent.call("delete_group", group_uuid=child["pk"])
        agent.call("delete_group", group_uuid=parent["pk"])


def test_flow_export_import_blueprint_roundtrip(agent, tmp_path):
    slug = _uniq("roundtrip")
    flow = agent.call("create_flow", name=slug, slug=slug, title="MCP round trip", designation="authentication")
    assert flow["slug"] == slug
    try:
        exported = agent.call("export_flow", slug=slug)
        assert isinstance(exported, str)
        file = tmp_path / "flow.yaml"
        file.write_text(exported)
        agent.call("delete_flow", slug=slug)
        imported = agent.call("import_blueprint", file=str(file))
        assert imported["success"] is True, imported
        restored = agent.call("show_flow", slug=slug)
        assert restored["name"] == slug and restored["title"] == "MCP round trip"
    finally:
        agent.call("delete_flow", slug=slug)


def test_send_recovery_email_delivers_link(agent):
    username = _uniq("recovery")
    address = username + "@test.local"
    user = agent.call("create_user", username=username, name="MCP recovery", email=address)
    stage = agent.call(
        "create_email_stage", name=_uniq("email"), use_global_settings=False,
        host="mailpit", port=1025, use_tls=False, use_ssl=False,
        from_address="authentik@test.local",
    )
    slug = _uniq("recovery-flow")
    flow = agent.call("create_flow", name=slug, slug=slug, title="Recovery", designation="recovery")
    default = next(brand for brand in agent.call("list_brands") if brand["default"])
    brand = agent.call("show_brand", brand_uuid=default["brand_uuid"])
    old_recovery = brand["flow_recovery"]
    configured = agent.call("update_brand", brand_uuid=brand["brand_uuid"], flow_recovery=flow["pk"])
    assert configured["flow_recovery"] == flow["pk"]
    try:
        sent = agent.call("send_recovery_email", id=user["pk"], email_stage=stage["pk"], token_duration="minutes=10")
        assert sent == {"status": "ok"}, sent
        deadline = time.monotonic() + 30
        message = None
        with httpx.Client(base_url="http://localhost:8025") as mail:
            while time.monotonic() < deadline:
                response = mail.get("/api/v1/search", params={"query": "to:" + address})
                response.raise_for_status()
                messages = response.json()["messages"]
                if messages:
                    message = mail.get("/api/v1/message/" + messages[0]["ID"]).json()
                    break
                time.sleep(0.2)
        assert message is not None, "Recovery email was not delivered to the test SMTP server"
        assert any(item["Address"] == address for item in message["To"])
        content = message.get("Text", "") + message.get("HTML", "")
        assert "token=" in content and "recovery" in content
    finally:
        agent.call("update_brand", brand_uuid=brand["brand_uuid"], flow_recovery=old_recovery)
        agent.call("delete_flow", slug=slug)
        agent.call("delete_email_stage", stage_uuid=stage["pk"])
        agent.call("delete_user", id=user["pk"])
