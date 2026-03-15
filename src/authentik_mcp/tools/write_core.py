from ..registry import _op
from .groups import authentik_write
from .helpers import _get_client, _ok

# ── Core — Users ─────────────────────────────────────────────────────


@_op(authentik_write)
def create_user(username: str, name: str, **kwargs):
    """Create a user. Required: username, name. Optional: email, is_active, path, groups, etc."""
    return _ok(_get_client().post("/core/users/", json={"username": username, "name": name, **kwargs}))


@_op(authentik_write)
def update_user(id: int, **kwargs):
    """Update a user. Pass fields to change."""
    return _ok(_get_client().patch(f"/core/users/{id}/", json=kwargs))


@_op(authentik_write)
def set_password(id: int, password: str):
    """Set a user's password."""
    return _ok(_get_client().post(f"/core/users/{id}/set_password/", json={"password": password}))


@_op(authentik_write)
def create_service_account(username: str, **kwargs):
    """Create a service account. Required: username."""
    return _ok(_get_client().post("/core/users/service_account/", json={"username": username, **kwargs}))


@_op(authentik_write)
def create_recovery_link(id: int):
    """Create a recovery link for a user."""
    return _ok(_get_client().post(f"/core/users/{id}/recovery/"))


@_op(authentik_write)
def send_recovery_email(id: int):
    """Send recovery email to a user."""
    return _ok(_get_client().post(f"/core/users/{id}/recovery_email/"))


@_op(authentik_write)
def export_users():
    """Export users."""
    return _ok(_get_client().post("/core/users/export/"))


@_op(authentik_write)
def impersonate_user(id: int):
    """Impersonate a user."""
    return _ok(_get_client().post(f"/core/users/{id}/impersonate/"))


@_op(authentik_write)
def impersonate_end():
    """End user impersonation."""
    return _ok(_get_client().get("/core/users/impersonate_end/"))


# ── Core — Groups ────────────────────────────────────────────────────


@_op(authentik_write)
def create_group(name: str, **kwargs):
    """Create a group. Required: name."""
    return _ok(_get_client().post("/core/groups/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_group(id: str, **kwargs):
    """Update a group. Pass fields to change."""
    return _ok(_get_client().patch(f"/core/groups/{id}/", json=kwargs))


@_op(authentik_write)
def add_user_to_group(group_id: str, user_id: int):
    """Add a user to a group."""
    return _ok(_get_client().post(f"/core/groups/{group_id}/add_user/", json={"pk": user_id}))


@_op(authentik_write)
def remove_user_from_group(group_id: str, user_id: int):
    """Remove a user from a group."""
    return _ok(_get_client().post(f"/core/groups/{group_id}/remove_user/", json={"pk": user_id}))


# ── Core — Applications ──────────────────────────────────────────────


@_op(authentik_write)
def create_application(name: str, slug: str, **kwargs):
    """Create an application. Required: name, slug."""
    return _ok(_get_client().post("/core/applications/", json={"name": name, "slug": slug, **kwargs}))


@_op(authentik_write)
def update_application(slug: str, **kwargs):
    """Update an application. Pass fields to change."""
    return _ok(_get_client().patch(f"/core/applications/{slug}/", json=kwargs))


@_op(authentik_write)
def update_transactional_application(**kwargs):
    """Create or update an application and its provider atomically."""
    return _ok(_get_client().put("/core/transactional_applications/", json=kwargs))


# ── Core — Application Entitlements ──────────────────────────────────


@_op(authentik_write)
def create_app_entitlement(app: str, **kwargs):
    """Create an application entitlement. Required: app."""
    return _ok(_get_client().post("/core/application_entitlements/", json={"app": app, **kwargs}))


@_op(authentik_write)
def update_app_entitlement(id: str, **kwargs):
    """Update an application entitlement."""
    return _ok(_get_client().patch(f"/core/application_entitlements/{id}/", json=kwargs))


# ── Core — Tokens ────────────────────────────────────────────────────


@_op(authentik_write)
def create_token(identifier: str, **kwargs):
    """Create a token. Required: identifier."""
    return _ok(_get_client().post("/core/tokens/", json={"identifier": identifier, **kwargs}))


@_op(authentik_write)
def update_token(identifier: str, **kwargs):
    """Update a token. Pass fields to change."""
    return _ok(_get_client().patch(f"/core/tokens/{identifier}/", json=kwargs))


@_op(authentik_write)
def set_token_key(identifier: str, key: str):
    """Set a token's key value."""
    return _ok(_get_client().post(f"/core/tokens/{identifier}/set_key/", json={"key": key}))


# ── Core — Brands ────────────────────────────────────────────────────


@_op(authentik_write)
def create_brand(domain: str, **kwargs):
    """Create a brand. Required: domain."""
    return _ok(_get_client().post("/core/brands/", json={"domain": domain, **kwargs}))


@_op(authentik_write)
def update_brand(id: str, **kwargs):
    """Update a brand. Pass fields to change."""
    return _ok(_get_client().patch(f"/core/brands/{id}/", json=kwargs))
