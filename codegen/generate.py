#!/usr/bin/env python3
"""Generate every Authentik 2026.8.3 operation from the vendored schema."""
from __future__ import annotations

import argparse
import hashlib
import json
import keyword
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "codegen/schema-2026.8.3.json"
TABLE_DIR = ROOT / "codegen/operations"
OUTPUT = ROOT / "src/authentik_mcp/_generated.py"
GROUPS = {
    "authentik_read", "authentik_write", "authentik_delete",
    "authentik_flows_read", "authentik_flows_write", "authentik_admin",
}
METHODS = {"get", "post", "put", "patch", "delete", "head", "options"}
MODEL_DEFINITIONS: dict[str, dict] = {}


def resolve(schema: dict, value: dict) -> dict:
    if "$ref" in value:
        ref = value["$ref"]
        if not ref.startswith("#/"):
            raise ValueError(f"External schema reference: {ref}")
        target = schema
        for part in ref[2:].split("/"):
            target = target[part.replace("~1", "/").replace("~0", "~")]
        return resolve(schema, target) | {k: v for k, v in value.items() if k != "$ref"}
    if "allOf" in value:
        merged: dict[str, Any] = {}
        for child in value["allOf"]:
            resolved = resolve(schema, child)
            for key, item in resolved.items():
                if key == "properties":
                    merged.setdefault(key, {}).update(item)
                elif key == "required":
                    merged[key] = list(dict.fromkeys(merged.get(key, []) + item))
                else:
                    merged[key] = item
        return merged | {k: v for k, v in value.items() if k != "allOf"}
    return value


def operations(schema: dict) -> dict[str, tuple[str, str, dict]]:
    found = {}
    for path, item in schema["paths"].items():
        for method, op in item.items():
            if method not in METHODS:
                continue
            opid = op["operationId"]
            if opid in found:
                raise ValueError(f"Duplicate schema operationId: {opid}")
            found[opid] = method, path, op
    return found


def load_table(schema: dict, area: str | None = None) -> dict[str, dict]:
    ops = operations(schema)
    rows = {}
    names = {}
    for file in sorted(TABLE_DIR.glob("*.json")):
        for row in json.loads(file.read_text()):
            opid = row["operationId"]
            if opid in rows:
                raise ValueError(f"Duplicate table operationId: {opid}")
            if opid not in ops:
                raise ValueError(f"Unknown operationId in {file.name}: {opid}")
            if ops[opid][1].split("/")[1] != file.stem:
                raise ValueError(f"Operation {opid} belongs in another API-area table")
            for field in ("name", "description", "group"):
                if not isinstance(row.get(field), str) or not row[field].strip():
                    raise ValueError(f"{opid}: empty {field}")
                if not row[field].isascii():
                    raise ValueError(f"{opid}: {field} must be ASCII")
            if not re.fullmatch(r"[A-Z][A-Za-z0-9]*", row["name"]):
                raise ValueError(f"{opid}: invalid public name {row['name']!r}")
            if row["group"] not in GROUPS:
                raise ValueError(f"{opid}: unknown group {row['group']!r}")
            if row["name"] in names:
                raise ValueError(f"Public name collision: {row['name']} ({names[row['name']]}, {opid})")
            names[row["name"]] = opid
            if not isinstance(row.get("exposed"), bool):
                raise TypeError(f"{opid}: exposed must be a boolean")
            method, path, _ = ops[opid]
            excluded = method == "put" and "patch" in schema["paths"][path]
            if row["exposed"] == excluded:
                raise ValueError(f"{opid}: exposed must be {not excluded}; only PUT with PATCH is excluded")
            rows[opid] = row
    missing = ops.keys() - rows.keys()
    if missing:
        raise ValueError(f"Schema operations missing table rows: {sorted(missing)}")
    if area and not any(path.split("/")[1] == area for _, path, _ in ops.values()):
        raise ValueError(f"Unknown API area: {area}")
    return rows


def python_name(name: str) -> str:
    return name + "_" if keyword.iskeyword(name) else name


def parameter_contract(schema: dict, op: dict) -> tuple[list[dict], str]:
    result = []
    taken = set()
    for raw in op.get("parameters", []):
        param = resolve(schema, raw)
        name = python_name(param["name"])
        if name in taken:
            name = param["in"] + "_" + name
        taken.add(name)
        result.append({
            "name": name, "wire": param["name"], "location": param["in"],
            "required": param.get("required", False),
            "schema": resolve(schema, param["schema"]) | ({"description": param["description"]} if param.get("description") else {}),
        })
    content = op.get("requestBody", {}).get("content", {})
    media = "application/json" if "application/json" in content else next(iter(content), "")
    if content:
        body = resolve(schema, content[media]["schema"])
        if "properties" not in body:
            result.append({"name": "body", "wire": "", "location": "body", "required": op["requestBody"].get("required", False), "schema": body})
        else:
            for wire, raw in body["properties"].items():
                value = resolve(schema, raw)
                if value.get("readOnly"):
                    continue
                name = python_name(wire)
                if name in taken:
                    name = "body_" + name
                taken.add(name)
                result.append({"name": name, "wire": wire, "location": "body", "required": wire in body.get("required", []), "schema": value})
    return result, media


def annotation(schema: dict, value: dict, stack: tuple[str, ...] = ()) -> str:
    if "$ref" in value:
        ref = value["$ref"]
        if ref in stack:
            return "dict[str, Any]"
        return annotation(schema, resolve(schema, value), stack + (ref,))
    value = resolve(schema, value)
    if "enum" in value:
        values = [repr(v) for v in value["enum"] if v is not None]
        kind = "Literal[" + ", ".join(values) + "]" if values else "None"
    elif "oneOf" in value or "anyOf" in value:
        kinds = [annotation(schema, v, stack) for v in value.get("oneOf", value.get("anyOf", []))]
        kind = " | ".join(dict.fromkeys(kinds))
    elif value.get("type") == "array":
        kind = f"list[{annotation(schema, value.get('items', {}), stack)}]"
    elif value.get("type") == "object" or "properties" in value:
        if value.get("properties"):
            digest = hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()[:12]
            kind = "RequestObject" + digest
            MODEL_DEFINITIONS.setdefault(kind, value)
        else:
            kind = "dict[str, Any]"
    else:
        kind = {"string": "str", "integer": "int", "number": "float", "boolean": "bool", "null": "None"}.get(value.get("type"), "Any")
    if value.get("nullable") and kind not in {"Any", "None"}:
        kind += " | None"
    metadata = {}
    if value.get("description"):
        metadata["description"] = value["description"]
    if value.get("format"):
        metadata["json_schema_extra"] = {"format": "file-path" if value["format"] == "binary" else value["format"]}
        if value["format"] == "binary":
            metadata["description"] = "Server-local file path, uploaded as multipart binary data."
    for source, target in (("minLength", "min_length"), ("maxLength", "max_length"), ("minimum", "ge"), ("maximum", "le"), ("pattern", "pattern"), ("minItems", "min_length"), ("maxItems", "max_length")):
        if source in value:
            metadata[target] = value[source]
    if metadata:
        fields = ", ".join(f"{key}={item!r}" for key, item in metadata.items())
        return f"Annotated[{kind}, Field({fields})]"
    return kind


def model_definitions(schema: dict) -> list[str]:
    lines = []
    emitted = set()
    while pending := MODEL_DEFINITIONS.keys() - emitted:
        for name in sorted(pending):
            value = MODEL_DEFINITIONS[name]
            additional = value.get("additionalProperties", False)
            extra = "allow" if additional is not False else "forbid"
            lines += [f"class {name}(BaseModel):", f"    model_config = ConfigDict(extra={extra!r})"]
            for wire, raw in value["properties"].items():
                field = resolve(schema, raw)
                if field.get("readOnly"):
                    continue
                param = python_name(wire)
                metadata = []
                if param != wire:
                    metadata.append(f"alias={wire!r}")
                if wire not in value.get("required", []):
                    metadata.append("default_factory=lambda: _UNSET")
                default = " = Field(" + ", ".join(metadata) + ")" if metadata else ""
                lines.append(f"    {param}: {annotation(schema, field)}{default}")
            lines.append("")
            emitted.add(name)
    lines += [f"{name}.model_rebuild()" for name in sorted(emitted)] + [""]
    return lines


def generate(schema: dict, table: dict[str, dict]) -> str:
    MODEL_DEFINITIONS.clear()
    lines = []
    for opid, (method, path, op) in sorted(operations(schema).items()):
        row = table[opid]
        if not row["exposed"]:
            continue
        params, media = parameter_contract(schema, op)
        response = next((v for k, v in op.get("responses", {}).items() if k.startswith("2")), {})
        response_schema = resolve(schema, response.get("content", {}).get("application/json", {}).get("schema", {}))
        paginated = method == "get" and "page_size" in {p["wire"] for p in params} and "results" in response_schema.get("properties", {})
        signature = sorted(params, key=lambda p: not p["required"])
        lines += [f"def {row['name']}(", "    *,"] if signature or paginated else [f"def {row['name']}():"]
        for param in signature:
            default = "" if param["required"] else " = _UNSET"
            lines.append(f"    {param['name']}: {annotation(schema, param['schema'])}{default},")
        if paginated:
            lines.append("    limit: Annotated[int, Field(ge=1, description='Maximum page size; defaults to 20 when page_size is omitted.')] = _UNSET,")
        if signature or paginated:
            lines.append("):")
        lines += [f"    {row['description']!r}", f"    return invoke({opid!r}, OPERATIONS[{opid!r}], locals())", ""]
        descriptor = {
            "name": row["name"], "description": row["description"], "group": row["group"],
            "method": method, "path": path, "media": media, "paginated": paginated,
            "text_response": response_schema.get("format") == "binary",
            "parameters": params,
        }
        lines += [f"OPERATIONS[{opid!r}] = {descriptor!r}", ""]
    header = [
        "# GENERATED by codegen/generate.py; DO NOT EDIT.",
        "from __future__ import annotations", "", "from typing import Annotated, Any, Literal", "",
        "from pydantic import BaseModel, ConfigDict, Field", "",
        "from .registry import _UNSET", "from .tools.runtime import invoke", "",
        "OPERATIONS: dict[str, dict] = {}", "",
    ]
    return "\n".join(header + model_definitions(schema) + lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--area", help="Validate this review slice without modifying generated output")
    args = parser.parse_args()
    schema = json.loads(SCHEMA_PATH.read_text())
    if schema["info"]["version"] != "2026.8.3":
        raise ValueError("Vendored schema must be Authentik 2026.8.3")
    table = load_table(schema, args.area)
    if args.area:
        count = sum(opid.startswith(args.area + "_") for opid in table)
        print(f"Validated {args.area}: {count} table rows; complete coverage and unique names")
        return 0
    output = generate(schema, table)
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text() != output:
            raise ValueError("Generated operations differ; run uv run python codegen/generate.py")
        print(f"Validated {len(table)} schema operations; generated output is current")
    else:
        OUTPUT.write_text(output)
        print(f"Generated {sum(row['exposed'] for row in table.values())} operations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
