from authentik_mcp.tools.helpers import (
    SLIM_APP,
    SLIM_EVENT,
    SLIM_FLOW,
    SLIM_GROUP,
    SLIM_USER,
    _ok,
    _paginated,
    _slim,
    _slim_list,
)


def test_ok_none():
    assert _ok(None) == {"status": "ok"}


def test_ok_data():
    assert _ok({"x": 1}) == {"x": 1}


def test_slim_flat():
    item = {"pk": 1, "username": "admin", "extra": "ignored"}
    result = _slim(item, {"pk", "username"})
    assert result == {"pk": 1, "username": "admin"}


def test_slim_nested():
    item = {"pk": 1, "provider_obj": {"name": "OAuth2"}, "slug": "app1"}
    result = _slim(item, {"pk", "slug", "provider_obj.name"})
    assert result == {"pk": 1, "slug": "app1", "provider_obj.name": "OAuth2"}


def test_slim_nested_missing():
    item = {"pk": 1, "slug": "app1"}
    result = _slim(item, {"pk", "provider_obj.name"})
    assert result == {"pk": 1}


def test_slim_list_basic():
    items = [{"pk": 1, "name": "a", "x": 9}, {"pk": 2, "name": "b", "x": 8}]
    result = _slim_list(items, {"pk", "name"})
    assert result == [{"pk": 1, "name": "a"}, {"pk": 2, "name": "b"}]


def test_slim_list_non_list():
    assert _slim_list("not a list", {"pk"}) == "not a list"


def test_slim_fields_defined():
    assert "pk" in SLIM_USER
    assert "username" in SLIM_USER
    assert "pk" in SLIM_GROUP
    assert "pk" in SLIM_APP
    assert "provider_obj.name" in SLIM_APP
    assert "pk" in SLIM_FLOW
    assert "pk" in SLIM_EVENT


def test_dispatch_help():
    from authentik_mcp.server import _group_ops

    for group_name, ops in _group_ops.items():
        assert len(ops) > 0, f"Group {group_name} has no operations"

    expected = {
        "authentik_read": 183,
        "authentik_write": 133,
        "authentik_delete": 131,
        "authentik_flows_read": 127,
        "authentik_flows_write": 114,
        "authentik_admin": 41,
    }
    for name, count in expected.items():
        assert len(_group_ops[name]) == count, f"{name}: expected {count}, got {len(_group_ops[name])}"
