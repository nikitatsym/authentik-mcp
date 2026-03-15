from ..registry import _op
from .groups import authentik_write
from .helpers import _get_client, _ok


@_op(authentik_write)
def create_outpost(name: str, type: str, **kwargs):
    """Create an outpost. Required: name, type."""
    return _ok(_get_client().post("/outposts/instances/", json={"name": name, "type": type, **kwargs}))


@_op(authentik_write)
def update_outpost(id: str, **kwargs):
    """Update an outpost."""
    return _ok(_get_client().patch(f"/outposts/instances/{id}/", json=kwargs))


@_op(authentik_write)
def create_docker_service_connection(name: str, **kwargs):
    """Create a Docker service connection. Required: name."""
    return _ok(_get_client().post("/outposts/service_connections/docker/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_docker_service_connection(id: str, **kwargs):
    """Update a Docker service connection."""
    return _ok(_get_client().patch(f"/outposts/service_connections/docker/{id}/", json=kwargs))


@_op(authentik_write)
def create_kubernetes_service_connection(name: str, **kwargs):
    """Create a Kubernetes service connection. Required: name."""
    return _ok(_get_client().post("/outposts/service_connections/kubernetes/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_kubernetes_service_connection(id: str, **kwargs):
    """Update a Kubernetes service connection."""
    return _ok(_get_client().patch(f"/outposts/service_connections/kubernetes/{id}/", json=kwargs))
