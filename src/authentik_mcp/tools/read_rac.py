from ..registry import _op
from .groups import authentik_read
from .helpers import SLIM_RAC_ENDPOINT, SLIM_RAC_TOKEN, _get_client, _paginated


@_op(authentik_read)
def list_rac_connection_tokens(limit: int = 20):
    """List RAC connection tokens."""
    return _paginated("/rac/connection_tokens/", limit=limit, slim_fields=SLIM_RAC_TOKEN)


@_op(authentik_read)
def show_rac_connection_token(id: str):
    """Get RAC connection token details."""
    return _get_client().get(f"/rac/connection_tokens/{id}/")


@_op(authentik_read)
def list_rac_endpoints(limit: int = 20):
    """List RAC endpoints."""
    return _paginated("/rac/endpoints/", limit=limit, slim_fields=SLIM_RAC_ENDPOINT)


@_op(authentik_read)
def show_rac_endpoint(id: str):
    """Get RAC endpoint details."""
    return _get_client().get(f"/rac/endpoints/{id}/")
