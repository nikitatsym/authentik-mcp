from ..registry import _op
from .groups import authentik_read
from .helpers import SLIM_CERTIFICATE, _get_client, _paginated


@_op(authentik_read)
def list_certificates(limit: int = 20):
    """List certificate-key pairs."""
    return _paginated("/crypto/certificatekeypairs/", limit=limit, slim_fields=SLIM_CERTIFICATE)


@_op(authentik_read)
def show_certificate(id: str):
    """Get certificate-key pair details."""
    return _get_client().get(f"/crypto/certificatekeypairs/{id}/")


@_op(authentik_read)
def view_certificate(id: str):
    """View certificate data."""
    return _get_client().get(f"/crypto/certificatekeypairs/{id}/view_certificate/")


@_op(authentik_read)
def view_private_key(id: str):
    """View private key data."""
    return _get_client().get(f"/crypto/certificatekeypairs/{id}/view_private_key/")
