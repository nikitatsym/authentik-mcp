from ..registry import _op
from .groups import authentik_write
from .helpers import _get_client, _ok


@_op(authentik_write)
def update_authenticator_totp(id: int, **kwargs):
    """Update a TOTP authenticator device."""
    return _ok(_get_client().patch(f"/authenticators/totp/{id}/", json=kwargs))


@_op(authentik_write)
def update_authenticator_webauthn(id: int, **kwargs):
    """Update a WebAuthn authenticator device."""
    return _ok(_get_client().patch(f"/authenticators/webauthn/{id}/", json=kwargs))


@_op(authentik_write)
def update_authenticator_duo(id: int, **kwargs):
    """Update a Duo authenticator device."""
    return _ok(_get_client().patch(f"/authenticators/duo/{id}/", json=kwargs))


@_op(authentik_write)
def update_authenticator_sms(id: int, **kwargs):
    """Update an SMS authenticator device."""
    return _ok(_get_client().patch(f"/authenticators/sms/{id}/", json=kwargs))


@_op(authentik_write)
def update_authenticator_static(id: int, **kwargs):
    """Update a static authenticator device."""
    return _ok(_get_client().patch(f"/authenticators/static/{id}/", json=kwargs))


@_op(authentik_write)
def update_authenticator_email(id: int, **kwargs):
    """Update an email authenticator device."""
    return _ok(_get_client().patch(f"/authenticators/email/{id}/", json=kwargs))
