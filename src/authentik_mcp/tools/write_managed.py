from ..registry import _op
from .groups import authentik_write
from .helpers import _get_client, _ok


@_op(authentik_write)
def create_blueprint(name: str, **kwargs):
    """Create a blueprint. Required: name."""
    return _ok(_get_client().post("/managed/blueprints/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_blueprint(id: str, **kwargs):
    """Update a blueprint."""
    return _ok(_get_client().patch(f"/managed/blueprints/{id}/", json=kwargs))


@_op(authentik_write)
def apply_blueprint(id: str):
    """Apply a blueprint."""
    return _ok(_get_client().post(f"/managed/blueprints/{id}/apply/"))
