from ..registry import _op
from .groups import authentik_write
from .helpers import _get_client, _ok


@_op(authentik_write)
def create_role(name: str, **kwargs):
    """Create an RBAC role. Required: name."""
    return _ok(_get_client().post("/rbac/roles/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_role(id: str, **kwargs):
    """Update an RBAC role."""
    return _ok(_get_client().patch(f"/rbac/roles/{id}/", json=kwargs))


@_op(authentik_write)
def add_user_to_role(role_id: str, user_id: int):
    """Add a user to a role."""
    return _ok(_get_client().post(f"/rbac/roles/{role_id}/add_user/", json={"pk": user_id}))


@_op(authentik_write)
def remove_user_from_role(role_id: str, user_id: int):
    """Remove a user from a role."""
    return _ok(_get_client().post(f"/rbac/roles/{role_id}/remove_user/", json={"pk": user_id}))


@_op(authentik_write)
def create_initial_permission(**kwargs):
    """Create an initial permission."""
    return _ok(_get_client().post("/rbac/initial_permissions/", json=kwargs))


@_op(authentik_write)
def update_initial_permission(id: int, **kwargs):
    """Update an initial permission."""
    return _ok(_get_client().patch(f"/rbac/initial_permissions/{id}/", json=kwargs))


@_op(authentik_write)
def assign_permissions_to_role(role: str, **kwargs):
    """Assign permissions to a role."""
    return _ok(_get_client().post("/rbac/permissions/assigned_by_roles/assign/", json={"role": role, **kwargs}))


@_op(authentik_write)
def unassign_permissions_from_role(role: str, **kwargs):
    """Unassign permissions from a role."""
    return _ok(_get_client().patch("/rbac/permissions/assigned_by_roles/unassign/", json={"role": role, **kwargs}))
