"""Conformance check: every hand-written API call matches authentik's OpenAPI schema.

authentik is Django REST Framework, which silently ignores query params it does
not recognise: a misspelled filter name still returns 200 and simply never
applies. Unknown body fields are dropped just as quietly on serializers that
accept extras. Neither the type system nor the integration suite can see that
class of typo, so this test reads every registered op off its own AST and
asserts each call's method, path, query-param names and body-field names
against the live instance's OpenAPI 3 document at `/api/v3/schema/`.

Ops that forward `**kwargs` onto the wire stay checkable: the field names they
spell out themselves are verified, while the caller-supplied extras are
unknowable statically and are simply not checked. Same rule one level down: an
op that hides one call behind an expression the extractor cannot read still has
its other calls checked, and an unreadable payload does not stop that call's
method and path from being checked.
"""

from __future__ import annotations

import ast
import functools
import inspect
import re
import textwrap
import typing
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Any, Literal, TypeGuard

import httpx
import pytest

from authentik_mcp.server import _collect_ops

pytestmark = pytest.mark.integration

# Ops with a shape the extractor below cannot read, mapped to the exact reasons
# it reports. Waiving an op waives only what the reader could not see: its other
# calls, and the method and path of the offending call, are still checked. ONLY
# code shapes belong here - never a name mismatch, which is the whole point of
# this test. The reasons are matched exactly, so a second unreadable shape in an
# already-waived op still surfaces.
UNANALYZABLE_OK: dict[str, tuple[str, ...]] = {
    # health() probes /-/health/live/, outside the API root and so outside the
    # schema. The op's /admin/version/ GET is read and checked as usual.
    "authentik_version": ("unknown client method 'health'",),
    # The PUT body is a read-modify-write of the fetched binding, so its keys
    # come from the response schema: PolicyBinding minus pk and the *_obj
    # expansions is exactly PolicyBindingRequest. Both calls' paths and methods
    # are still checked.
    "update_policy_binding": (
        "body.update() mutates the payload",
        "dict built from a DictComp, not a literal",
    ),
}

# Ops with no wire call of their own: they only drive other registered ops,
# whose calls are checked in their own right.
NO_WIRE_CALL_OK: frozenset[str] = frozenset()

@dataclass(frozen=True)
class _Unserved:
    """A call the pinned live schema has no endpoint for, and why that is fine."""

    reason: str
    call: str  # "METHOD /path", as the extractor renders it


def _unserved(reason: str, entries: dict[str, str]) -> dict[str, _Unserved]:
    return {op: _Unserved(reason, call) for op, call in entries.items()}


# Endpoints authentik grew after the pinned test image (tests/docker-compose.yml).
# Each call below was found in the published schema.yml of the release named in
# its reason, so it is verified, just not here. Recording the exact method and
# path is what keeps that verification honest: the test asserts these are
# precisely the calls the pinned instance cannot serve, so retargeting one at a
# typo fails just like any other op, and a pin bump that starts serving one fails
# until it is dropped from the table.
SPEC_GAPS: dict[str, _Unserved] = {
    **_unserved(
        "endpoint added in authentik 2025.10",
        {
            "create_telegram_source": "POST /sources/telegram/",
            "create_telegram_source_mapping": "POST /propertymappings/source/telegram/",
            "delete_telegram_source": "DELETE /sources/telegram/{slug}/",
            "delete_telegram_source_mapping": "DELETE /propertymappings/source/telegram/{id}/",
            "list_telegram_source_mappings": "GET /propertymappings/source/telegram/",
            "list_telegram_sources": "GET /sources/telegram/",
            "show_telegram_source": "GET /sources/telegram/{slug}/",
            "show_telegram_source_mapping": "GET /propertymappings/source/telegram/{id}/",
            "update_telegram_source": "PATCH /sources/telegram/{slug}/",
            "update_telegram_source_mapping": "PATCH /propertymappings/source/telegram/{id}/",
        },
    ),
    **_unserved(
        "endpoint added in authentik 2025.12",
        {
            "add_user_to_role": "POST /rbac/roles/{role_id}/add_user/",
            "connect_telegram_user": "POST /sources/telegram/{slug}/connect_user/",
            "create_admin_file": "POST /admin/file/",
            "create_agent_connector": "POST /endpoints/agents/connectors/",
            "create_agent_enrollment_token": "POST /endpoints/agents/enrollment_tokens/",
            "create_device_access_group": "POST /endpoints/device_access_groups/",
            "create_device_binding": "POST /endpoints/device_bindings/",
            "create_endpoint_stage": "POST /stages/endpoints/",
            "delete_admin_file": "DELETE /admin/file/",
            "delete_agent_connector": "DELETE /endpoints/agents/connectors/{id}/",
            "delete_agent_enrollment_token": "DELETE /endpoints/agents/enrollment_tokens/{id}/",
            "delete_device_access_group": "DELETE /endpoints/device_access_groups/{id}/",
            "delete_device_binding": "DELETE /endpoints/device_bindings/{id}/",
            "delete_endpoint_connector": "DELETE /endpoints/connectors/{id}/",
            "delete_endpoint_device": "DELETE /endpoints/devices/{id}/",
            "delete_endpoint_stage": "DELETE /stages/endpoints/{id}/",
            "delete_export": "DELETE /reports/exports/{id}/",
            "export_events": "POST /events/events/export/",
            "export_users": "POST /core/users/export/",
            "get_endpoint_device_summary": "GET /endpoints/devices/summary/",
            "list_admin_files": "GET /admin/file/",
            "list_agent_connectors": "GET /endpoints/agents/connectors/",
            "list_agent_enrollment_tokens": "GET /endpoints/agents/enrollment_tokens/",
            "list_device_access_groups": "GET /endpoints/device_access_groups/",
            "list_device_bindings": "GET /endpoints/device_bindings/",
            "list_endpoint_connector_types": "GET /endpoints/connectors/types/",
            "list_endpoint_connectors": "GET /endpoints/connectors/",
            "list_endpoint_devices": "GET /endpoints/devices/",
            "list_endpoint_stages": "GET /stages/endpoints/",
            "list_exports": "GET /reports/exports/",
            "remove_user_from_role": "POST /rbac/roles/{role_id}/remove_user/",
            "show_agent_connector": "GET /endpoints/agents/connectors/{id}/",
            "show_agent_enrollment_token": "GET /endpoints/agents/enrollment_tokens/{id}/",
            "show_device_access_group": "GET /endpoints/device_access_groups/{id}/",
            "show_device_binding": "GET /endpoints/device_bindings/{id}/",
            "show_endpoint_connector": "GET /endpoints/connectors/{id}/",
            "show_endpoint_device": "GET /endpoints/devices/{id}/",
            "show_endpoint_stage": "GET /stages/endpoints/{id}/",
            "show_export": "GET /reports/exports/{id}/",
            "update_agent_connector": "PATCH /endpoints/agents/connectors/{id}/",
            "update_agent_enrollment_token": "PATCH /endpoints/agents/enrollment_tokens/{id}/",
            "update_device_access_group": "PATCH /endpoints/device_access_groups/{id}/",
            "update_device_binding": "PATCH /endpoints/device_bindings/{id}/",
            "update_endpoint_device": "PATCH /endpoints/devices/{id}/",
            "update_endpoint_stage": "PATCH /stages/endpoints/{id}/",
            "view_enrollment_token_key": "GET /endpoints/agents/enrollment_tokens/{id}/view_key/",
        },
    ),
    **_unserved(
        "endpoint added in authentik 2026.2",
        {
            "bulk_delete_sessions": "DELETE /core/authenticated_sessions/bulk_delete/",
            "create_fleet_connector": "POST /endpoints/fleet/connectors/",
            "create_lifecycle_iteration": "POST /lifecycle/iterations/",
            "create_wsfed_provider": "POST /providers/wsfed/",
            "delete_fleet_connector": "DELETE /endpoints/fleet/connectors/{id}/",
            "delete_wsfed_provider": "DELETE /providers/wsfed/{id}/",
            "get_wsfed_metadata": "GET /providers/wsfed/{id}/metadata/",
            "list_fleet_connectors": "GET /endpoints/fleet/connectors/",
            "list_wsfed_providers": "GET /providers/wsfed/",
            "show_fleet_connector": "GET /endpoints/fleet/connectors/{id}/",
            "show_wsfed_provider": "GET /providers/wsfed/{id}/",
            "update_fleet_connector": "PATCH /endpoints/fleet/connectors/{id}/",
            "update_wsfed_provider": "PATCH /providers/wsfed/{id}/",
        },
    ),
    **_unserved(
        "endpoint added in authentik 2026.5",
        {
            "create_google_chrome_connector": "POST /endpoints/google_chrome/connectors/",
            "delete_google_chrome_connector": (
                "DELETE /endpoints/google_chrome/connectors/{id}/"
            ),
            "list_google_chrome_connectors": "GET /endpoints/google_chrome/connectors/",
            "send_invitation_email": "POST /stages/invitation/invitations/{id}/send_email/",
            "show_google_chrome_connector": "GET /endpoints/google_chrome/connectors/{id}/",
            "update_google_chrome_connector": (
                "PATCH /endpoints/google_chrome/connectors/{id}/"
            ),
        },
    ),
}

# Endpoints the pinned release does publish but the community container does not
# route. These do not shrink with a pin bump - only an Enterprise licence and
# multi-tenant mode would expose them - so they are kept apart from SPEC_GAPS.
# Their query and body names were checked against the pinned release's own
# published schema.yml, which does carry them.
FEATURE_GATED: dict[str, _Unserved] = _unserved(
    "Enterprise multi-tenancy: published by the pinned release, not routed by "
    "the community container",
    {
        "create_tenant": "POST /tenants/tenants/",
        "create_tenant_admin_group": "POST /tenants/tenants/{id}/create_admin_group/",
        "create_tenant_domain": "POST /tenants/domains/",
        "create_tenant_recovery_key": "POST /tenants/tenants/{id}/create_recovery_key/",
        "delete_tenant": "DELETE /tenants/tenants/{id}/",
        "delete_tenant_domain": "DELETE /tenants/domains/{id}/",
        "list_tenant_domains": "GET /tenants/domains/",
        "list_tenants": "GET /tenants/tenants/",
        "show_tenant": "GET /tenants/tenants/{id}/",
        "show_tenant_domain": "GET /tenants/domains/{id}/",
        "update_tenant": "PATCH /tenants/tenants/{id}/",
        "update_tenant_domain": "PATCH /tenants/domains/{id}/",
    },
)

_UNSERVED: dict[str, _Unserved] = {**SPEC_GAPS, **FEATURE_GATED}

_CLIENT_VERBS = {
    "get": "GET",
    "post": "POST",
    "put": "PUT",
    "patch": "PATCH",
    "delete": "DELETE",
}
# httpx kwargs that carry no field names of their own.
_NO_PAYLOAD_KWARGS = frozenset({"headers", "timeout"})
# httpx kwargs that spell out request-body field names: JSON object keys, and
# the form/file parts of a multipart request.
_BODY_KWARGS = frozenset({"json", "data", "files"})

# Call plumbing the extractor already models; everything else that reaches
# these markers inside a helper is a wire call hiding from the check.
_PLUMBING = frozenset({"_body", "_get_client", "_paginated", "locals"})
_WIRE_MARKER = re.compile(r"_get_client\(|_paginated\(|httpx\.")


@functools.cache
def _hits_wire(target: Callable[..., Any]) -> bool:
    # getsource failing here is a loud test error by design: an unreadable
    # helper cannot be assumed clean.
    return bool(_WIRE_MARKER.search(inspect.getsource(target)))


@dataclass(frozen=True)
class _WireCall:
    """One outbound HTTP call, as read off the source of an op."""

    method: str
    path: str
    query: frozenset[str]
    body: frozenset[str]


def _is_named(node: ast.expr | None, name: str) -> bool:
    return isinstance(node, ast.Name) and node.id == name


def _is_call_to(node: ast.expr | None, name: str) -> TypeGuard[ast.Call]:
    return isinstance(node, ast.Call) and _is_named(node.func, name)


# -- AST extraction ---------------------------------------------------------


class _OpExtractor:
    """Reads the wire calls an op makes straight off its source.

    Every shape outside the grammar records a reason in `reasons`, which the
    op has to account for in UNANALYZABLE_OK. What was read alongside it is
    still returned, so waiving a shape never waives the rest of the op.
    """

    def __init__(self, fn: Callable[..., Any]) -> None:
        self.params: list[str] = []
        self.var_keyword: str | None = None
        for name, param in inspect.signature(fn).parameters.items():
            if param.kind is inspect.Parameter.VAR_KEYWORD:
                self.var_keyword = name
            else:
                self.params.append(name)
        self.module = inspect.getmodule(fn)
        tree = ast.parse(textwrap.dedent(inspect.getsource(fn)))
        self.stmts: list[ast.stmt] = tree.body[0].body  # type: ignore[attr-defined]
        self.reasons: list[str] = []
        self.clients = {
            target.id
            for node in self._walk()
            if isinstance(node, ast.Assign) and _is_call_to(node.value, "_get_client")
            for target in node.targets
            if isinstance(target, ast.Name)
        }

    def calls(self) -> list[_WireCall]:
        """Every call whose method and path could be read, blocked op or not.

        A call is dropped only when its own path is unreadable - there is then
        nothing left to assert. A call whose payload alone defeated the reader
        keeps the names that were read: those are real, only the rest is unknown.
        """
        found = []
        for node in self._walk():
            if not isinstance(node, ast.Call):
                continue
            fn = node.func
            if isinstance(fn, ast.Attribute) and self._is_client(fn.value):
                call = self._from_client(node, fn.attr)
            elif _is_named(fn, "_paginated"):
                call = self._from_paginated(node)
            else:
                if isinstance(fn, ast.Name):
                    self._check_helper(fn.id)
                continue
            if call is not None:
                found.append(call)
        return found

    def _is_client(self, node: ast.expr) -> bool:
        return _is_call_to(node, "_get_client") or (
            isinstance(node, ast.Name) and node.id in self.clients
        )

    def _check_helper(self, name: str) -> None:
        """Block ops whose helpers hit the wire where this test cannot see."""
        if name in _PLUMBING:
            return
        target = getattr(self.module, name, None)
        # Registered ops another op drives are checked in their own right.
        if not inspect.isfunction(target) or hasattr(target, "_mcp_group"):
            return
        if _hits_wire(target):
            self._block(f"calls {name}(), which makes HTTP calls this extractor cannot read")

    def _new_binding_before(self, call: ast.Call) -> bool:
        """True if a non-parameter name is bound before `call` captures locals().

        A rebind of a signature parameter keeps the locals() key set intact, and
        a binding whose statement contains `call` itself completes only after
        locals() is read - both are safe. Everything else could smuggle an
        extra name onto the wire.
        """
        for stmt in self.stmts:
            for node in ast.walk(stmt):
                if isinstance(node, ast.NamedExpr):
                    return True
                new_binding = False
                if isinstance(node, ast.Assign):
                    names = [t.id for t in node.targets if isinstance(t, ast.Name)]
                    new_binding = len(names) != len(node.targets) or not all(
                        n in self.params for n in names
                    )
                elif isinstance(node, ast.AnnAssign):
                    new_binding = not (
                        isinstance(node.target, ast.Name) and node.target.id in self.params
                    )
                elif isinstance(node, (ast.For, ast.With, ast.AugAssign)):
                    new_binding = True
                if new_binding and (
                    node.end_lineno or node.lineno,
                    node.end_col_offset or 0,
                ) < (call.lineno, call.col_offset):
                    return True
        return False

    def _walk(self) -> Iterator[ast.AST]:
        for stmt in self.stmts:
            yield from ast.walk(stmt)

    def _block(self, reason: str) -> None:
        # Deduplicated so the recorded reason set is stable enough to allowlist.
        if reason not in self.reasons:
            self.reasons.append(reason)

    # -- literals -----------------------------------------------------------

    def _const_str(self, node: ast.expr | None) -> str:
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        self._block(f"expected a string literal, found {type(node).__name__}")
        return ""

    def _str_tuple(self, node: ast.expr) -> set[str]:
        if isinstance(node, (ast.Tuple, ast.List)):
            return {self._const_str(e) for e in node.elts}
        self._block("exclude= is not a literal tuple")
        return set()

    def _str_dict(self, node: ast.expr) -> dict[str, str]:
        if isinstance(node, ast.Dict):
            return {self._const_str(k): self._const_str(v) for k, v in zip(node.keys, node.values)}
        self._block("rename= is not a literal dict")
        return {}

    def _dict_keys(self, node: ast.Dict) -> set[str]:
        """Literal keys, letting `**kwargs` through as the unknowable extras."""
        for key, value in zip(node.keys, node.values):
            if key is None and not _is_named(value, self.var_keyword or ""):
                self._block("dict literal unpacks something other than **kwargs")
                return set()
        return {self._const_str(k) for k in node.keys if k is not None}

    # -- name derivation ----------------------------------------------------

    def _forwarded(self, node: ast.Call) -> set[str]:
        """Signature params that reach the wire, after exclude= and rename=."""
        excluded: set[str] = set()
        renames: dict[str, str] = {}
        for kw in node.keywords:
            if kw.arg == "exclude":
                excluded |= self._str_tuple(kw.value)
            elif kw.arg == "rename":
                renames = self._str_dict(kw.value)
            elif kw.arg != "keep_null":  # keep_null changes values, not names
                self._block(f"unsupported keyword {kw.arg!r}")
        return {renames.get(p, p) for p in self.params if p not in excluded}

    def _body_call_names(self, node: ast.Call) -> set[str]:
        if not node.args or not _is_call_to(node.args[0], "locals"):
            self._block("_body() is not called on locals()")
            return set()
        if self._new_binding_before(node):
            self._block("a local is bound before _body(locals()) reads the frame")
            return set()
        return self._forwarded(node)

    def _payload_names(self, value: ast.expr | None) -> set[str]:
        if value is None or (isinstance(value, ast.Constant) and value.value is None):
            return set()
        if isinstance(value, ast.Dict):
            return self._dict_keys(value)
        if _is_call_to(value, "_body"):
            return self._body_call_names(value)
        if isinstance(value, ast.Name):
            # A bare **kwargs payload carries only caller-supplied names.
            if value.id == self.var_keyword:
                return set()
            return self._resolve_dict_var(value.id)
        self._block(f"payload is a {type(value).__name__}, not a readable dict")
        return set()

    def _resolve_dict_var(self, name: str) -> set[str]:
        """Union of the keys a local dict variable can end up carrying."""
        keys: set[str] = set()
        assigned = False
        for node in self._walk():
            targets: list[ast.expr] = []
            value: ast.expr | None = None
            if isinstance(node, ast.Assign):
                targets, value = list(node.targets), node.value
            elif isinstance(node, ast.AnnAssign):
                targets, value = [node.target], node.value
            elif isinstance(node, ast.AugAssign) and _is_named(node.target, name):
                self._block(f"augmented assignment to {name!r}")
            elif (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and _is_named(node.func.value, name)
            ):
                self._block(f"{name}.{node.func.attr}() mutates the payload")
            for target in targets:
                if _is_named(target, name):
                    keys |= self._initial_keys(value)
                    assigned = True
                elif isinstance(target, ast.Subscript) and _is_named(target.value, name):
                    keys.add(self._const_str(target.slice))
        if not assigned:
            self._block(f"no assignment to {name!r} found in the op")
        return keys

    def _initial_keys(self, value: ast.expr | None) -> set[str]:
        if isinstance(value, ast.Dict):
            return self._dict_keys(value)
        if _is_call_to(value, "_body"):
            return self._body_call_names(value)
        self._block(f"dict built from a {type(value).__name__}, not a literal")
        return set()

    # -- call shapes --------------------------------------------------------

    def _readable_path(self, node: ast.expr) -> str | None:
        """The path, or None once reading it recorded a reason."""
        mark = len(self.reasons)
        path = self._path(node)
        return None if len(self.reasons) != mark else path

    def _from_client(self, node: ast.Call, verb: str) -> _WireCall | None:
        if verb not in _CLIENT_VERBS:
            self._block(f"unknown client method {verb!r}")
            return None
        if not node.args:
            self._block(f"{verb}() called without a path")
            return None
        path = self._readable_path(node.args[0])
        if path is None:
            return None
        if node.args[1:]:
            self._block(f"{verb}() passes a payload positionally")
        query: set[str] = set()
        body: set[str] = set()
        for kw in node.keywords:
            if kw.arg == "params":
                query |= self._payload_names(kw.value)
            elif kw.arg in _BODY_KWARGS:
                body |= self._payload_names(kw.value)
            elif kw.arg not in _NO_PAYLOAD_KWARGS:
                self._block(f"{verb}() carries a payload in {kw.arg!r}")
        return _WireCall(_CLIENT_VERBS[verb], path, frozenset(query), frozenset(body))

    def _from_paginated(self, node: ast.Call) -> _WireCall | None:
        """_paginated(path, params, limit, slim_fields) is a GET that adds page_size."""
        positional = dict(zip(("path", "params", "limit", "slim_fields"), node.args))
        by_name = {kw.arg: kw.value for kw in node.keywords if kw.arg}
        unknown = sorted(set(by_name) - {"params", "limit", "slim_fields"})
        if len(node.args) > 4 or unknown or "path" not in positional:
            self._block(f"_paginated() called as (args={len(node.args)}, extra={unknown})")
            return None
        path = self._readable_path(positional["path"])
        if path is None:
            return None
        query = self._payload_names(positional.get("params") or by_name.get("params"))
        return _WireCall("GET", path, frozenset(query | {"page_size"}), frozenset())

    def _path(self, node: ast.expr) -> str:
        if isinstance(node, ast.Constant):
            return self._const_str(node)
        if not isinstance(node, ast.JoinedStr):
            self._block(f"path is a {type(node).__name__}, not a literal")
            return ""
        parts = []
        for piece in node.values:
            if isinstance(piece, ast.Constant):
                parts.append(str(piece.value))
            elif isinstance(piece, ast.FormattedValue) and isinstance(piece.value, ast.Name):
                parts.append("{" + piece.value.id + "}")
            else:
                self._block("path f-string interpolates an expression")
                return ""
        return "".join(parts)


@dataclass(frozen=True)
class _Ops:
    """Readable calls per op, plus what defeated the reader where it did."""

    calls: dict[str, list[_WireCall]]
    blocked: dict[str, tuple[str, ...]]
    no_wire_call: list[str]


@functools.lru_cache(maxsize=1)
def _extract_ops() -> _Ops:
    calls: dict[str, list[_WireCall]] = {}
    blocked: dict[str, tuple[str, ...]] = {}
    no_wire_call: list[str] = []
    for name, fn in sorted(_collect_ops().items()):
        extractor = _OpExtractor(fn)
        found = extractor.calls()
        if found:
            calls[name] = found
        if extractor.reasons:
            blocked[name] = tuple(sorted(extractor.reasons))
        elif not found:
            no_wire_call.append(name)
    return _Ops(calls, blocked, no_wire_call)


# -- OpenAPI index ----------------------------------------------------------


_HTTP_METHODS = frozenset(_CLIENT_VERBS.values())
_PLACEHOLDER_SEGMENT = re.compile(r"^\{\w+\}$")
_MAX_REF_DEPTH = 8


def _shape(path: str) -> tuple[str | None, ...]:
    """The path with its placeholder names erased, so ours line up with the spec's.

    Placeholder names are ours to choose; every other segment has to match
    exactly. Letting a spec placeholder swallow one of our literals instead would
    hide the commonest path typo, because a mistyped sub-resource
    (`/core/users/pathz/`) reads like just another detail route.

    Only the leading slash is stripped: Django routes `/tasks/workers` and
    `/tasks/workers/` differently and httpx does not follow the APPEND_SLASH
    redirect, so a trailing slash we add or drop has to register as a mismatch.
    """
    return tuple(
        None if _PLACEHOLDER_SEGMENT.match(seg) else seg for seg in path.lstrip("/").split("/")
    )


class _Schema:
    """Query/body name sets per (path template, method), matched structurally."""

    def __init__(self, spec: dict[str, Any]) -> None:
        components = spec.get("components") or {}
        self._defs: dict[str, Any] = components.get("schemas") or {}
        self._shared_params: dict[str, Any] = components.get("parameters") or {}
        self.endpoints: dict[tuple[str, str], tuple[frozenset[str], frozenset[str]]] = {}
        self.query_enums: dict[tuple[str, str], dict[str, frozenset[str]]] = {}
        self._paths: list[str] = sorted(spec["paths"])
        self._by_shape: dict[tuple[str | None, ...], list[str]] = {}
        for path in self._paths:
            self._by_shape.setdefault(_shape(path), []).append(path)
        for path, item in spec["paths"].items():
            shared = item.get("parameters") or []
            for method, operation in item.items():
                if method.upper() not in _HTTP_METHODS or not isinstance(operation, dict):
                    continue
                query: set[str] = set()
                enums: dict[str, frozenset[str]] = {}
                for entry in [*shared, *(operation.get("parameters") or [])]:
                    # Pagination and search params are shared components from
                    # authentik 2025.10 on; older schemas inline every one.
                    ref = entry.get("$ref")
                    param = self._shared_params.get(ref.rsplit("/", 1)[-1], {}) if ref else entry
                    if param.get("in") != "query":
                        continue
                    query.add(param["name"])
                    # Formal enums only; prose-documented value sets are not
                    # machine-checkable and are skipped.
                    values = self._enum_values(param.get("schema") or {})
                    if values:
                        enums[param["name"]] = values
                key = (path, method.upper())
                self.endpoints[key] = (frozenset(query), self._body_names(operation))
                self.query_enums[key] = enums

    def _deref(self, schema: dict[str, Any]) -> dict[str, Any]:
        ref = schema.get("$ref")
        return self._defs.get(ref.rsplit("/", 1)[-1]) or {} if ref else {}

    def _body_names(self, operation: dict[str, Any]) -> frozenset[str]:
        """Field names of every media type the endpoint accepts (JSON, multipart)."""
        content = (operation.get("requestBody") or {}).get("content") or {}
        names: set[str] = set()
        for media in content.values():
            names |= self._properties(media.get("schema") or {})
        return frozenset(names)

    def _properties(self, schema: dict[str, Any], depth: int = 0) -> set[str]:
        if depth > _MAX_REF_DEPTH or not isinstance(schema, dict):
            return set()
        if "$ref" in schema:
            return self._properties(self._deref(schema), depth + 1)
        names = set(schema.get("properties") or {})
        for keyword in ("allOf", "oneOf", "anyOf"):
            for member in schema.get(keyword) or []:
                names |= self._properties(member, depth + 1)
        return names

    def _enum_values(self, schema: dict[str, Any], depth: int = 0) -> frozenset[str]:
        """String enum values, through $ref and through an array's item schema."""
        if depth > _MAX_REF_DEPTH or not isinstance(schema, dict):
            return frozenset()
        if "$ref" in schema:
            return self._enum_values(self._deref(schema), depth + 1)
        values = {v for v in schema.get("enum") or [] if isinstance(v, str)}
        return frozenset(values | self._enum_values(schema.get("items") or {}, depth + 1))

    def candidates(self, path: str, method: str) -> list[str]:
        pool = self._by_shape.get(_shape(path), ())
        return [p for p in pool if (p, method) in self.endpoints]

    def describe(self, path: str) -> str:
        """What the spec has here instead, so a wrong verb or a typo is obvious."""
        pool = self._by_shape.get(_shape(path), ())
        if pool:
            verbs = sorted(f"{m} {p}" for p in pool for (p2, m) in self.endpoints if p2 == p)
            return ", ".join(verbs)
        prefix = "/" + "/".join(path.strip("/").split("/")[:2])
        near = [p for p in self._paths if p.startswith(prefix)]
        return ", ".join(near[:8]) if near else "nothing under this prefix"


@pytest.fixture(scope="session")
def schema(configure_env: dict[str, str]) -> _Schema:
    """The live instance's own OpenAPI 3 document, served under the API root."""
    response = httpx.get(
        f"{configure_env['AUTHENTIK_URL']}/api/v3/schema/",
        headers={"Accept": "application/json"},
        timeout=60.0,
    )
    response.raise_for_status()
    return _Schema(response.json())


# -- Tests ------------------------------------------------------------------


def test_every_unreadable_shape_is_allowlisted() -> None:
    """The reasons have to match entry for entry, not just the op name."""
    unknown = {
        name: reasons
        for name, reasons in _extract_ops().blocked.items()
        if UNANALYZABLE_OK.get(name) != reasons
    }
    assert not unknown, (
        "Shapes this test cannot read are missing from UNANALYZABLE_OK, or the "
        "recorded reasons no longer match. Reshape the op into a readable form, "
        "teach the extractor the shape, or allowlist it with its exact reasons - "
        "code shapes only, NEVER a name mismatch:\n"
        + "\n".join(f"  {name}: {list(reasons)}" for name, reasons in sorted(unknown.items()))
    )


def test_allowlists_have_no_stale_entries() -> None:
    ops = _extract_ops()
    stale = sorted(set(UNANALYZABLE_OK) - set(ops.blocked))
    assert not stale, (
        "These ops read cleanly now - drop them from UNANALYZABLE_OK so the "
        f"allowlist can only shrink: {stale}"
    )
    both = sorted(set(SPEC_GAPS) & set(FEATURE_GATED))
    assert not both, f"Ops listed as both a spec gap and feature-gated: {both}"
    orphaned = sorted(set(_UNSERVED) - set(ops.calls))
    assert not orphaned, f"SPEC_GAPS/FEATURE_GATED name ops with no wire call: {orphaned}"


def test_no_wire_call_ops_are_expected() -> None:
    ops = _extract_ops()
    unexpected = sorted(set(ops.no_wire_call) - NO_WIRE_CALL_OK)
    assert not unexpected, (
        "Ops with no readable wire call of their own. If they truly only "
        f"drive other registered ops, add them to NO_WIRE_CALL_OK: {unexpected}"
    )
    stale = sorted(NO_WIRE_CALL_OK - set(ops.no_wire_call))
    assert not stale, f"NO_WIRE_CALL_OK entries no longer match reality: {stale}"


def _arg_wire_names(fn: Callable[..., Any]) -> dict[str, str]:
    """Best-effort map from a signature arg to the wire name it is sent under.

    Sources: `rename=` dicts of _body, dict literals `{"key": arg}`, and
    subscript assigns `params["key"] = arg`. Args sent under their own name need
    no entry; args whose value is transformed before sending stay unmapped and
    are simply not enum-checked.
    """
    mapping: dict[str, str] = {}
    for node in ast.walk(ast.parse(textwrap.dedent(inspect.getsource(fn)))):
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Subscript)
            and isinstance(node.targets[0].slice, ast.Constant)
            and isinstance(node.value, ast.Name)
        ):
            mapping[node.value.id] = node.targets[0].slice.value
        elif isinstance(node, ast.Dict):
            for key, value in zip(node.keys, node.values):
                if isinstance(key, ast.Constant) and isinstance(value, ast.Name):
                    mapping[value.id] = key.value
        elif _is_call_to(node, "_body"):
            for kw in node.keywords:
                if kw.arg == "rename" and isinstance(kw.value, ast.Dict):
                    for key, value in zip(kw.value.keys, kw.value.values):
                        if isinstance(key, ast.Constant) and isinstance(value, ast.Constant):
                            mapping[key.value] = value.value
    return mapping


def _literal_values(annotation: Any) -> frozenset[str]:
    """String values of every Literal reachable inside the annotation."""
    values: set[str] = set()
    stack = [annotation]
    while stack:
        ann = stack.pop()
        if typing.get_origin(ann) is Literal:
            values |= {a for a in typing.get_args(ann) if isinstance(a, str)}
        else:
            stack.extend(typing.get_args(ann))
    return frozenset(values)


def test_query_enum_values_match_schema(schema: _Schema) -> None:
    """A Literal value the schema's enum lacks is the silent-lie class again:
    authentik's filter backend drops the whole filter instead of erroring. Query
    params only - body enums are rare and not modeled here."""
    findings: list[str] = []
    for op, calls in sorted(_extract_ops().calls.items()):
        fn = _collect_ops()[op]
        hints = typing.get_type_hints(fn, include_extras=True)
        wire_of = _arg_wire_names(fn)
        for call in calls:
            matches = schema.candidates(call.path, call.method)
            if len(matches) != 1:
                continue
            enums = schema.query_enums.get((matches[0], call.method), {})
            for arg, annotation in hints.items():
                values = _literal_values(annotation)
                wire = wire_of.get(arg, arg)
                if not values or wire not in call.query:
                    continue
                extra = sorted(values - enums[wire]) if wire in enums else []
                if extra:
                    findings.append(
                        f"{op}.{arg} -> {call.method} {call.path} ?{wire}: Literal "
                        f"values {extra} are not in the schema enum {sorted(enums[wire])}"
                    )
    assert not findings, (
        f"{len(findings)} Literal(s) advertise values the schema enum lacks; "
        "authentik silently ignores these:\n" + "\n".join(f"  {f}" for f in findings)
    )


def test_wire_calls_match_schema(schema: _Schema) -> None:
    findings: list[str] = []
    for op, calls in sorted(_extract_ops().calls.items()):
        recorded = _UNSERVED.get(op)
        unserved: set[str] = set()
        for call in calls:
            where = f"{op}: {call.method} {call.path}"
            matches = schema.candidates(call.path, call.method)
            if not matches:
                unserved.add(f"{call.method} {call.path}")
                if recorded is None:
                    findings.append(
                        f"{where}: no such endpoint in the schema; it has "
                        f"{schema.describe(call.path)}"
                    )
                continue
            if len(matches) > 1:
                findings.append(f"{where}: ambiguous, matches schema paths {matches}")
                continue
            allowed_query, allowed_body = schema.endpoints[matches[0], call.method]
            bad_query = sorted(call.query - allowed_query)
            if bad_query:
                findings.append(
                    f"{where}: query params {bad_query} are not in the schema; "
                    f"it accepts {sorted(allowed_query)}"
                )
            bad_body = sorted(call.body - allowed_body)
            if bad_body:
                findings.append(
                    f"{where}: body fields {bad_body} are not in the schema; "
                    f"it accepts {sorted(allowed_body)}"
                )
        if recorded is not None and unserved != {recorded.call}:
            findings.append(
                f"{op}: recorded as unserved by the pinned instance for "
                f"[{recorded.call}], but its unserved calls are "
                f"{sorted(unserved) or 'none - drop it from the table'}"
            )
    assert not findings, (
        f"{len(findings)} call(s) disagree with the authentik schema. authentik "
        "drops unknown names silently, so each of these is a request that quietly "
        "does not do what it says:\n" + "\n".join(f"  {f}" for f in findings)
    )
