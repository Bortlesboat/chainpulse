"""Tests for CLI module."""

from typer.testing import CliRunner

from chainpulse import __version__
from chainpulse.cli import app

runner = CliRunner()


def test_version_flag():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_help_flag():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output


def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    result = runner.invoke(app, ["test query"])
    assert result.exit_code == 1
    assert "ANTHROPIC_API_KEY" in result.output
