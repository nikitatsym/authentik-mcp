#!/usr/bin/env python3
"""Check the public request contract independently of the generator resolver."""
from __future__ import annotations

import inspect
import json
from pathlib import Path

from authentik_mcp import _generated
from authentik_mcp.server import _group_ops

ROOT = Path(__file__).resolve().parent.parent


def dereference(document: dict, value: dict) -> dict:
    while "$ref" in value:
        result = document
        for segment in value["$ref"].removeprefix("#/").split("/"):
            result = result[segment]
        value = result | {k: v for k, v in value.items() if k != "$ref"}
    if "allOf" in value:
        combined = {}
        for child in value["allOf"]:
            combined.update(dereference(document, child))
        value = combined | {k: v for k, v in value.items() if k != "allOf"}
    return value


def check_contract() -> int:
    document = json.loads((ROOT / "codegen/schema-2026.8.3.json").read_text())
    expected_ids = set()
    for path, path_item in document["paths"].items():
        for method, op in path_item.items():
            if not isinstance(op, dict) or "operationId" not in op:
                continue
            if method == "put" and "patch" in path_item:
                continue
            operation_id = op["operationId"]
            expected_ids.add(operation_id)
            operation = _generated.OPERATIONS[operation_id]
            if operation["method"] != method or operation["path"] != path:
                raise ValueError(f"{operation_id}: generated HTTP target differs from schema")
            fn = _group_ops[operation["group"]][operation["name"]]
            expected = {}
            for raw in op.get("parameters", []):
                param = dereference(document, raw)
                expected[param["in"], param["name"]] = param.get("required", False)
            body_content = op.get("requestBody", {}).get("content", {})
            if body_content:
                body = dereference(document, next(iter(body_content.values()))["schema"])
                if "properties" not in body:
                    expected["body", ""] = op["requestBody"].get("required", False)
                else:
                    for name, raw in body["properties"].items():
                        if dereference(document, raw).get("readOnly"):
                            continue
                        expected["body", name] = name in body.get("required", [])
            actual = {}
            signature = inspect.signature(fn).parameters
            model = fn._params_model
            for param in operation["parameters"]:
                required = signature[param["name"]].default is inspect.Parameter.empty
                if model.model_fields[param["name"]].is_required() != required:
                    raise ValueError(f"{operation_id}.{param['name']}: validation and signature differ")
                actual[param["location"], param["wire"]] = required
            if actual != expected:
                raise ValueError(f"{operation_id}: required request parameters differ: {expected!r} != {actual!r}")
            if operation_id == "policies_bindings_partial_update":
                full = dereference(document, path_item["put"]["requestBody"]["content"]["application/json"]["schema"])
                if set(full["properties"]) != {name for location, name in expected if location == "body"}:
                    raise ValueError("Binding read-modify-write field set differs from PUT schema")
    if expected_ids != _generated.OPERATIONS.keys():
        raise ValueError("Generated surface differs from schema operation coverage")
    print(f"Verified public body/query/path requiredness for {len(expected_ids)} operations")
    return 0


if __name__ == "__main__":
    raise SystemExit(check_contract())
