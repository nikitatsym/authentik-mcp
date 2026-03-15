from ..registry import _op
from .groups import authentik_read
from .helpers import _get_client, _paginated


@_op(authentik_read)
def list_exports(limit: int = 20):
    """List report exports."""
    return _paginated("/reports/exports/", limit=limit)


@_op(authentik_read)
def show_export(id: str):
    """Get report export details."""
    return _get_client().get(f"/reports/exports/{id}/")
