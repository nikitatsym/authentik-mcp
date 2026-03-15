from ..registry import _op
from .groups import authentik_read
from .helpers import _get_client, _paginated


@_op(authentik_read)
def list_ssf_streams(limit: int = 20):
    """List SSF streams."""
    return _paginated("/ssf/streams/", limit=limit)


@_op(authentik_read)
def show_ssf_stream(id: str):
    """Get SSF stream details."""
    return _get_client().get(f"/ssf/streams/{id}/")
