from ..registry import _op
from .groups import authentik_read
from .helpers import _get_client, _paginated

# ── Outposts ─────────────────────────────────────────────────────────


@_op(authentik_read)
def list_outposts(limit: int = 20):
    """List outposts."""
    return _paginated("/outposts/instances/", limit=limit)


@_op(authentik_read)
def show_outpost(id: str):
    """Get outpost details."""
    return _get_client().get(f"/outposts/instances/{id}/")


@_op(authentik_read)
def get_outpost_health(id: str):
    """Get outpost health status."""
    return _get_client().get(f"/outposts/instances/{id}/health/")


@_op(authentik_read)
def get_outpost_default_settings():
    """Get outpost default settings."""
    return _get_client().get("/outposts/instances/default_settings/")


# ── Outpost Service Connections ──────────────────────────────────────


@_op(authentik_read)
def list_outpost_service_connections(limit: int = 20):
    """List all outpost service connections."""
    return _paginated("/outposts/service_connections/all/", limit=limit)


@_op(authentik_read)
def show_outpost_service_connection(id: str):
    """Get service connection details."""
    return _get_client().get(f"/outposts/service_connections/all/{id}/")


@_op(authentik_read)
def get_service_connection_state(id: str):
    """Get service connection state."""
    return _get_client().get(f"/outposts/service_connections/all/{id}/state/")


@_op(authentik_read)
def list_service_connection_types():
    """List service connection types."""
    return _get_client().get("/outposts/service_connections/all/types/")


@_op(authentik_read)
def list_docker_service_connections(limit: int = 20):
    """List Docker service connections."""
    return _paginated("/outposts/service_connections/docker/", limit=limit)


@_op(authentik_read)
def show_docker_service_connection(id: str):
    """Get Docker service connection details."""
    return _get_client().get(f"/outposts/service_connections/docker/{id}/")


@_op(authentik_read)
def list_kubernetes_service_connections(limit: int = 20):
    """List Kubernetes service connections."""
    return _paginated("/outposts/service_connections/kubernetes/", limit=limit)


@_op(authentik_read)
def show_kubernetes_service_connection(id: str):
    """Get Kubernetes service connection details."""
    return _get_client().get(f"/outposts/service_connections/kubernetes/{id}/")


# ── Outpost Protocol Lists ───────────────────────────────────────────


@_op(authentik_read)
def list_outpost_ldap(id: str | None = None, limit: int = 20):
    """List outpost LDAP configs."""
    p = {}
    if id is not None:
        p["id"] = id
    return _paginated("/outposts/ldap/", p, limit)


@_op(authentik_read)
def list_outpost_proxy(id: str | None = None, limit: int = 20):
    """List outpost proxy configs."""
    p = {}
    if id is not None:
        p["id"] = id
    return _paginated("/outposts/proxy/", p, limit)


@_op(authentik_read)
def list_outpost_radius(id: str | None = None, limit: int = 20):
    """List outpost Radius configs."""
    p = {}
    if id is not None:
        p["id"] = id
    return _paginated("/outposts/radius/", p, limit)
