from ..registry import _op
from .groups import authentik_flows_write
from .helpers import _get_client, _ok


@_op(authentik_flows_write)
def test_policy(id: str, **kwargs):
    """Test a policy."""
    return _ok(_get_client().post(f"/policies/all/{id}/test/", json=kwargs))


@_op(authentik_flows_write)
def clear_policy_cache():
    """Clear policy cache."""
    return _ok(_get_client().post("/policies/all/cache_clear/"))


@_op(authentik_flows_write)
def create_policy_binding(target: str, policy: str, order: int, **kwargs):
    """Create a policy binding. Required: target, policy, order."""
    return _ok(_get_client().post("/policies/bindings/", json={"target": target, "policy": policy, "order": order, **kwargs}))


@_op(authentik_flows_write)
def update_policy_binding(id: str, **kwargs):
    """Update a policy binding."""
    return _ok(_get_client().patch(f"/policies/bindings/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_expression_policy(name: str, expression: str, **kwargs):
    """Create an expression policy. Required: name, expression."""
    return _ok(_get_client().post("/policies/expression/", json={"name": name, "expression": expression, **kwargs}))


@_op(authentik_flows_write)
def update_expression_policy(id: str, **kwargs):
    """Update an expression policy."""
    return _ok(_get_client().patch(f"/policies/expression/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_password_policy(name: str, **kwargs):
    """Create a password policy. Required: name."""
    return _ok(_get_client().post("/policies/password/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_password_policy(id: str, **kwargs):
    """Update a password policy."""
    return _ok(_get_client().patch(f"/policies/password/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_password_expiry_policy(name: str, **kwargs):
    """Create a password expiry policy. Required: name."""
    return _ok(_get_client().post("/policies/password_expiry/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_password_expiry_policy(id: str, **kwargs):
    """Update a password expiry policy."""
    return _ok(_get_client().patch(f"/policies/password_expiry/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_reputation_policy(name: str, **kwargs):
    """Create a reputation policy. Required: name."""
    return _ok(_get_client().post("/policies/reputation/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_reputation_policy(id: str, **kwargs):
    """Update a reputation policy."""
    return _ok(_get_client().patch(f"/policies/reputation/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_event_matcher_policy(name: str, **kwargs):
    """Create an event matcher policy. Required: name."""
    return _ok(_get_client().post("/policies/event_matcher/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_event_matcher_policy(id: str, **kwargs):
    """Update an event matcher policy."""
    return _ok(_get_client().patch(f"/policies/event_matcher/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_geoip_policy(name: str, **kwargs):
    """Create a GeoIP policy. Required: name."""
    return _ok(_get_client().post("/policies/geoip/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_geoip_policy(id: str, **kwargs):
    """Update a GeoIP policy."""
    return _ok(_get_client().patch(f"/policies/geoip/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_dummy_policy(name: str, **kwargs):
    """Create a dummy policy. Required: name."""
    return _ok(_get_client().post("/policies/dummy/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_dummy_policy(id: str, **kwargs):
    """Update a dummy policy."""
    return _ok(_get_client().patch(f"/policies/dummy/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_unique_password_policy(name: str, **kwargs):
    """Create a unique password policy. Required: name."""
    return _ok(_get_client().post("/policies/unique_password/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_unique_password_policy(id: str, **kwargs):
    """Update a unique password policy."""
    return _ok(_get_client().patch(f"/policies/unique_password/{id}/", json=kwargs))
