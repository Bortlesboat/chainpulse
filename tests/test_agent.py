"""Tests for agent module — mocked Anthropic + httpx."""

from unittest.mock import MagicMock, patch

import httpx
import pytest
import respx

from chainpulse.agent import run_agent
from chainpulse.config import Config


def _make_config():
    return Config(
        anthropic_api_key="sk-test",
        api_base_url="https://bitcoinsapi.com",
        model="claude-sonnet-4-20250514",
    )


def _make_text_response(text: str):
    """Create a mock Anthropic response with just text (end_turn)."""
    block = MagicMock()
    block.type = "text"
    block.text = text

    response = MagicMock()
    response.stop_reason = "end_turn"
    response.content = [block]
    return response


def _make_tool_response(tool_name: str, tool_input: dict, tool_id: str = "tool_1"):
    """Create a mock Anthropic response with a tool_use block."""
    block = MagicMock()
    block.type = "tool_use"
    block.name = tool_name
    block.input = tool_input
    block.id = tool_id

    response = MagicMock()
    response.stop_reason = "tool_use"
    response.content = [block]
    return response


@pytest.mark.asyncio
async def test_run_agent_simple_text():
    """Agent returns text immediately without tool calls."""
    mock_response = _make_text_response("Bitcoin fees are 5 sat/vB.")

    with patch("chainpulse.agent.anthropic.Anthropic") as mock_cls:
        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_cls.return_value = mock_client

        text, height = await run_agent("What are fees?", _make_config())

    assert "5 sat/vB" in text
    assert height is None


@pytest.mark.asyncio
async def test_run_agent_with_tool_call():
    """Agent calls a tool, gets result, then responds."""
    tool_resp = _make_tool_response("get_fee_estimates", {})
    text_resp = _make_text_response("Current fees are around 3 sat/vB.")

    api_data = {
        "data": [{"conf_target": 1, "fee_rate_sat_vb": 3.0}],
        "meta": {"node_height": 900000},
    }

    with patch("chainpulse.agent.anthropic.Anthropic") as mock_cls:
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = [tool_resp, text_resp]
        mock_cls.return_value = mock_client

        with respx.mock:
            respx.get("https://bitcoinsapi.com/api/v1/fees").mock(
                return_value=httpx.Response(200, json=api_data)
            )

            text, height = await run_agent("What are fees?", _make_config())

    assert "3 sat/vB" in text
    assert height == 900000


@pytest.mark.asyncio
async def test_run_agent_max_rounds():
    """Agent stops after MAX_TOOL_ROUNDS to prevent infinite loops."""
    # Always return tool calls
    tool_resp = _make_tool_response("get_fee_estimates", {})
    api_data = {"data": [], "meta": {"node_height": 900000}}

    with patch("chainpulse.agent.anthropic.Anthropic") as mock_cls:
        mock_client = MagicMock()
        mock_client.messages.create.return_value = tool_resp
        mock_cls.return_value = mock_client

        with respx.mock:
            respx.get("https://bitcoinsapi.com/api/v1/fees").mock(
                return_value=httpx.Response(200, json=api_data)
            )

            text, height = await run_agent("loop forever", _make_config())

    assert "maximum tool rounds" in text.lower()
