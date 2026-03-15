from ..registry import _op
from .groups import authentik_read
from .helpers import _get_client, _paginated


@_op(authentik_read)
def list_licenses(limit: int = 20):
    """List enterprise licenses."""
    return _paginated("/enterprise/license/", limit=limit)


@_op(authentik_read)
def show_license(id: str):
    """Get license details."""
    return _get_client().get(f"/enterprise/license/{id}/")


@_op(authentik_read)
def get_license_forecast():
    """Get license forecast."""
    return _get_client().get("/enterprise/license/forecast/")


@_op(authentik_read)
def get_license_summary():
    """Get license summary."""
    return _get_client().get("/enterprise/license/summary/")


@_op(authentik_read)
def get_install_id():
    """Get installation ID."""
    return _get_client().get("/enterprise/license/install_id/")
