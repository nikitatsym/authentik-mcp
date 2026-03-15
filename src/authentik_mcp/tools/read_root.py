from ..registry import _op
from .groups import authentik_read
from .helpers import _get_client


@_op(authentik_read)
def get_config():
    """Get Authentik root config."""
    return _get_client().get("/root/config/")
