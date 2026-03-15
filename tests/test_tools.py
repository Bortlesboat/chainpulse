"""Tests for tools module."""

import httpx
import pytest
import respx

from chainpulse.tools import _TOOL_ENDPOINTS, TOOL_DEFINITIONS, execute_tool


def test_all_tools_have_endpoints():
    """Every defined tool must map to an endpoint."""
    tool_names = {t["name"] for t in TOOL_DEFINITIONS}
    endpoint_names = set(_TOOL_ENDPOINTS.keys())
    assert tool_names == endpoint_names


def test_tool_definitions_valid_schema():
    """All tool definitions must have required fields."""
    for tool in TOOL_DEFINITIONS:
        assert "name" in tool
        assert "description" in tool
        assert "input_schema" in tool
        assert tool["input_schema"]["type"] == "object"


@pytest.mark.asyncio
async def test_execute_tool_success():
    mock_response = {"data": {"size": 5000}, "meta": {"node_height": 900000}}

    with respx.mock:
        respx.get("https://bitcoinsapi.com/api/v1/mempool/info").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

        async with httpx.AsyncClient() as client:
            result = await execute_tool(
                "get_mempool_info", {}, "https://bitcoinsapi.com", client
            )

    assert result == mock_response


@pytest.mark.asyncio
async def test_execute_tool_unknown():
    async with httpx.AsyncClient() as client:
        result = await execute_tool(
            "nonexistent_tool", {}, "https://bitcoinsapi.com", client
        )
    assert "error" in result
    assert "Unknown tool" in result["error"]


@pytest.mark.asyncio
async def test_execute_tool_timeout():
    with respx.mock:
        respx.get("https://bitcoinsapi.com/api/v1/fees").mock(
            side_effect=httpx.ReadTimeout("timeout")
        )

        async with httpx.AsyncClient() as client:
            result = await execute_tool(
                "get_fee_estimates", {}, "https://bitcoinsapi.com", client
            )

    assert "error" in result
    assert "Timeout" in result["error"]


@pytest.mark.asyncio
async def test_execute_tool_http_error():
    with respx.mock:
        respx.get("https://bitcoinsapi.com/api/v1/mining").mock(
            return_value=httpx.Response(500, text="Internal Server Error")
        )

        async with httpx.AsyncClient() as client:
            result = await execute_tool(
                "get_mining_info", {}, "https://bitcoinsapi.com", client
            )

    assert "error" in result
    assert "500" in result["error"]
