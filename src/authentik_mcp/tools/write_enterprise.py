from ..registry import _op
from .groups import authentik_write
from .helpers import _get_client, _ok


@_op(authentik_write)
def create_license(key: str, **kwargs):
    """Create an enterprise license. Required: key."""
    return _ok(_get_client().post("/enterprise/license/", json={"key": key, **kwargs}))


@_op(authentik_write)
def update_license(id: str, **kwargs):
    """Update an enterprise license."""
    return _ok(_get_client().patch(f"/enterprise/license/{id}/", json=kwargs))
