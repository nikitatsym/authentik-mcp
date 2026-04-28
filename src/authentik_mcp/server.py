import inspect
import typing

from mcp.server.fastmcp import FastMCP

from . import tools as _tools_module
from .registry import ROOT

mcp = FastMCP("authentik")

# ── State (populated by _register_tools) ──────────────────────────────

_group_ops: dict[str, dict] = {}  # {group_name: {PascalName: fn}}
_all_grouped: dict[str, str] = {}  # {PascalName: group_name}


def _to_pascal(name: str) -> str:
    return "".join(w.capitalize() for w in name.split("_"))


def _parse_bool(val, default: bool) -> bool:
    if val is None:
        return default
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.lower() in ("1", "true", "yes")
    return bool(val)


def _is_bool_hint(hint) -> bool:
    if hint is bool:
        return True
    args = typing.get_args(hint)
    return bool in args if args else False


def _coerce_call(fn, params: dict):
    sig = inspect.signature(fn)
    hints = typing.get_type_hints(fn)
    kwargs = {}
    for name, param in sig.parameters.items():
        if name == "kwargs":
            continue
        if name not in params:
            continue
        val = params[name]
        hint = hints.get(name)
        if hint and _is_bool_hint(hint) and not isinstance(val, bool):
            default = param.default
            if default is inspect.Parameter.empty or default is None:
                default = False
            val = _parse_bool(val, default)
        kwargs[name] = val
    # Pass remaining params as kwargs for functions that accept **kwargs
    if any(
        p.kind == inspect.Parameter.VAR_KEYWORD
        for p in sig.parameters.values()
    ):
        for k, v in params.items():
            if k not in kwargs:
                kwargs[k] = v
    return fn(**kwargs)


def _build_help(group_name: str) -> str:
    """First docstring line is the op summary; the rest is indented under it.

    Non-type constraints (formats, conditional requirements, embedded-tag
    rules, opaque-string formats) live in the docstring body so callers learn
    from help, not from error messages.
    """
    ops = _group_ops[group_name]
    lines = []
    for pascal_name, fn in ops.items():
        sig = inspect.signature(fn)
        params = ", ".join(
            n for n, p in sig.parameters.items()
            if p.kind != inspect.Parameter.VAR_KEYWORD
        )
        doc = inspect.getdoc(fn) or ""
        head, _, body = doc.partition("\n\n")
        head = " ".join(head.split())
        lines.append(f"  {pascal_name}({params}) — {head}")
        for body_line in body.rstrip().splitlines():
            lines.append(f"    {body_line}" if body_line else "")
    return f"{len(ops)} operations available:\n" + "\n".join(lines)


def _dispatch(operation: str, group_name: str, params: dict):
    ops = _group_ops[group_name]
    if operation not in ops:
        if operation in _all_grouped:
            correct = _all_grouped[operation]
            return {
                "error": f"{operation} belongs to {correct}. "
                f"Use {correct}() instead."
            }
        return {
            "error": f"Unknown operation: {operation}. "
            'Use operation="help" to list available operations.'
        }
    fn = ops[operation]
    return _coerce_call(fn, params)


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
        for pascal_name in ops:
            _all_grouped[pascal_name] = group_name

        def _make_tool(gname, gdoc):
            def tool_fn(operation: str, params: dict = {}):
                if operation == "help":
                    return _build_help(gname)
                return _dispatch(operation, gname, params)

            tool_fn.__name__ = gname
            tool_fn.__qualname__ = gname
            tool_fn.__doc__ = gdoc
            return tool_fn

        mcp.tool()(_make_tool(group_name, group.doc))


_register_tools()
