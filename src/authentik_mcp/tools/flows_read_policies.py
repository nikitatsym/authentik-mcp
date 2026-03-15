from ..registry import _op
from .groups import authentik_flows_read
from .helpers import _get_client, _paginated

# ── Policies — All ───────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_policies(limit: int = 20):
    """List all policies."""
    return _paginated("/policies/all/", limit=limit)


@_op(authentik_flows_read)
def show_policy(id: str):
    """Get policy details."""
    return _get_client().get(f"/policies/all/{id}/")


@_op(authentik_flows_read)
def list_policy_types():
    """List policy types."""
    return _get_client().get("/policies/all/types/")


@_op(authentik_flows_read)
def list_policy_bindings(limit: int = 20):
    """List policy bindings."""
    return _paginated("/policies/bindings/", limit=limit)


@_op(authentik_flows_read)
def show_policy_binding(id: str):
    """Get policy binding details."""
    return _get_client().get(f"/policies/bindings/{id}/")


# ── Policies — Expression ────────────────────────────────────────────


@_op(authentik_flows_read)
def list_expression_policies(limit: int = 20):
    """List expression policies."""
    return _paginated("/policies/expression/", limit=limit)


@_op(authentik_flows_read)
def show_expression_policy(id: str):
    """Get expression policy details."""
    return _get_client().get(f"/policies/expression/{id}/")


# ── Policies — Password ──────────────────────────────────────────────


@_op(authentik_flows_read)
def list_password_policies(limit: int = 20):
    """List password policies."""
    return _paginated("/policies/password/", limit=limit)


@_op(authentik_flows_read)
def show_password_policy(id: str):
    """Get password policy details."""
    return _get_client().get(f"/policies/password/{id}/")


@_op(authentik_flows_read)
def list_password_expiry_policies(limit: int = 20):
    """List password expiry policies."""
    return _paginated("/policies/password_expiry/", limit=limit)


@_op(authentik_flows_read)
def show_password_expiry_policy(id: str):
    """Get password expiry policy details."""
    return _get_client().get(f"/policies/password_expiry/{id}/")


@_op(authentik_flows_read)
def list_unique_password_policies(limit: int = 20):
    """List unique password policies."""
    return _paginated("/policies/unique_password/", limit=limit)


@_op(authentik_flows_read)
def show_unique_password_policy(id: str):
    """Get unique password policy details."""
    return _get_client().get(f"/policies/unique_password/{id}/")


# ── Policies — Reputation ────────────────────────────────────────────


@_op(authentik_flows_read)
def list_reputation_policies(limit: int = 20):
    """List reputation policies."""
    return _paginated("/policies/reputation/", limit=limit)


@_op(authentik_flows_read)
def show_reputation_policy(id: str):
    """Get reputation policy details."""
    return _get_client().get(f"/policies/reputation/{id}/")


@_op(authentik_flows_read)
def list_reputation_scores(limit: int = 20):
    """List reputation scores."""
    return _paginated("/policies/reputation/scores/", limit=limit)


@_op(authentik_flows_read)
def show_reputation_score(id: int):
    """Get reputation score details."""
    return _get_client().get(f"/policies/reputation/scores/{id}/")


# ── Policies — Event Matcher ─────────────────────────────────────────


@_op(authentik_flows_read)
def list_event_matcher_policies(limit: int = 20):
    """List event matcher policies."""
    return _paginated("/policies/event_matcher/", limit=limit)


@_op(authentik_flows_read)
def show_event_matcher_policy(id: str):
    """Get event matcher policy details."""
    return _get_client().get(f"/policies/event_matcher/{id}/")


# ── Policies — GeoIP ─────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_geoip_policies(limit: int = 20):
    """List GeoIP policies."""
    return _paginated("/policies/geoip/", limit=limit)


@_op(authentik_flows_read)
def show_geoip_policy(id: str):
    """Get GeoIP policy details."""
    return _get_client().get(f"/policies/geoip/{id}/")


# ── Policies — Dummy ─────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_dummy_policies(limit: int = 20):
    """List dummy policies."""
    return _paginated("/policies/dummy/", limit=limit)


@_op(authentik_flows_read)
def show_dummy_policy(id: str):
    """Get dummy policy details."""
    return _get_client().get(f"/policies/dummy/{id}/")
