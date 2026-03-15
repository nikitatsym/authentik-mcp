from ..registry import _op
from .groups import authentik_write
from .helpers import _get_client, _ok


@_op(authentik_write)
def update_task_schedule(id: str, **kwargs):
    """Update a task schedule."""
    return _ok(_get_client().patch(f"/tasks/schedules/{id}/", json=kwargs))


@_op(authentik_write)
def send_task_schedule(id: str):
    """Send/trigger a task schedule."""
    return _ok(_get_client().post(f"/tasks/schedules/{id}/send/"))


@_op(authentik_write)
def retry_task(id: str):
    """Retry a task."""
    return _ok(_get_client().post(f"/tasks/tasks/{id}/retry/"))
