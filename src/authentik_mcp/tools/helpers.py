from typing import Any

from ..client import AuthentikClient
from ..registry import _UNSET

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


def _body(
    local_vars: dict,
    exclude=(),
    rename: dict | None = None,
    keep_null=(),
) -> dict:
    """Build a JSON body from a function's locals(), dropping omitted fields.

    Drops keys whose value is `_UNSET` (caller omitted) or `None` (unless the
    key is listed in `keep_null`, for nullable fields the API clears on null).
    `exclude` drops keys outright (e.g. path params); `rename` maps Python
    parameter names to API field names. A `**kwargs` dict in locals() is
    merged in (extras passed by the caller), under the same drop rules.

    Usage:
        return _ok(_get_client().post("/x/", json=_body(locals())))
        return _ok(_get_client().patch(f"/x/{id}/", json=_body(
            locals(), exclude=("id",), keep_null=("group",))))
    """
    excl = set(exclude)
    rmap = rename or {}
    keep = set(keep_null)
    out: dict = {}

    def _add(k, v):
        if k in excl:
            return
        if v is _UNSET:
            return
        if v is None and k not in keep:
            return
        out[rmap.get(k, k)] = v

    for k, v in local_vars.items():
        if k == "kwargs":
            continue
        _add(k, v)
    extra = local_vars.get("kwargs")
    if isinstance(extra, dict):
        for k, v in extra.items():
            _add(k, v)
    return out


def _verify_response(sent: dict, received: dict, drops: dict | None = None) -> None:
    """Raise if the API silently dropped a sent field (sent non-null → null in response).

    drops: optional {field: hint} for known-drop fields that need a dedicated endpoint.
    """
    if not isinstance(received, dict):
        return
    drops = drops or {}
    for key, sent_val in sent.items():
        if sent_val is None or sent_val == "":
            continue
        if key not in received:
            continue
        if received[key] is None:
            hint = drops.get(key, "")
            raise ValueError(
                f"API silently dropped {key!r}: sent {sent_val!r}, got null. {hint}".strip()
            )


def _slim(item: dict, fields: set) -> dict:
    out = {}
    for f in fields:
        if "." in f:
            parts = f.split(".")
            val: Any = item
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

# Core
SLIM_USER = {"pk", "username", "name", "email", "is_active", "path", "last_login"}
SLIM_GROUP = {"pk", "name", "parent_name", "num_pk", "is_superuser"}
SLIM_APP = {"pk", "name", "slug", "provider", "provider_obj.name", "meta_launch_url"}
SLIM_TOKEN = {"pk", "identifier", "intent", "user", "description", "expiring", "expires"}
SLIM_SESSION = {"uuid", "user", "last_ip", "last_used", "expires", "geo_ip.country", "geo_ip.city"}
SLIM_BRAND = {"brand_uuid", "domain", "default", "branding_title"}
SLIM_USER_CONSENT = {"pk", "user.pk", "user.username", "application.slug", "application.name", "expires", "permissions"}
SLIM_APP_ENTITLEMENT = {"pbm_uuid", "name", "app"}

# Flows
SLIM_FLOW = {"pk", "name", "slug", "title", "designation"}
SLIM_FLOW_BINDING = {"pk", "target", "stage", "order", "evaluate_on_plan", "re_evaluate_policies"}

# Policies
SLIM_POLICY = {"pk", "name", "component", "execution_logging", "bound_to"}
SLIM_POLICY_BINDING = {"pk", "policy", "group", "user", "target", "negate", "enabled", "order", "timeout"}
SLIM_REPUTATION_SCORE = {"pk", "identifier", "ip", "score", "updated"}

# Stages
SLIM_STAGE = {"pk", "name", "component", "verbose_name"}

# Sources
SLIM_SOURCE = {"pk", "name", "slug", "enabled", "component", "verbose_name"}
SLIM_SOURCE_CONNECTION = {"pk", "source", "identifier"}

# Providers
SLIM_PROVIDER = {"pk", "name", "component", "authorization_flow", "assigned_application_slug", "assigned_application_name"}

# Property mappings
SLIM_PROPERTY_MAPPING = {"pk", "name", "managed", "component", "verbose_name"}

# Events
SLIM_EVENT = {"pk", "action", "app", "user", "created"}
SLIM_NOTIFICATION = {"pk", "severity", "body", "created", "seen"}
SLIM_NOTIFICATION_RULE = {"pk", "name", "transports", "severity", "destination_group"}
SLIM_NOTIFICATION_TRANSPORT = {"pk", "name", "mode"}

# Crypto
SLIM_CERTIFICATE = {"pk", "name", "fingerprint_sha256", "cert_expiry", "managed"}

# Outposts
SLIM_OUTPOST = {"pk", "name", "type", "providers", "service_connection", "managed"}
SLIM_SERVICE_CONNECTION = {"pk", "name", "component", "local"}

# RBAC
SLIM_ROLE = {"pk", "name"}
SLIM_PERMISSION = {"id", "name", "codename", "model", "app_label"}

# Authenticator devices
SLIM_AUTHENTICATOR_DEVICE = {"pk", "name", "user.pk", "user.username"}

# OAuth2 tokens
SLIM_OAUTH2_TOKEN = {"pk", "provider.pk", "provider.name", "user.pk", "user.username", "is_expired", "expires", "scope", "revoked"}

# Managed
SLIM_BLUEPRINT = {"pk", "name", "path", "enabled", "status"}

# Tasks
SLIM_TASK = {"uid", "state", "description", "mtime"}

# Enterprise / Tenants
SLIM_LICENSE = {"pk", "name", "expiry", "internal_users", "external_users"}
SLIM_TENANT = {"pk", "name", "schema_name", "ready"}
SLIM_TENANT_DOMAIN = {"pk", "domain", "is_primary", "tenant"}

# RAC
SLIM_RAC_ENDPOINT = {"pk", "name", "protocol", "host", "provider"}
SLIM_RAC_TOKEN = {"pk", "provider", "endpoint", "user"}

# Endpoints
SLIM_ENDPOINT = {"pk", "name"}

# Misc
SLIM_EXPORT = {"pk", "name", "created"}
SLIM_SSF_STREAM = {"pk", "provider", "delivery_method", "endpoint_url"}
SLIM_VERSION_HISTORY = {"id", "version", "build", "timestamp"}
SLIM_ADMIN_FILE = {"pk", "name", "path"}
