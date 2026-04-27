from pathlib import Path

from ..registry import _op
from .groups import authentik_admin
from .helpers import (
    SLIM_ADMIN_FILE,
    SLIM_AUTHENTICATOR_DEVICE,
    SLIM_VERSION_HISTORY,
    _get_client,
    _ok,
    _paginated,
)

# ── Admin (Read) ─────────────────────────────────────────────────────


@_op(authentik_admin)
def list_admin_apps():
    """List admin apps."""
    return _get_client().get("/admin/apps/")


@_op(authentik_admin)
def list_admin_models():
    """List admin models."""
    return _get_client().get("/admin/models/")


@_op(authentik_admin)
def get_admin_settings():
    """Get admin settings."""
    return _get_client().get("/admin/settings/")


@_op(authentik_admin)
def get_system_info():
    """Get system info."""
    return _get_client().get("/admin/system/")


@_op(authentik_admin)
def get_admin_version():
    """Get Authentik version."""
    return _get_client().get("/admin/version/")


@_op(authentik_admin)
def list_version_history(limit: int = 20):
    """List version history."""
    return _paginated("/admin/version/history/", limit=limit, slim_fields=SLIM_VERSION_HISTORY)


@_op(authentik_admin)
def show_version_history(id: int):
    """Get version history entry details."""
    return _get_client().get(f"/admin/version/history/{id}/")


@_op(authentik_admin)
def list_admin_files(limit: int = 20):
    """List admin files."""
    return _paginated("/admin/file/", limit=limit, slim_fields=SLIM_ADMIN_FILE)


# ── Admin (Write) ────────────────────────────────────────────────────


@_op(authentik_admin)
def update_admin_settings(**kwargs):
    """Update admin settings. Pass fields to change."""
    return _ok(_get_client().patch("/admin/settings/", json=kwargs))


@_op(authentik_admin)
def create_admin_system():
    """Create admin system entry."""
    return _ok(_get_client().post("/admin/system/"))


@_op(authentik_admin)
def create_admin_file(file_path: str, name: str | None = None):
    """Upload a file to authentik media (/media/public/). Returns the served URL."""
    p = Path(file_path)
    with p.open("rb") as f:
        return _ok(_get_client().post(
            "/admin/file/",
            files={"file": (name or p.name, f)},
            data={"name": name or p.name},
        ))


# ── Authenticators — Admin (Read) ────────────────────────────────────


@_op(authentik_admin)
def list_admin_authenticators():
    """List all admin authenticator devices."""
    return _get_client().get("/authenticators/admin/all/")


@_op(authentik_admin)
def list_admin_duo_devices(limit: int = 20):
    """List admin Duo devices."""
    return _paginated("/authenticators/admin/duo/", limit=limit, slim_fields=SLIM_AUTHENTICATOR_DEVICE)


@_op(authentik_admin)
def show_admin_duo_device(id: int):
    """Get admin Duo device details."""
    return _get_client().get(f"/authenticators/admin/duo/{id}/")


@_op(authentik_admin)
def list_admin_email_devices(limit: int = 20):
    """List admin email devices."""
    return _paginated("/authenticators/admin/email/", limit=limit, slim_fields=SLIM_AUTHENTICATOR_DEVICE)


@_op(authentik_admin)
def show_admin_email_device(id: int):
    """Get admin email device details."""
    return _get_client().get(f"/authenticators/admin/email/{id}/")


@_op(authentik_admin)
def list_admin_endpoint_devices(limit: int = 20):
    """List admin endpoint devices."""
    return _paginated("/authenticators/admin/endpoint/", limit=limit, slim_fields=SLIM_AUTHENTICATOR_DEVICE)


@_op(authentik_admin)
def show_admin_endpoint_device(id: int):
    """Get admin endpoint device details."""
    return _get_client().get(f"/authenticators/admin/endpoint/{id}/")


@_op(authentik_admin)
def list_admin_sms_devices(limit: int = 20):
    """List admin SMS devices."""
    return _paginated("/authenticators/admin/sms/", limit=limit, slim_fields=SLIM_AUTHENTICATOR_DEVICE)


@_op(authentik_admin)
def show_admin_sms_device(id: int):
    """Get admin SMS device details."""
    return _get_client().get(f"/authenticators/admin/sms/{id}/")


@_op(authentik_admin)
def list_admin_static_devices(limit: int = 20):
    """List admin static devices."""
    return _paginated("/authenticators/admin/static/", limit=limit, slim_fields=SLIM_AUTHENTICATOR_DEVICE)


@_op(authentik_admin)
def show_admin_static_device(id: int):
    """Get admin static device details."""
    return _get_client().get(f"/authenticators/admin/static/{id}/")


@_op(authentik_admin)
def list_admin_totp_devices(limit: int = 20):
    """List admin TOTP devices."""
    return _paginated("/authenticators/admin/totp/", limit=limit, slim_fields=SLIM_AUTHENTICATOR_DEVICE)


@_op(authentik_admin)
def show_admin_totp_device(id: int):
    """Get admin TOTP device details."""
    return _get_client().get(f"/authenticators/admin/totp/{id}/")


@_op(authentik_admin)
def list_admin_webauthn_devices(limit: int = 20):
    """List admin WebAuthn devices."""
    return _paginated("/authenticators/admin/webauthn/", limit=limit, slim_fields=SLIM_AUTHENTICATOR_DEVICE)


@_op(authentik_admin)
def show_admin_webauthn_device(id: int):
    """Get admin WebAuthn device details."""
    return _get_client().get(f"/authenticators/admin/webauthn/{id}/")


# ── Authenticators — Admin (Write) ───────────────────────────────────


@_op(authentik_admin)
def create_admin_duo_device(**kwargs):
    """Create admin Duo device."""
    return _ok(_get_client().post("/authenticators/admin/duo/", json=kwargs))


@_op(authentik_admin)
def update_admin_duo_device(id: int, **kwargs):
    """Update admin Duo device."""
    return _ok(_get_client().patch(f"/authenticators/admin/duo/{id}/", json=kwargs))


@_op(authentik_admin)
def create_admin_email_device(**kwargs):
    """Create admin email device."""
    return _ok(_get_client().post("/authenticators/admin/email/", json=kwargs))


@_op(authentik_admin)
def update_admin_email_device(id: int, **kwargs):
    """Update admin email device."""
    return _ok(_get_client().patch(f"/authenticators/admin/email/{id}/", json=kwargs))


@_op(authentik_admin)
def create_admin_endpoint_device(**kwargs):
    """Create admin endpoint device."""
    return _ok(_get_client().post("/authenticators/admin/endpoint/", json=kwargs))


@_op(authentik_admin)
def update_admin_endpoint_device(id: int, **kwargs):
    """Update admin endpoint device."""
    return _ok(_get_client().patch(f"/authenticators/admin/endpoint/{id}/", json=kwargs))


@_op(authentik_admin)
def create_admin_sms_device(**kwargs):
    """Create admin SMS device."""
    return _ok(_get_client().post("/authenticators/admin/sms/", json=kwargs))


@_op(authentik_admin)
def update_admin_sms_device(id: int, **kwargs):
    """Update admin SMS device."""
    return _ok(_get_client().patch(f"/authenticators/admin/sms/{id}/", json=kwargs))


@_op(authentik_admin)
def create_admin_static_device(**kwargs):
    """Create admin static device."""
    return _ok(_get_client().post("/authenticators/admin/static/", json=kwargs))


@_op(authentik_admin)
def update_admin_static_device(id: int, **kwargs):
    """Update admin static device."""
    return _ok(_get_client().patch(f"/authenticators/admin/static/{id}/", json=kwargs))


@_op(authentik_admin)
def create_admin_totp_device(**kwargs):
    """Create admin TOTP device."""
    return _ok(_get_client().post("/authenticators/admin/totp/", json=kwargs))


@_op(authentik_admin)
def update_admin_totp_device(id: int, **kwargs):
    """Update admin TOTP device."""
    return _ok(_get_client().patch(f"/authenticators/admin/totp/{id}/", json=kwargs))


@_op(authentik_admin)
def create_admin_webauthn_device(**kwargs):
    """Create admin WebAuthn device."""
    return _ok(_get_client().post("/authenticators/admin/webauthn/", json=kwargs))


@_op(authentik_admin)
def update_admin_webauthn_device(id: int, **kwargs):
    """Update admin WebAuthn device."""
    return _ok(_get_client().patch(f"/authenticators/admin/webauthn/{id}/", json=kwargs))


# ── Lifecycle ────────────────────────────────────────────────────────


@_op(authentik_admin)
def create_lifecycle_iteration():
    """Create lifecycle iteration."""
    return _ok(_get_client().post("/lifecycle/iterations/"))
