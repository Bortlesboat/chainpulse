"""Tests for config module."""

import pytest

from chainpulse.config import Config, ConfigError


def test_load_missing_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(ConfigError, match="ANTHROPIC_API_KEY not set"):
        Config.load()


def test_load_defaults(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-123")
    monkeypatch.delenv("CHAINPULSE_API_URL", raising=False)
    monkeypatch.delenv("CHAINPULSE_MODEL", raising=False)

    config = Config.load()
    assert config.anthropic_api_key == "sk-test-123"
    assert config.api_base_url == "https://bitcoinsapi.com"
    assert config.model == "claude-sonnet-4-20250514"


def test_load_custom_url(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-123")
    monkeypatch.setenv("CHAINPULSE_API_URL", "http://localhost:8000/")

    config = Config.load()
    assert config.api_base_url == "http://localhost:8000"  # trailing slash stripped


def test_load_custom_model(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-123")
    monkeypatch.setenv("CHAINPULSE_MODEL", "claude-haiku-4-5-20251001")

    config = Config.load()
    assert config.model == "claude-haiku-4-5-20251001"
