from ..registry import _op
from .groups import authentik_flows_write
from .helpers import _get_client, _ok


@_op(authentik_flows_write)
def create_event(action: str, **kwargs):
    """Create an event. Required: action."""
    return _ok(_get_client().post("/events/events/", json={"action": action, **kwargs}))


@_op(authentik_flows_write)
def update_event(id: str, **kwargs):
    """Update an event."""
    return _ok(_get_client().patch(f"/events/events/{id}/", json=kwargs))


@_op(authentik_flows_write)
def export_events():
    """Export events."""
    return _ok(_get_client().post("/events/events/export/"))


@_op(authentik_flows_write)
def update_notification(id: str, **kwargs):
    """Update a notification."""
    return _ok(_get_client().patch(f"/events/notifications/{id}/", json=kwargs))


@_op(authentik_flows_write)
def mark_all_notifications_seen():
    """Mark all notifications as seen."""
    return _ok(_get_client().post("/events/notifications/mark_all_seen/"))


@_op(authentik_flows_write)
def create_notification_rule(name: str, **kwargs):
    """Create a notification rule. Required: name."""
    return _ok(_get_client().post("/events/rules/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_notification_rule(id: str, **kwargs):
    """Update a notification rule."""
    return _ok(_get_client().patch(f"/events/rules/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_notification_transport(name: str, **kwargs):
    """Create a notification transport. Required: name."""
    return _ok(_get_client().post("/events/transports/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_notification_transport(id: str, **kwargs):
    """Update a notification transport."""
    return _ok(_get_client().patch(f"/events/transports/{id}/", json=kwargs))


@_op(authentik_flows_write)
def test_notification_transport(id: str):
    """Test a notification transport."""
    return _ok(_get_client().post(f"/events/transports/{id}/test/"))
