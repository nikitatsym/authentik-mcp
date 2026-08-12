#!/usr/bin/env python3
"""Bring up the test Authentik stack and provision a known API token.

Usage: `uv run python scripts/bootstrap.py`  (pass `--no-up` to skip compose up)

Rather than rely on AUTHENTIK_BOOTSTRAP_TOKEN (its timing/availability varies
by version), we create the token deterministically: once the server is ready,
`ak shell` upserts a non-expiring API token for the `akadmin` user with a known
key. Tests then authenticate with that key.

Writes AUTHENTIK_URL / AUTHENTIK_TOKEN to `tests/.env` and prints the token on
success. Idempotent: safe to re-run.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
COMPOSE_FILE = ROOT / "tests" / "docker-compose.yml"
ENV_FILE = ROOT / "tests" / ".env"

AUTHENTIK_URL = os.environ.get("AUTHENTIK_URL", "http://localhost:9000")
API_TOKEN = os.environ.get("AUTHENTIK_TOKEN", "mcp-e2e-test-token-0123456789abcdef012345")
READY_TIMEOUT = int(os.environ.get("AUTHENTIK_READY_TIMEOUT", "420"))  # seconds

# Upsert a non-expiring API token for akadmin with our known key.
_TOKEN_SNIPPET = (
    "from authentik.core.models import Token, User\n"
    "u = User.objects.get(username='akadmin')\n"
    "Token.objects.update_or_create(identifier='mcp-e2e', "
    f"defaults=dict(user=u, intent='api', expiring=False, key='{API_TOKEN}'))\n"
    "print('TOKEN_OK')\n"
)


def _compose(*args: str, capture: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["docker", "compose", "-f", str(COMPOSE_FILE), *args],
        text=True,
        capture_output=capture,
        check=False,
    )


def compose_up() -> None:
    print("[bootstrap] docker compose up -d ...")
    if _compose("up", "-d").returncode != 0:
        raise RuntimeError("docker compose up failed")


def wait_for_ready(url: str, timeout: int) -> None:
    """Poll /-/health/ready/ until the server reports ready (HTTP 204)."""
    deadline = time.time() + timeout
    last = "(no attempt yet)"
    attempts = 0
    while time.time() < deadline:
        attempts += 1
        try:
            r = httpx.get(f"{url}/-/health/ready/", timeout=5)
            if r.status_code in (200, 204):
                print(f"[bootstrap] server ready ({attempts} attempts)")
                return
            last = f"HTTP {r.status_code}"
        except Exception as e:  # noqa: BLE001 — diagnostic only
            last = type(e).__name__
        if attempts % 6 == 0:
            print(f"[bootstrap] waiting for server... last: {last}")
        time.sleep(3)
    raise TimeoutError(f"{url} not ready in {timeout}s (last: {last})")


def ensure_token(timeout: int) -> None:
    """Upsert the API token via `ak shell`, retrying until akadmin exists."""
    deadline = time.time() + timeout
    last = ""
    while time.time() < deadline:
        r = _compose("exec", "-T", "server", "ak", "shell", "-c", _TOKEN_SNIPPET,
                     capture=True)
        if r.returncode == 0 and "TOKEN_OK" in (r.stdout or ""):
            print("[bootstrap] API token provisioned for akadmin")
            return
        last = ((r.stderr or "") + (r.stdout or "")).strip().splitlines()[-1:] or ["?"]
        time.sleep(3)
    raise TimeoutError(f"could not provision token (last: {last})")


def verify(url: str, token: str) -> None:
    r = httpx.get(f"{url}/api/v3/core/users/me/",
                  headers={"Authorization": f"Bearer {token}"}, timeout=8)
    if r.status_code != 200:
        raise RuntimeError(f"token verify failed: HTTP {r.status_code}: {r.text[:200]}")
    user = r.json().get("user", {}).get("username", "?")
    print(f"[bootstrap] token verified — authenticated as {user!r}")


def write_env_file(url: str, token: str) -> None:
    ENV_FILE.parent.mkdir(parents=True, exist_ok=True)
    # LF pinned: shells `source` this file, and CRLF would leave \r inside the token.
    ENV_FILE.write_text(
        "# Written by scripts/bootstrap.py — consumed by tests and local shells\n"
        f"AUTHENTIK_URL={url}\n"
        f"AUTHENTIK_TOKEN={token}\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"[bootstrap] wrote {ENV_FILE}")


def main() -> int:
    print(f"[bootstrap] target: {AUTHENTIK_URL}")
    if "--no-up" not in sys.argv:
        compose_up()
    try:
        wait_for_ready(AUTHENTIK_URL, READY_TIMEOUT)
        ensure_token(timeout=120)
        verify(AUTHENTIK_URL, API_TOKEN)
    except (TimeoutError, RuntimeError) as e:
        print(f"[bootstrap] FAILED: {e}", file=sys.stderr)
        print("[bootstrap] check: docker compose -f tests/docker-compose.yml logs server worker",
              file=sys.stderr)
        return 1
    write_env_file(AUTHENTIK_URL, API_TOKEN)
    print(f"[bootstrap] OK — token: {API_TOKEN}")
    print(f"[bootstrap] interactive shell: `set -a; source {ENV_FILE.relative_to(ROOT)}; set +a`")
    return 0


if __name__ == "__main__":
    sys.exit(main())
