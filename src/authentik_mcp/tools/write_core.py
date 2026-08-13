from pathlib import Path
from typing import Annotated

from pydantic import Field

from ..registry import _op
from .groups import authentik_write
from .helpers import _get_client, _ok, _verify_response

# Fields PATCH /core/applications/{slug}/ silently drops because they need a
# dedicated endpoint. Used by update_application to fail fast with a hint.
_APP_PATCH_DROPS = {
    "meta_icon": "Use SetApplicationIconUrl(slug, url) or SetApplicationIcon(slug, file_path).",
}

# ── Core — Users ─────────────────────────────────────────────────────


@_op(authentik_write)
def create_user(
    username: str,
    name: str,
    groups: Annotated[
        list[str] | None,
        Field(description="Group UUIDs the user belongs to. Authentik requires this key; defaults to empty."),
    ] = None,
    **kwargs,
):
    """Create a user. Required: username, name. Optional: email, is_active, path, etc."""
    return _ok(_get_client().post("/core/users/", json={
        "username": username, "name": name, "groups": groups or [], **kwargs,
    }))


@_op(authentik_write)
def update_user(id: int, **kwargs):
    """Update a user. Pass fields to change."""
    return _ok(_get_client().patch(f"/core/users/{id}/", json=kwargs))


@_op(authentik_write)
def set_password(id: int, password: str):
    """Set a user's password."""
    return _ok(_get_client().post(f"/core/users/{id}/set_password/", json={"password": password}))


@_op(authentik_write)
def create_service_account(name: str, **kwargs):
    """Create a service account. Required: name (also becomes the username)."""
    return _ok(_get_client().post("/core/users/service_account/", json={"name": name, **kwargs}))


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
def create_group(
    name: str,
    parent: Annotated[
        str | None,
        Field(description="Parent group UUID; null = top-level group (default)."),
    ] = None,
    users: Annotated[
        list[int] | None,
        Field(description="Member user PKs. Authentik requires this key; defaults to empty."),
    ] = None,
    **kwargs,
):
    """Create a group. Required: name. parent/users default to null/empty (Authentik requires them present)."""
    return _ok(_get_client().post("/core/groups/", json={
        "name": name, "parent": parent, "users": users or [], **kwargs,
    }))


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
    """Create an application. Required: name, slug.

    Ungated apps are open to all users. Restrict to a group/user with
    CreatePolicyBinding(target=<app pk>, group=...) in authentik_flows_write.
    """
    return _ok(_get_client().post("/core/applications/", json={"name": name, "slug": slug, **kwargs}))


@_op(authentik_write)
def update_application(slug: str, **kwargs):
    """Update an application. Pass fields to change."""
    bad = [k for k in kwargs if k in _APP_PATCH_DROPS]
    if bad:
        hints = "; ".join(f"{k}: {_APP_PATCH_DROPS[k]}" for k in bad)
        raise ValueError(
            f"PATCH /core/applications/ silently drops these fields: {bad}. {hints}"
        )
    response = _get_client().patch(f"/core/applications/{slug}/", json=kwargs)
    _verify_response(kwargs, response, _APP_PATCH_DROPS)
    return _ok(response)


@_op(authentik_write)
def update_transactional_application(**kwargs):
    """Create or update an application and its provider atomically."""
    return _ok(_get_client().put("/core/transactional/applications/", json=kwargs))


@_op(authentik_write)
def set_application_icon_url(slug: str, url: str):
    """Set application icon by URL (use this instead of UpdateApplication for meta_icon)."""
    return _ok(_get_client().post(
        f"/core/applications/{slug}/set_icon_url/",
        json={"url": url},
    ))


@_op(authentik_write)
def set_application_icon(slug: str, file_path: str):
    """Upload application icon from a local file path (multipart)."""
    p = Path(file_path)
    with p.open("rb") as f:
        return _ok(_get_client().post(
            f"/core/applications/{slug}/set_icon/",
            files={"file": (p.name, f)},
        ))


@_op(authentik_write)
def clear_application_icon(slug: str):
    """Remove the application icon."""
    # An empty url is what clears it; the endpoint takes no other field.
    return _ok(_get_client().post(
        f"/core/applications/{slug}/set_icon_url/",
        json={"url": ""},
    ))


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
