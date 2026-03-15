from ..registry import _op
from .groups import authentik_flows_read
from .helpers import SLIM_FLOW, _get_client, _paginated


@_op(authentik_flows_read)
def list_flows(limit: int = 20):
    """List flows (slim)."""
    return _paginated("/flows/instances/", limit=limit, slim_fields=SLIM_FLOW)


@_op(authentik_flows_read)
def show_flow(slug: str):
    """Get full flow details."""
    return _get_client().get(f"/flows/instances/{slug}/")


@_op(authentik_flows_read)
def get_flow_diagram(slug: str):
    """Get flow diagram."""
    return _get_client().get(f"/flows/instances/{slug}/diagram/")


@_op(authentik_flows_read)
def export_flow(slug: str):
    """Export flow as YAML."""
    return _get_client().get(f"/flows/instances/{slug}/export/")


@_op(authentik_flows_read)
def list_flow_bindings(limit: int = 20):
    """List flow stage bindings."""
    return _paginated("/flows/bindings/", limit=limit)


@_op(authentik_flows_read)
def show_flow_binding(id: str):
    """Get flow stage binding details."""
    return _get_client().get(f"/flows/bindings/{id}/")
