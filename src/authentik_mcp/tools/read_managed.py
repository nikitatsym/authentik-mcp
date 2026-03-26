from ..registry import _op
from .groups import authentik_read
from .helpers import SLIM_BLUEPRINT, _get_client, _paginated


@_op(authentik_read)
def list_blueprints(limit: int = 20):
    """List blueprints."""
    return _paginated("/managed/blueprints/", limit=limit, slim_fields=SLIM_BLUEPRINT)


@_op(authentik_read)
def show_blueprint(id: str):
    """Get blueprint details."""
    return _get_client().get(f"/managed/blueprints/{id}/")


@_op(authentik_read)
def list_available_blueprints():
    """List available blueprint templates."""
    return _get_client().get("/managed/blueprints/available/")
