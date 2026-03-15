from ..registry import _op
from .groups import authentik_flows_write
from .helpers import _get_client, _ok


@_op(authentik_flows_write)
def create_flow(name: str, slug: str, **kwargs):
    """Create a flow. Required: name, slug."""
    return _ok(_get_client().post("/flows/instances/", json={"name": name, "slug": slug, **kwargs}))


@_op(authentik_flows_write)
def update_flow(slug: str, **kwargs):
    """Update a flow."""
    return _ok(_get_client().patch(f"/flows/instances/{slug}/", json=kwargs))


@_op(authentik_flows_write)
def import_flow(**kwargs):
    """Import a flow."""
    return _ok(_get_client().post("/flows/instances/import/", json=kwargs))


@_op(authentik_flows_write)
def clear_flow_cache():
    """Clear flow cache."""
    return _ok(_get_client().post("/flows/instances/cache_clear/"))


@_op(authentik_flows_write)
def create_flow_binding(target: str, stage: str, order: int, **kwargs):
    """Create a flow stage binding. Required: target, stage, order."""
    return _ok(_get_client().post("/flows/bindings/", json={"target": target, "stage": stage, "order": order, **kwargs}))


@_op(authentik_flows_write)
def update_flow_binding(id: str, **kwargs):
    """Update a flow stage binding."""
    return _ok(_get_client().patch(f"/flows/bindings/{id}/", json=kwargs))
