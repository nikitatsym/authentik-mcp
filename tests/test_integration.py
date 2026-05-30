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
        binding = agent.call(
            "create_policy_binding", target=app_pk, group=group_pk, order=0
        )
        binding_pk = binding["pk"]
        assert binding["group"] == group_pk
        assert binding["policy"] is None, \
            f"expected null policy on a group binding, got {binding['policy']!r}"
        assert binding["target"] == app_pk

        # Readable back through show + list.
        shown = agent.call("show_policy_binding", id=binding_pk)
        assert shown["group"] == group_pk and shown["policy"] is None

        listed = agent.call("list_policy_bindings", limit=100)
        assert any(b["pk"] == binding_pk for b in listed)

        # Update toggles `enabled` via **kwargs passthrough. Authentik re-runs
        # the "exactly one of policy/group/user" check on PATCH, so the subject
        # (group) must be re-sent alongside the change.
        updated = agent.call(
            "update_policy_binding", id=binding_pk, group=group_pk, enabled=False
        )
        assert updated["enabled"] is False
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
