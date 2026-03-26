from ..registry import _op
from .groups import authentik_read
from .helpers import SLIM_EXPORT, _get_client, _paginated


@_op(authentik_read)
def list_exports(limit: int = 20):
    """List report exports."""
    return _paginated("/reports/exports/", limit=limit, slim_fields=SLIM_EXPORT)


@_op(authentik_read)
def show_export(id: str):
    """Get report export details."""
    return _get_client().get(f"/reports/exports/{id}/")
