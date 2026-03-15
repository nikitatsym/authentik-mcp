from ..registry import _op
from .groups import authentik_write
from .helpers import _get_client, _ok


@_op(authentik_write)
def update_endpoint_device(id: str, **kwargs):
    """Update an endpoint device."""
    return _ok(_get_client().patch(f"/endpoints/devices/{id}/", json=kwargs))


@_op(authentik_write)
def create_agent_connector(name: str, **kwargs):
    """Create an agent connector. Required: name."""
    return _ok(_get_client().post("/endpoints/agents/connectors/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_agent_connector(id: str, **kwargs):
    """Update an agent connector."""
    return _ok(_get_client().patch(f"/endpoints/agents/connectors/{id}/", json=kwargs))


@_op(authentik_write)
def create_agent_enrollment_token(**kwargs):
    """Create an agent enrollment token."""
    return _ok(_get_client().post("/endpoints/agents/enrollment_tokens/", json=kwargs))


@_op(authentik_write)
def update_agent_enrollment_token(id: str, **kwargs):
    """Update an agent enrollment token."""
    return _ok(_get_client().patch(f"/endpoints/agents/enrollment_tokens/{id}/", json=kwargs))


@_op(authentik_write)
def create_device_access_group(name: str, **kwargs):
    """Create a device access group. Required: name."""
    return _ok(_get_client().post("/endpoints/device_access_groups/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_device_access_group(id: str, **kwargs):
    """Update a device access group."""
    return _ok(_get_client().patch(f"/endpoints/device_access_groups/{id}/", json=kwargs))


@_op(authentik_write)
def create_device_binding(**kwargs):
    """Create a device binding."""
    return _ok(_get_client().post("/endpoints/device_bindings/", json=kwargs))


@_op(authentik_write)
def update_device_binding(id: str, **kwargs):
    """Update a device binding."""
    return _ok(_get_client().patch(f"/endpoints/device_bindings/{id}/", json=kwargs))


@_op(authentik_write)
def create_fleet_connector(name: str, **kwargs):
    """Create a fleet connector. Required: name."""
    return _ok(_get_client().post("/endpoints/fleet_connectors/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_fleet_connector(id: str, **kwargs):
    """Update a fleet connector."""
    return _ok(_get_client().patch(f"/endpoints/fleet_connectors/{id}/", json=kwargs))


@_op(authentik_write)
def create_google_chrome_connector(name: str, **kwargs):
    """Create a Google Chrome connector. Required: name."""
    return _ok(_get_client().post("/endpoints/google_chrome_connectors/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_google_chrome_connector(id: str, **kwargs):
    """Update a Google Chrome connector."""
    return _ok(_get_client().patch(f"/endpoints/google_chrome_connectors/{id}/", json=kwargs))
