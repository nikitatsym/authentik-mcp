import os

from authentik_mcp.config import Settings, _reset_settings, get_settings


def test_defaults():
    s = Settings()
    assert s.authentik_url == ""
    assert s.authentik_token == ""


def test_env_vars(monkeypatch):
    monkeypatch.setenv("AUTHENTIK_URL", "https://auth.example.com")
    monkeypatch.setenv("AUTHENTIK_TOKEN", "tok123")
    s = Settings()
    assert s.authentik_url == "https://auth.example.com"
    assert s.authentik_token == "tok123"


def test_singleton():
    _reset_settings()
    a = get_settings()
    b = get_settings()
    assert a is b
    _reset_settings()


def test_reset():
    _reset_settings()
    a = get_settings()
    _reset_settings()
    b = get_settings()
    assert a is not b
    _reset_settings()
