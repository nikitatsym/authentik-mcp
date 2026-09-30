import json

import httpx
import pytest

from authentik_mcp import client_var, server
from authentik_mcp.client import AuthentikClient


@pytest.fixture
def requests():
    recorded = []

    def respond(request):
        recorded.append(request)
        if request.method == "GET" and "/policies/bindings/" in request.url.path:
            return httpx.Response(200, json={"group": "existing", "policy": None, "user": None, "target": "app", "order": 0, "enabled": True, "pk": "not-writable"})
        if request.method == "GET":
            return httpx.Response(200, json={"results": [{"pk": 7, "username": "alice", "attributes": {"private": True}}]})
        return httpx.Response(200, json=json.loads(request.content) if request.content else {})

    client = AuthentikClient(base_url="http://authentik.test", token="test")
    client._http.close()
    client._http = httpx.Client(base_url="http://authentik.test/api/v3/", transport=httpx.MockTransport(respond))
    binding = client_var.set(client)
    try:
        yield recorded
    finally:
        client_var.reset(binding)
        client._http.close()


def test_required_recovery_email_stage_is_checked_before_http(requests):
    result = server._dispatch("SendRecoveryEmail", "authentik_write", {"id": 7})
    assert "email_stage: Field required" in result["error"]
    assert requests == []


def test_required_bulk_session_and_role_filters_are_checked_before_http(requests):
    sessions = server._dispatch("BulkDeleteSessions", "authentik_delete", {})
    permissions = server._dispatch("ListPermissionsAssignedByRoles", "authentik_read", {})
    assert "user_pks: Field required" in sessions["error"]
    assert "model: Field required" in permissions["error"]
    assert requests == []


def test_nullable_binding_subject_is_distinct_from_omission(requests):
    uuid = "f1513508-4ccf-4e3c-b2ea-479b26db086d"
    server._dispatch("UpdatePolicyBinding", "authentik_flows_write", {"policy_binding_uuid": uuid, "enabled": False})
    body = json.loads(requests[-1].content)
    assert body["group"] == "existing" and body["enabled"] is False
    assert "pk" not in body
    server._dispatch("UpdatePolicyBinding", "authentik_flows_write", {"policy_binding_uuid": uuid, "group": None})
    assert json.loads(requests[-1].content)["group"] is None


def test_body_identifier_does_not_replace_path_identifier(requests):
    server._dispatch("UpdateApplication", "authentik_write", {"slug": "old", "body_slug": "new"})
    assert requests[-1].url.path == "/api/v3/core/applications/old/"
    assert json.loads(requests[-1].content) == {"slug": "new"}


def test_list_projection_and_explicit_page_size(requests):
    result = server._dispatch("ListUsers", "authentik_read", {"page": 2, "page_size": 5, "limit": 5})
    assert result == [{"pk": 7, "username": "alice"}]
    assert requests[-1].url.params["page"] == "2"
    assert requests[-1].url.params["page_size"] == "5"


def test_unknown_body_field_is_rejected_before_http(requests):
    result = server._dispatch("UpdateUser", "authentik_write", {"id": 7, "bogus": "ignored?"})
    assert "bogus" in result["error"]
    assert requests == []
