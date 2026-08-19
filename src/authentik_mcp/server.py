"""Authentik MCP server — auto-discovery across the tools/ package, Pydantic
validation, schema introspection, dispatch.

v2.5 pattern (see mcp-server-v2.md): every @_op function gets a Pydantic params
model built from its signature at registration time. `params` is routed through
`model.model_validate()` — unknown keys are rejected (`extra='forbid'`), or
forwarded into `**kwargs` for ops that declare it (`extra='allow'`). Optional
params default to the `_UNSET` sentinel so "caller omitted" survives to the
function; an explicit `null` (for nullable fields the API clears) is preserved.
"""

import inspect
import re
import string
import types as _types
import typing
from typing import Annotated, Any

from mcp.server.mcpserver import MCPServer
from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    create_model,
    field_validator,
)

from . import tools as _tools_module
from .registry import _UNSET, ROOT, _Unset

mcp = MCPServer("authentik")

# ── State (populated by _register_tools) ──────────────────────────────

_group_ops: dict[str, dict] = {}  # {group_name: {PascalName: fn}}
_all_grouped: dict[str, str] = {}  # {PascalName: group_name}


def _to_pascal(name: str) -> str:
    return "".join(w.capitalize() for w in name.split("_"))


# ── Params model + validation ─────────────────────────────────────────


class _BoolCoercingBase(BaseModel):
    """Base for generated per-op models: loose str->bool coercion.

    The validator lives on a real class so `@classmethod` binds correctly
    under mypy - a classmethod on a local closure isn't a method of any
    class. Each generated model sets `extra` via `__cls_kwargs__` in
    `_build_params_model` (forbid, or allow for ops declaring **kwargs).
    """

    @field_validator("*", mode="before")
    @classmethod
    def _coerce_string_bool(cls, v: Any, info: Any) -> Any:
        if not isinstance(v, str):
            return v
        ann = cls.model_fields[info.field_name].annotation
        types_in_ann = (ann,) + typing.get_args(ann)
        if bool not in types_in_ann:
            return v
        lower = v.lower()
        if lower in ("true", "1", "yes"):
            return True
        if lower in ("false", "0", "no"):
            return False
        return v


def _build_params_model(fn) -> type[BaseModel]:
    """Build a Pydantic model from a function's signature.

    - Parameters without a default → required fields (missing → error).
    - Parameters defaulting to `_UNSET` → optional, via `default_factory` so
      Pydantic omits the default from the JSON Schema and `exclude_unset=True`
      can tell "omitted" from "passed".
    - `Annotated[T, Field(description=..., ...)]` is honored — description and
      constraints flow into help and the JSON Schema.
    - `**kwargs` in the signature → `extra='allow'` (extras forwarded into it);
      otherwise `extra='forbid'` (unknown keys rejected).
    - Loose string→bool coercion ("true"/"yes"/"1" / "false"/"no"/"0") on
      bool-typed fields, so MCP clients passing JSON-string booleans validate.
    """
    hints = getattr(fn, "_mcp_hints", None) or typing.get_type_hints(
        fn, include_extras=True
    )
    sig = inspect.signature(fn)
    fields: dict[str, Any] = {}
    has_var_keyword = False
    for name, p in sig.parameters.items():
        if p.kind is inspect.Parameter.VAR_KEYWORD:
            has_var_keyword = True
            continue
        ann = hints.get(name, Any)
        if p.default is inspect.Parameter.empty:
            field_spec: Any = ...
        elif isinstance(p.default, _Unset):
            field_spec = Field(default_factory=lambda: _UNSET)
        else:
            field_spec = p.default
        fields[name] = (ann, field_spec)
    extra = "allow" if has_var_keyword else "forbid"

    return create_model(
        f"{_to_pascal(fn.__name__)}Params",
        __base__=_BoolCoercingBase,
        __cls_kwargs__={"extra": extra},
        **fields,
    )


def _format_validation_error(err: ValidationError, op_name: str) -> str:
    """Pydantic ValidationError → readable multi-line message."""
    lines = [f"Invalid params for {op_name}:"]
    for e in err.errors():
        loc = ".".join(str(x) for x in e["loc"]) or "<root>"
        got = repr(e.get("input"))
        if len(got) > 80:
            got = got[:77] + "..."
        lines.append(f"  - {loc}: {e['msg']} (got {got})")
    lines.append(
        f"Call operation='schema', params={{'op': {op_name!r}}} for full parameter spec."
    )
    return "\n".join(lines)


def _coerce_call(fn, params: dict, op_name: str):
    """Validate `params` via the cached Pydantic model, then call `fn`.

    Caller-omitted fields (sentinel `_UNSET` defaults) are dropped via
    `exclude_unset=True` so the function sees its own default. Extras land in
    `model_extra` and are forwarded into `**kwargs`. Body fields nested under
    the var-keyword name get a friendly hint (Pydantic wouldn't flag it — the
    var-keyword name IS a valid key under `extra='allow'`).
    """
    sig_params = inspect.signature(fn).parameters
    var_kw = next(
        (p.name for p in sig_params.values()
         if p.kind is inspect.Parameter.VAR_KEYWORD),
        None,
    )
    if var_kw and var_kw in params and isinstance(params[var_kw], dict):
        raise ValueError(
            f"Do not nest fields under {var_kw!r}. Pass extra fields as "
            f"top-level params (e.g. group='<uuid>'), not {var_kw}={{...}}. "
            "See this op's docstring for the supported fields."
        )
    model: type[BaseModel] = fn._params_model
    try:
        validated = model.model_validate(params)
    except ValidationError as e:
        raise ValueError(_format_validation_error(e, op_name)) from None
    kwargs = validated.model_dump(exclude_unset=True)
    if validated.model_extra:
        kwargs.update(validated.model_extra)
    return fn(**kwargs)


# ── Type rendering for help ───────────────────────────────────────────


def _render_type(hint) -> str:
    """Compact human-readable rendering of a type hint for help text.

    Keeps `| None` so the optional/nullable distinction is visible alongside
    the `?` name marker.
    """
    if hint is None or hint is type(None):
        return "None"
    if typing.get_origin(hint) is Annotated:
        hint = typing.get_args(hint)[0]
    origin = typing.get_origin(hint)
    args = typing.get_args(hint)
    if origin in (typing.Union, _types.UnionType):
        return " | ".join(_render_type(a) for a in args)
    if origin is typing.Literal:
        return "|".join(a if isinstance(a, str) else repr(a) for a in args)
    if origin in (list, tuple, set):
        inner = ", ".join(_render_type(a) for a in args) or "Any"
        return f"{origin.__name__}[{inner}]"
    if origin is dict:
        return "dict"
    if hint is Any:
        return "any"
    return getattr(hint, "__name__", repr(hint))


def _render_ops_block(ops: dict) -> str:
    """Render a per-op signature block.

    Signature conventions (so the agent knows what the API accepts BEFORE the
    call, not after):
      - `name: T`        — required.
      - `name?: T`       — optional (caller may omit). Signalled by `_UNSET`.
      - `name: T | None` — nullable (caller must pass; may pass null).
      - `name: T = ...`  — optional with a concrete default.
      - `**name`         — accepts additional fields; pass them as TOP-LEVEL
                           params, not nested under a `name` key.

    Docstring body is indented under the signature; per-param
    `Field(description=...)` renders as an indented `name: description` bullet.
    """
    lines: list[str] = []
    for pascal_name in sorted(ops):
        fn = ops[pascal_name]
        sig = inspect.signature(fn)
        hints = getattr(fn, "_mcp_hints", None) or typing.get_type_hints(
            fn, include_extras=True
        )
        parts: list[str] = []
        descs: list[tuple[str, str]] = []
        for name, p in sig.parameters.items():
            if p.kind is inspect.Parameter.VAR_KEYWORD:
                parts.append(f"**{name}")
                continue
            hint = hints.get(name)
            type_str = _render_type(hint) if hint is not None else "any"
            if p.default is inspect.Parameter.empty:
                parts.append(f"{name}: {type_str}")
            elif isinstance(p.default, _Unset):
                parts.append(f"{name}?: {type_str}")
            elif p.default is None:
                parts.append(f"{name}: {type_str} = None")
            else:
                parts.append(f"{name}: {type_str} = {p.default!r}")
            if typing.get_origin(hint) is Annotated:
                for meta in typing.get_args(hint)[1:]:
                    desc = getattr(meta, "description", None)
                    if desc:
                        descs.append((name, desc))
        doc = inspect.getdoc(fn) or ""
        head, _, body = doc.partition("\n\n")
        head = " ".join(head.split())
        lines.append(f"  {pascal_name}({', '.join(parts)}) — {head}")
        for body_line in body.rstrip().splitlines():
            lines.append(f"    {body_line}" if body_line else "")
        for name, desc in descs:
            lines.append(f"    {name}: {desc}")
    return "\n".join(lines)


def _build_help(group_name: str, search: str | None = None) -> str:
    """Per-op signatures with types, docstring body, and per-param bullets.

    Without args: lists every op in the group. With `search='foo'`: restricts
    to ops whose name contains `foo` (case-insensitive); if nothing matches
    locally but the substring matches ops in OTHER groups, a cross-group hint
    is appended so the agent learns where to look.
    """
    ops = _group_ops[group_name]
    suffix = (
        " Call operation='schema', params={'op': 'OpName'} for the full JSON Schema."
    )

    if search:
        s = search.lower()

        def _hit(pn: str, fn) -> bool:
            # Match the op name and its docstring, so intent words (e.g.
            # "access", "gate") find ops named differently (e.g. PolicyBinding).
            return (
                s in pn.lower()
                or s in fn.__name__.lower()
                or s in (inspect.getdoc(fn) or "").lower()
            )

        matched = {pn: fn for pn, fn in ops.items() if _hit(pn, fn)}
        elsewhere: dict[str, list[str]] = {}
        for op_name, other_group in _all_grouped.items():
            if other_group == group_name:
                continue
            if _hit(op_name, _group_ops[other_group][op_name]):
                elsewhere.setdefault(other_group, []).append(op_name)
        if not matched:
            msg = f"No ops in {group_name} matching {search!r}."
            if elsewhere:
                msg += " Found in other groups: " + "; ".join(
                    f"{g}: {', '.join(sorted(names))}"
                    for g, names in sorted(elsewhere.items())
                )
            else:
                msg += " Call operation='help' (no params) to list all ops."
            return msg
        header = (
            f"{len(matched)} of {len(ops)} operations in {group_name} "
            f"matching {search!r}.{suffix}"
        )
        body = _render_ops_block(matched)
        if elsewhere:
            body += "\n\nAlso matching in other groups: " + "; ".join(
                f"{g}: {', '.join(sorted(names))}"
                for g, names in sorted(elsewhere.items())
            )
        return f"{header}\n{body}"

    header = f"{len(ops)} operations available.{suffix}"
    return f"{header}\n{_render_ops_block(ops)}"


def _build_schema(group_name: str, op_name: str | None) -> dict:
    """JSON Schema for one op (params={'op': 'X'}) or the op-name list (params={})."""
    ops = _group_ops[group_name]
    if op_name is None:
        return {
            "operations": sorted(ops.keys()),
            "hint": "Pass params={'op': '<OpName>'} to get the full JSON Schema.",
        }
    if op_name not in ops:
        raise ValueError(
            f"Unknown operation {op_name!r} in {group_name}. "
            f"Available: {sorted(ops)}"
        )
    fn = ops[op_name]
    schema = fn._params_model.model_json_schema()
    doc = inspect.getdoc(fn) or ""
    if doc:
        schema["description"] = doc
    return schema


def _dispatch(operation: str, group_name: str, params: dict):
    """Route an operation call: schema/help-aware, fails loud on anything wrong."""
    if operation == "schema":
        return _build_schema(group_name, params.get("op"))
    ops = _group_ops[group_name]
    if operation not in ops:
        if operation in _all_grouped:
            correct = _all_grouped[operation]
            raise ValueError(
                f"{operation!r} belongs to {correct!r}, not {group_name!r}. "
                f"Call {correct}(operation={operation!r}, ...) instead."
            )
        raise ValueError(
            f"Unknown operation {operation!r} in {group_name}. "
            "Use operation='help' to list or operation='schema' for details."
        )
    return _coerce_call(ops[operation], params, operation)


# ── Discovery + registration ──────────────────────────────────────────


_HARDCODED_OPERATION = re.compile(r"""\boperation\s*=\s*["'](?![$<])""")


def _render_group_doc(group_name: str, doc: str, ops: dict) -> str:
    """Resolve $OpName placeholders in a group doc against the registered operations.

    Examples are hand-written while operation names are derived from the @_op
    function names; rendering the names from the registry keeps the two from
    drifting apart, and an unresolved placeholder aborts startup. A hardcoded
    operation name is rejected outright; `<...>` stays available for deliberately
    generic placeholders.
    """
    if _HARDCODED_OPERATION.search(doc):
        raise RuntimeError(
            f"{group_name} doc hardcodes an operation name; use the $OpName form"
        )
    names = {name: name for name in ops} | {"help": "help", "schema": "schema"}
    try:
        return string.Template(doc).substitute(names)
    except (KeyError, ValueError) as exc:
        raise RuntimeError(
            f"{group_name} doc references an unknown operation placeholder: {exc}"
        ) from exc


def _collect_ops():
    """Collect @_op-decorated functions from all submodules of the tools package."""
    import importlib
    import pkgutil

    fns = {}
    for _importer, modname, _ispkg in pkgutil.walk_packages(
        _tools_module.__path__, _tools_module.__name__ + "."
    ):
        mod = importlib.import_module(modname)
        for name, fn in inspect.getmembers(mod, inspect.isfunction):
            if hasattr(fn, "_mcp_group"):
                fns[name] = fn
    return fns


def _register_tools():
    groups: dict[str, tuple] = {}
    for name, fn in _collect_ops().items():
        fn._mcp_hints = typing.get_type_hints(fn, include_extras=True)
        fn._params_model = _build_params_model(fn)
        group = fn._mcp_group
        if group is ROOT:
            mcp.tool()(fn)
        else:
            if group.name not in groups:
                groups[group.name] = (group, {})
            groups[group.name][1][name] = fn

    for group_name, (group, fns) in groups.items():
        ops = {_to_pascal(n): fn for n, fn in fns.items()}
        _group_ops[group_name] = ops
        doc = _render_group_doc(group_name, group.doc, ops)
        for pascal_name in ops:
            _all_grouped[pascal_name] = group_name

        def _make_tool(gname, gdoc):
            def tool_fn(operation: str, params: dict | None = None):
                params = params or {}
                if operation == "help":
                    return _build_help(gname, search=params.get("search"))
                return _dispatch(operation, gname, params)

            tool_fn.__name__ = gname
            tool_fn.__qualname__ = gname
            tool_fn.__doc__ = gdoc
            return tool_fn

        mcp.tool()(_make_tool(group_name, doc))


_register_tools()
