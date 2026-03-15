from ..registry import _op
from .groups import authentik_flows_read
from .helpers import SLIM_EVENT, _get_client, _paginated


@_op(authentik_flows_read)
def list_events(action: str | None = None, search: str | None = None, limit: int = 20):
    """List events (slim)."""
    p = {}
    if action is not None:
        p["action"] = action
    if search is not None:
        p["search"] = search
    return _paginated("/events/events/", p, limit, SLIM_EVENT)


@_op(authentik_flows_read)
def show_event(id: str):
    """Get full event details."""
    return _get_client().get(f"/events/events/{id}/")


@_op(authentik_flows_read)
def list_event_actions():
    """List event action types."""
    return _get_client().get("/events/events/actions/")


@_op(authentik_flows_read)
def list_event_per_month():
    """List events per month."""
    return _get_client().get("/events/events/per_month/")


@_op(authentik_flows_read)
def list_event_top_per_user():
    """List top events per user."""
    return _get_client().get("/events/events/top_per_user/")


@_op(authentik_flows_read)
def get_event_volume():
    """Get event volume."""
    return _get_client().get("/events/events/volume/")


# ── Notifications ────────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_notifications(limit: int = 20):
    """List notifications."""
    return _paginated("/events/notifications/", limit=limit)


@_op(authentik_flows_read)
def show_notification(id: str):
    """Get notification details."""
    return _get_client().get(f"/events/notifications/{id}/")


@_op(authentik_flows_read)
def list_notification_rules(limit: int = 20):
    """List notification rules."""
    return _paginated("/events/rules/", limit=limit)


@_op(authentik_flows_read)
def show_notification_rule(id: str):
    """Get notification rule details."""
    return _get_client().get(f"/events/rules/{id}/")


@_op(authentik_flows_read)
def list_notification_transports(limit: int = 20):
    """List notification transports."""
    return _paginated("/events/transports/", limit=limit)


@_op(authentik_flows_read)
def show_notification_transport(id: str):
    """Get notification transport details."""
    return _get_client().get(f"/events/transports/{id}/")


# ── System Tasks ─────────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_system_tasks():
    """List system tasks."""
    return _get_client().get("/events/system_tasks/")


@_op(authentik_flows_read)
def show_system_task(id: str):
    """Get system task details."""
    return _get_client().get(f"/events/system_tasks/{id}/")
