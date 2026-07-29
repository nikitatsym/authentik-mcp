from ..registry import ROOT, _op
from .helpers import _get_client


@_op(ROOT)
def authentik_version():
    """Get the Authentik MCP server version and service status."""
    from importlib.metadata import version

    service = {}
    try:
        service.update(_get_client().health())
    except Exception as e:  # noqa: BLE001 - reporting reachability is this tool's whole contract
        service["status"] = "error"
        service["error"] = f"{type(e).__name__}: {e}"
    try:
        service.update(_get_client().get("/admin/version/"))
    except Exception as e:  # noqa: BLE001 - admin-only endpoint; still report status without it
        service["version_error"] = f"{type(e).__name__}: {e}"
    return {"mcp": version("authentik-mcp"), "service": service}
