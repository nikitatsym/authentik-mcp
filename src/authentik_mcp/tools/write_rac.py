from ..registry import _op
from .groups import authentik_write
from .helpers import _get_client, _ok


@_op(authentik_write)
def update_rac_connection_token(id: str, **kwargs):
    """Update a RAC connection token."""
    return _ok(_get_client().patch(f"/rac/connection_tokens/{id}/", json=kwargs))


@_op(authentik_write)
def create_rac_endpoint(name: str, **kwargs):
    """Create a RAC endpoint. Required: name."""
    return _ok(_get_client().post("/rac/endpoints/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_rac_endpoint(id: str, **kwargs):
    """Update a RAC endpoint."""
    return _ok(_get_client().patch(f"/rac/endpoints/{id}/", json=kwargs))
