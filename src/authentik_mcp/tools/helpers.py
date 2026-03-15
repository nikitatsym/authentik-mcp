from ..client import AuthentikClient

_client: AuthentikClient | None = None


def _get_client() -> AuthentikClient:
    global _client
    if _client is None:
        _client = AuthentikClient()
    return _client


def _ok(data):
    if data is None:
        return {"status": "ok"}
    return data


def _slim(item: dict, fields: set) -> dict:
    out = {}
    for f in fields:
        if "." in f:
            parts = f.split(".")
            val = item
            for p in parts:
                if isinstance(val, dict):
                    val = val.get(p)
                else:
                    val = None
                    break
            if val is not None:
                out[f] = val
        elif f in item:
            out[f] = item[f]
    return out


def _slim_list(items, fields: set) -> list:
    if not isinstance(items, list):
        return items
    return [_slim(i, fields) for i in items if isinstance(i, dict)]


def _paginated(
    path: str,
    params: dict | None = None,
    limit: int = 20,
    slim_fields: set | None = None,
):
    """GET a paginated endpoint, return results with optional slimming."""
    p = dict(params or {})
    p["page_size"] = limit
    data = _get_client().get(path, params=p)
    results = data.get("results", data) if isinstance(data, dict) else data
    if slim_fields and isinstance(results, list):
        return _slim_list(results, slim_fields)
    return results


# ── Slim field sets ──────────────────────────────────────────────────

SLIM_USER = {"pk", "username", "name", "email", "is_active", "path", "last_login"}
SLIM_GROUP = {"pk", "name", "parent_name", "num_pk", "is_superuser"}
SLIM_APP = {"pk", "name", "slug", "provider", "provider_obj.name", "meta_launch_url"}
SLIM_FLOW = {"pk", "name", "slug", "title", "designation"}
SLIM_EVENT = {"pk", "action", "app", "user", "created"}
SLIM_TOKEN = {"pk", "identifier", "intent", "user", "description", "expiring", "expires"}
SLIM_SESSION = {"pk", "user.pk", "user.username", "last_ip", "last_used", "expires"}
SLIM_BRAND = {"pk", "domain", "default", "branding_title"}
