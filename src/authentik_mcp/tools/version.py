from ..registry import ROOT, _op
from .helpers import _get_client


@_op(ROOT)
def authentik_version():
    """Get the Authentik MCP server version and service status."""
    from importlib.metadata import version

    try:
        service = _get_client().health()
    except Exception:
        service = {"status": "error"}
    return {"mcp": version("authentik-mcp"), "service": service}
