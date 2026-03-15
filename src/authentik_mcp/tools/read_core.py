from ..registry import _op
from .groups import authentik_read
from .helpers import SLIM_APP, SLIM_GROUP, SLIM_USER, _get_client, _paginated

# ── Core — Users ─────────────────────────────────────────────────────


@_op(authentik_read)
def list_users(search: str | None = None, path: str | None = None, limit: int = 20):
    """List users (slim)."""
    p = {}
    if search is not None:
        p["search"] = search
    if path is not None:
        p["path"] = path
    return _paginated("/core/users/", p, limit, SLIM_USER)


@_op(authentik_read)
def show_user(id: int):
    """Get full user details."""
    return _get_client().get(f"/core/users/{id}/")


@_op(authentik_read)
def get_me():
    """Get current user info."""
    return _get_client().get("/core/users/me/")


@_op(authentik_read)
def list_user_paths():
    """List user path prefixes."""
    return _get_client().get("/core/users/paths/")


@_op(authentik_read)
def list_user_consent(user: int | None = None, limit: int = 20):
    """List user consent entries."""
    p = {}
    if user is not None:
        p["user"] = user
    return _paginated("/core/user_consent/", p, limit)


@_op(authentik_read)
def show_user_consent(id: int):
    """Get user consent details."""
    return _get_client().get(f"/core/user_consent/{id}/")


# ── Core — Groups ────────────────────────────────────────────────────


@_op(authentik_read)
def list_groups(search: str | None = None, limit: int = 20):
    """List groups (slim)."""
    p = {}
    if search is not None:
        p["search"] = search
    return _paginated("/core/groups/", p, limit, SLIM_GROUP)


@_op(authentik_read)
def show_group(id: str):
    """Get full group details."""
    return _get_client().get(f"/core/groups/{id}/")


# ── Core — Applications ──────────────────────────────────────────────


@_op(authentik_read)
def list_applications(search: str | None = None, limit: int = 20):
    """List applications (slim)."""
    p = {}
    if search is not None:
        p["search"] = search
    return _paginated("/core/applications/", p, limit, SLIM_APP)


@_op(authentik_read)
def show_application(slug: str):
    """Get full application details."""
    return _get_client().get(f"/core/applications/{slug}/")


@_op(authentik_read)
def check_access(slug: str):
    """Check access to an application."""
    return _get_client().get(f"/core/applications/{slug}/check_access/")


# ── Core — Application Entitlements ──────────────────────────────────


@_op(authentik_read)
def list_app_entitlements(app: str | None = None, limit: int = 20):
    """List application entitlements."""
    p = {}
    if app is not None:
        p["app"] = app
    return _paginated("/core/application_entitlements/", p, limit)


@_op(authentik_read)
def show_app_entitlement(id: str):
    """Get application entitlement details."""
    return _get_client().get(f"/core/application_entitlements/{id}/")


# ── Core — Tokens ────────────────────────────────────────────────────


@_op(authentik_read)
def list_tokens(limit: int = 20):
    """List tokens."""
    return _paginated("/core/tokens/", limit=limit)


@_op(authentik_read)
def show_token(identifier: str):
    """Get token details."""
    return _get_client().get(f"/core/tokens/{identifier}/")


@_op(authentik_read)
def view_token_key(identifier: str):
    """View token key value."""
    return _get_client().get(f"/core/tokens/{identifier}/view_key/")


# ── Core — Brands ────────────────────────────────────────────────────


@_op(authentik_read)
def list_brands(limit: int = 20):
    """List brands."""
    return _paginated("/core/brands/", limit=limit)


@_op(authentik_read)
def show_brand(id: str):
    """Get brand details."""
    return _get_client().get(f"/core/brands/{id}/")


@_op(authentik_read)
def get_current_brand():
    """Get current brand."""
    return _get_client().get("/core/brands/current/")


# ── Core — Sessions ──────────────────────────────────────────────────


@_op(authentik_read)
def list_sessions(limit: int = 20):
    """List authenticated sessions."""
    return _paginated("/core/authenticated_sessions/", limit=limit)


@_op(authentik_read)
def show_session(id: str):
    """Get session details."""
    return _get_client().get(f"/core/authenticated_sessions/{id}/")
