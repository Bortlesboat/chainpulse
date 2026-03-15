"""Tests for render module."""

from io import StringIO

from rich.console import Console

from chainpulse.render import (
    render_check_fail,
    render_check_ok,
    render_error,
    render_response,
    render_tool_call,
    render_welcome,
)


def _capture(func, *args, **kwargs) -> str:
    """Capture Rich console output as plain text."""
    buf = StringIO()
    # Temporarily replace the module-level console
    import chainpulse.render as mod
    original = mod.console
    mod.console = Console(file=buf, force_terminal=True, width=120)
    try:
        func(*args, **kwargs)
    finally:
        mod.console = original
    return buf.getvalue()


def test_render_response_contains_text():
    output = _capture(render_response, "Bitcoin fees are low right now.", block_height=900000)
    assert "ChainPulse" in output
    assert "bitcoinsapi.com" in output
    assert "900,000" in output


def test_render_response_no_height():
    output = _capture(render_response, "Test response.")
    assert "bitcoinsapi.com" in output


def test_render_error():
    output = _capture(render_error, "Something went wrong")
    assert "Error" in output
    assert "Something went wrong" in output


def test_render_tool_call():
    output = _capture(render_tool_call, "get_fee_estimates")
    assert "Fee Estimates" in output


def test_render_welcome():
    output = _capture(render_welcome)
    assert "ChainPulse" in output
    assert "Interactive" in output


def test_render_check_ok():
    output = _capture(render_check_ok, block_height=900000)
    assert "900" in output and "000" in output


def test_render_check_fail():
    output = _capture(render_check_fail, "API unreachable")
    assert "API unreachable" in output
