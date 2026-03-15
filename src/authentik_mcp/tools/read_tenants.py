from ..registry import _op
from .groups import authentik_read
from .helpers import _get_client, _paginated


@_op(authentik_read)
def list_tenants(limit: int = 20):
    """List tenants."""
    return _paginated("/tenants/tenants/", limit=limit)


@_op(authentik_read)
def show_tenant(id: str):
    """Get tenant details."""
    return _get_client().get(f"/tenants/tenants/{id}/")


@_op(authentik_read)
def list_tenant_domains(limit: int = 20):
    """List tenant domains."""
    return _paginated("/tenants/domains/", limit=limit)


@_op(authentik_read)
def show_tenant_domain(id: str):
    """Get tenant domain details."""
    return _get_client().get(f"/tenants/domains/{id}/")
