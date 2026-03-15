from ..registry import _op
from .groups import authentik_write
from .helpers import _get_client, _ok


@_op(authentik_write)
def create_certificate(name: str, **kwargs):
    """Create a certificate-key pair. Required: name."""
    return _ok(_get_client().post("/crypto/certificatekeypairs/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_certificate(id: str, **kwargs):
    """Update a certificate-key pair."""
    return _ok(_get_client().patch(f"/crypto/certificatekeypairs/{id}/", json=kwargs))


@_op(authentik_write)
def generate_certificate(name: str, **kwargs):
    """Generate a new certificate-key pair. Required: name."""
    return _ok(_get_client().post("/crypto/certificatekeypairs/generate/", json={"name": name, **kwargs}))
