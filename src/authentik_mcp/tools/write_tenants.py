from ..registry import _op
from .groups import authentik_write
from .helpers import _get_client, _ok


@_op(authentik_write)
def create_tenant(name: str, **kwargs):
    """Create a tenant. Required: name."""
    return _ok(_get_client().post("/tenants/tenants/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_tenant(id: str, **kwargs):
    """Update a tenant."""
    return _ok(_get_client().patch(f"/tenants/tenants/{id}/", json=kwargs))


@_op(authentik_write)
def create_tenant_admin_group(id: str):
    """Create a tenant admin group."""
    return _ok(_get_client().post(f"/tenants/tenants/{id}/create_admin_group/"))


@_op(authentik_write)
def create_tenant_recovery_key(id: str):
    """Create a tenant recovery key."""
    return _ok(_get_client().post(f"/tenants/tenants/{id}/create_recovery_key/"))


@_op(authentik_write)
def create_tenant_domain(domain: str, tenant: str, **kwargs):
    """Create a tenant domain. Required: domain, tenant."""
    return _ok(_get_client().post("/tenants/domains/", json={"domain": domain, "tenant": tenant, **kwargs}))


@_op(authentik_write)
def update_tenant_domain(id: str, **kwargs):
    """Update a tenant domain."""
    return _ok(_get_client().patch(f"/tenants/domains/{id}/", json=kwargs))
