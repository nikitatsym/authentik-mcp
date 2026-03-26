from ..registry import ROOT, _op
from .helpers import _get_client


@_op(ROOT)
def authentik_version():
    """Get the Authentik MCP server version and service status."""
    from importlib.metadata import version

    service = {}
    try:
        service.update(_get_client().health())
    except Exception:
        service["status"] = "error"
    try:
        service.update(_get_client().get("/admin/version/"))
    except Exception:
        pass
    return {"mcp": version("authentik-mcp"), "service": service}
