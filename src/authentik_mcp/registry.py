from typing import Any


class Group:
    """A named group of MCP tool operations exposed as a single meta-tool."""

    __slots__ = ("doc", "name")

    def __init__(self, name: str, doc: str):
        self.name = name
        self.doc = doc


ROOT = Group("root", "")


class _Unset:
    """Caller omitted a parameter, distinct from explicit null.

    Pydantic excludes omitted fields and generated transport drops `_UNSET`.
    Explicit None reaches nullable API fields, allowing a caller to clear them.
    """

    _instance: "_Unset | None" = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "_UNSET"

    def __bool__(self) -> bool:
        return False


# `Any` by design: tool signatures declare their public type (e.g. `str |
# None`) and use `_UNSET` as the default. If `_UNSET` were typed as `_Unset`,
# every `x: str | None = _UNSET` default would trip mypy's assignment check.
_UNSET: Any = _Unset()


def _op(group: Group):
    """Mark a function as an MCP tool in the given group."""

    def decorator(fn):
        if not fn.__doc__:
            raise RuntimeError(f"Tool function {fn.__name__!r} has no docstring")
        fn._mcp_group = group
        return fn

    return decorator
