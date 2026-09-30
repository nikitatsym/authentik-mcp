"""Transport for generated operations; behavior overrides stay handwritten."""
import json
from contextlib import ExitStack
from pathlib import Path
from typing import Any
from urllib.parse import quote

from ..registry import _UNSET
from .helpers import _get_client, _ok, _slim_list, _verify_response
from .overrides import DIRECT_PROJECTIONS, LIST_PROJECTIONS, REQUEST_OVERRIDES


def invoke(operation_id: str, operation: dict, values: dict[str, Any]):
    path = operation["path"]
    query = {}
    body = {}
    for param in operation["parameters"]:
        value = values[param["name"]]
        if value is _UNSET:
            continue
        location = param["location"]
        if location == "path":
            path = path.replace("{" + param["wire"] + "}", quote(str(value), safe=""))
        elif location == "query":
            query[param["wire"]] = value
        elif location == "body":
            if param["wire"]:
                body[param["wire"]] = value
            else:
                body = value
        else:
            raise ValueError(f"Unsupported parameter location: {location}")
    if operation["paginated"]:
        limit = values["limit"]
        if "page_size" in query and limit is not _UNSET and query["page_size"] != limit:
            raise ValueError("Pass either limit or page_size, or give both the same value")
        query.setdefault("page_size", 20 if limit is _UNSET else limit)
    client = _get_client()
    kwargs: dict[str, Any] = {"params": query} if query else {}
    if operation["text_response"]:
        kwargs["text"] = True
    method = operation["method"]
    if operation_id in REQUEST_OVERRIDES:
        response = REQUEST_OVERRIDES[operation_id](client, operation | {"path": path}, body, query)
    elif operation["media"] == "multipart/form-data":
        with ExitStack() as stack:
            files = {}
            data = {}
            for param in operation["parameters"]:
                if param["location"] != "body" or param["wire"] not in body:
                    continue
                value = body[param["wire"]]
                if param["schema"].get("format") == "binary":
                    file = Path(value)
                    files[param["wire"]] = (file.name, stack.enter_context(file.open("rb")))
                else:
                    data[param["wire"]] = value if isinstance(value, str) else json.dumps(value)
            response = getattr(client, method)(path, files=files, data=data, **kwargs)
    elif operation["media"]:
        response = getattr(client, method)(path, json=body, **kwargs)
    else:
        response = getattr(client, method)(path, **kwargs)
    if operation_id == "core_applications_partial_update":
        _verify_response(body, response)
    if operation["paginated"]:
        response = response.get("results", response) if isinstance(response, dict) else response
        fields = LIST_PROJECTIONS.get(operation_id)
        if fields:
            response = _slim_list(response, fields)
    elif operation_id in DIRECT_PROJECTIONS:
        response = _slim_list(response, DIRECT_PROJECTIONS[operation_id])
    return _ok(response)
