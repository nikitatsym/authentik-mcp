from ..registry import _op
from .groups import authentik_read
from .helpers import _get_client, _paginated


@_op(authentik_read)
def list_authenticators():
    """List all authenticator devices."""
    return _get_client().get("/authenticators/all/")


@_op(authentik_read)
def list_authenticator_totp_devices(limit: int = 20):
    """List TOTP authenticator devices."""
    return _paginated("/authenticators/totp/", limit=limit)


@_op(authentik_read)
def show_authenticator_totp_device(id: int):
    """Get TOTP device details."""
    return _get_client().get(f"/authenticators/totp/{id}/")


@_op(authentik_read)
def list_authenticator_webauthn_devices(limit: int = 20):
    """List WebAuthn authenticator devices."""
    return _paginated("/authenticators/webauthn/", limit=limit)


@_op(authentik_read)
def show_authenticator_webauthn_device(id: int):
    """Get WebAuthn device details."""
    return _get_client().get(f"/authenticators/webauthn/{id}/")


@_op(authentik_read)
def list_authenticator_duo_devices(limit: int = 20):
    """List Duo authenticator devices."""
    return _paginated("/authenticators/duo/", limit=limit)


@_op(authentik_read)
def show_authenticator_duo_device(id: int):
    """Get Duo device details."""
    return _get_client().get(f"/authenticators/duo/{id}/")


@_op(authentik_read)
def list_authenticator_sms_devices(limit: int = 20):
    """List SMS authenticator devices."""
    return _paginated("/authenticators/sms/", limit=limit)


@_op(authentik_read)
def show_authenticator_sms_device(id: int):
    """Get SMS device details."""
    return _get_client().get(f"/authenticators/sms/{id}/")


@_op(authentik_read)
def list_authenticator_static_devices(limit: int = 20):
    """List static authenticator devices."""
    return _paginated("/authenticators/static/", limit=limit)


@_op(authentik_read)
def show_authenticator_static_device(id: int):
    """Get static device details."""
    return _get_client().get(f"/authenticators/static/{id}/")


@_op(authentik_read)
def list_authenticator_email_devices(limit: int = 20):
    """List email authenticator devices."""
    return _paginated("/authenticators/email/", limit=limit)


@_op(authentik_read)
def show_authenticator_email_device(id: int):
    """Get email device details."""
    return _get_client().get(f"/authenticators/email/{id}/")


@_op(authentik_read)
def list_authenticator_endpoint_devices(limit: int = 20):
    """List endpoint authenticator devices."""
    return _paginated("/authenticators/endpoint/", limit=limit)


@_op(authentik_read)
def show_authenticator_endpoint_device(id: int):
    """Get endpoint device details."""
    return _get_client().get(f"/authenticators/endpoint/{id}/")
