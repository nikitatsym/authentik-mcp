from ..registry import _op
from .groups import authentik_read
from .helpers import SLIM_ENDPOINT, _get_client, _paginated

# ── Endpoint Devices ─────────────────────────────────────────────────


@_op(authentik_read)
def list_endpoint_devices(limit: int = 20):
    """List endpoint devices."""
    return _paginated("/endpoints/devices/", limit=limit, slim_fields=SLIM_ENDPOINT)


@_op(authentik_read)
def show_endpoint_device(id: str):
    """Get endpoint device details."""
    return _get_client().get(f"/endpoints/devices/{id}/")


@_op(authentik_read)
def get_endpoint_device_summary():
    """Get endpoint device summary."""
    return _get_client().get("/endpoints/devices/summary/")


# ── Endpoint Connectors ──────────────────────────────────────────────


@_op(authentik_read)
def list_endpoint_connectors(limit: int = 20):
    """List endpoint connectors."""
    return _paginated("/endpoints/connectors/", limit=limit, slim_fields=SLIM_ENDPOINT)


@_op(authentik_read)
def show_endpoint_connector(id: str):
    """Get endpoint connector details."""
    return _get_client().get(f"/endpoints/connectors/{id}/")


@_op(authentik_read)
def list_endpoint_connector_types():
    """List endpoint connector types."""
    return _get_client().get("/endpoints/connectors/types/")


# ── Agent Connectors ─────────────────────────────────────────────────


@_op(authentik_read)
def list_agent_connectors(limit: int = 20):
    """List agent connectors."""
    return _paginated("/endpoints/agents/connectors/", limit=limit, slim_fields=SLIM_ENDPOINT)


@_op(authentik_read)
def show_agent_connector(id: str):
    """Get agent connector details."""
    return _get_client().get(f"/endpoints/agents/connectors/{id}/")


# ── Agent Enrollment Tokens ──────────────────────────────────────────


@_op(authentik_read)
def list_agent_enrollment_tokens(limit: int = 20):
    """List agent enrollment tokens."""
    return _paginated("/endpoints/agents/enrollment_tokens/", limit=limit, slim_fields=SLIM_ENDPOINT)


@_op(authentik_read)
def show_agent_enrollment_token(id: str):
    """Get agent enrollment token details."""
    return _get_client().get(f"/endpoints/agents/enrollment_tokens/{id}/")


@_op(authentik_read)
def view_enrollment_token_key(id: str):
    """View agent enrollment token key."""
    return _get_client().get(f"/endpoints/agents/enrollment_tokens/{id}/view_key/")


# ── Device Access Groups ─────────────────────────────────────────────


@_op(authentik_read)
def list_device_access_groups(limit: int = 20):
    """List device access groups."""
    return _paginated("/endpoints/device_access_groups/", limit=limit, slim_fields=SLIM_ENDPOINT)


@_op(authentik_read)
def show_device_access_group(id: str):
    """Get device access group details."""
    return _get_client().get(f"/endpoints/device_access_groups/{id}/")


# ── Device Bindings ──────────────────────────────────────────────────


@_op(authentik_read)
def list_device_bindings(limit: int = 20):
    """List device bindings."""
    return _paginated("/endpoints/device_bindings/", limit=limit, slim_fields=SLIM_ENDPOINT)


@_op(authentik_read)
def show_device_binding(id: str):
    """Get device binding details."""
    return _get_client().get(f"/endpoints/device_bindings/{id}/")


# ── Fleet Connectors ─────────────────────────────────────────────────


@_op(authentik_read)
def list_fleet_connectors(limit: int = 20):
    """List fleet connectors."""
    return _paginated("/endpoints/fleet_connectors/", limit=limit, slim_fields=SLIM_ENDPOINT)


@_op(authentik_read)
def show_fleet_connector(id: str):
    """Get fleet connector details."""
    return _get_client().get(f"/endpoints/fleet_connectors/{id}/")


# ── Google Chrome Connectors ─────────────────────────────────────────


@_op(authentik_read)
def list_google_chrome_connectors(limit: int = 20):
    """List Google Chrome connectors."""
    return _paginated("/endpoints/google_chrome_connectors/", limit=limit, slim_fields=SLIM_ENDPOINT)


@_op(authentik_read)
def show_google_chrome_connector(id: str):
    """Get Google Chrome connector details."""
    return _get_client().get(f"/endpoints/google_chrome_connectors/{id}/")
