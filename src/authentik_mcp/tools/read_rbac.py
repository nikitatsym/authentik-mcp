from ..registry import _op
from .groups import authentik_read
from .helpers import _get_client, _paginated


@_op(authentik_read)
def list_roles(limit: int = 20):
    """List RBAC roles."""
    return _paginated("/rbac/roles/", limit=limit)


@_op(authentik_read)
def show_role(id: str):
    """Get RBAC role details."""
    return _get_client().get(f"/rbac/roles/{id}/")


@_op(authentik_read)
def list_permissions(limit: int = 20):
    """List permissions."""
    return _paginated("/rbac/permissions/", limit=limit)


@_op(authentik_read)
def show_permission(id: int):
    """Get permission details."""
    return _get_client().get(f"/rbac/permissions/{id}/")


@_op(authentik_read)
def list_initial_permissions(limit: int = 20):
    """List initial permissions."""
    return _paginated("/rbac/initial_permissions/", limit=limit)


@_op(authentik_read)
def show_initial_permission(id: int):
    """Get initial permission details."""
    return _get_client().get(f"/rbac/initial_permissions/{id}/")


@_op(authentik_read)
def list_permissions_assigned_by_roles(limit: int = 20):
    """List permissions assigned by roles."""
    return _paginated("/rbac/permissions/assigned_by_roles/", limit=limit)


@_op(authentik_read)
def list_permissions_roles(limit: int = 20):
    """List permission-role mappings."""
    return _paginated("/rbac/permissions/roles/", limit=limit)
