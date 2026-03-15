from ..registry import _op
from .groups import authentik_read
from .helpers import _get_client, _paginated


@_op(authentik_read)
def list_task_schedules(limit: int = 20):
    """List task schedules."""
    return _paginated("/tasks/schedules/", limit=limit)


@_op(authentik_read)
def show_task_schedule(id: str):
    """Get task schedule details."""
    return _get_client().get(f"/tasks/schedules/{id}/")


@_op(authentik_read)
def list_tasks(limit: int = 20):
    """List tasks."""
    return _paginated("/tasks/tasks/", limit=limit)


@_op(authentik_read)
def show_task(id: str):
    """Get task details."""
    return _get_client().get(f"/tasks/tasks/{id}/")


@_op(authentik_read)
def get_task_status(id: str):
    """Get task status."""
    return _get_client().get(f"/tasks/tasks/{id}/status/")


@_op(authentik_read)
def list_workers():
    """List task workers."""
    return _get_client().get("/tasks/workers/")
