"""Integration test fixtures.

Does NOT manage the Docker lifecycle — it reads AUTHENTIK_URL / AUTHENTIK_TOKEN
from the environment or `tests/.env` (produced by `scripts/bootstrap.py`).
Tests using the `agent` / `configure_env` fixtures skip automatically when
those aren't set, so `pytest` stays green without Docker.

Bring the stack up first:  uv run python scripts/bootstrap.py
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pytest

TESTS_DIR = Path(__file__).parent
ENV_FILE = TESTS_DIR / ".env"


def _read_env_file() -> dict[str, str]:
    """Parse tests/.env into a dict. Does NOT touch os.environ — so unit tests
    that assert empty config defaults aren't polluted at collect time."""
    out: dict[str, str] = {}
    if not ENV_FILE.exists():
        return out
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        out[key.strip()] = value.strip()
    return out


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers", "integration: requires a running Authentik (AUTHENTIK_URL/TOKEN)."
    )


# ── Agent simulator ────────────────────────────────────────────────────


class AgentSimulator:
    """Calls MCP operations the way the meta-tools dispatch them.

    `call("create_application", name=..., slug=...)` resolves the snake_case op
    to its PascalCase name, finds its group, and routes through
    `server._dispatch` — exercising the real Pydantic validation + dispatch
    path. Returns the raw result object (dict/list) or raises (ValueError for
    bad params, APIError for HTTP failures).
    """

    def __init__(self) -> None:
        from authentik_mcp import server

        self._server = server

    def call(self, op_snake: str, **params: Any) -> Any:
        s = self._server
        pascal = s._to_pascal(op_snake)
        group = s._all_grouped.get(pascal)
        if group is None:
            raise ValueError(
                f"Unknown grouped operation {op_snake!r} (→ {pascal}). "
                "ROOT ops (e.g. authentik_version) are called directly, not via the agent."
            )
        return s._dispatch(pascal, group, params)

    def help(self, group: str, **params: Any) -> str:
        return self._server._build_help(group, search=params.get("search"))


# ── Fixtures ───────────────────────────────────────────────────────────


def _resolve_env(*names: str) -> dict[str, str] | None:
    """Resolve each name from os.environ first, then tests/.env. None if any missing."""
    file_env = _read_env_file()
    resolved: dict[str, str] = {}
    for n in names:
        val = os.environ.get(n) or file_env.get(n)
        if not val:
            return None
        resolved[n] = val
    return resolved


@pytest.fixture(scope="session")
def configure_env():
    """Point the client at the test instance and reset cached settings/client.

    Resolves env lazily (only when an integration test runs), so unit tests
    that assert empty config defaults stay clean. Restores prior values on
    teardown.
    """
    env = _resolve_env("AUTHENTIK_URL", "AUTHENTIK_TOKEN")
    if env is None:
        pytest.skip(
            "Integration test requires AUTHENTIK_URL/AUTHENTIK_TOKEN. "
            "Run `uv run python scripts/bootstrap.py` to start Authentik."
        )

    from authentik_mcp import config
    from authentik_mcp.tools import helpers

    prior = {k: os.environ.get(k) for k in env}
    os.environ.update(env)
    config._reset_settings()
    helpers._client = None
    yield env
    helpers._client = None
    for k, v in prior.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    config._reset_settings()


@pytest.fixture(scope="session")
def agent(configure_env) -> AgentSimulator:
    return AgentSimulator()
