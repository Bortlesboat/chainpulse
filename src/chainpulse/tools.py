"""Tool definitions and HTTP execution for the Bitcoin analyst agent.

Each tool maps to a Satoshi API endpoint. Tool definitions follow the Anthropic
tool_use schema. Execute functions make httpx calls and return JSON results.
"""

from __future__ import annotations

import httpx

# -- Tool definitions for Anthropic API --

TOOL_DEFINITIONS = [
    {
        "name": "get_fee_estimates",
        "description": (
            "Get current fee rate estimates for different confirmation targets "
            "(1, 3, 6, 25, 144 blocks). Returns fee rates in sat/vB."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "get_fee_recommendation",
        "description": (
            "Get a human-readable fee recommendation: whether to send now or wait, "
            "with estimated costs and savings analysis."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "get_fee_landscape",
        "description": (
            "Get the full fee landscape analysis: send-now vs wait comparison, "
            "trend direction, and fee range statistics."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "get_mempool_info",
        "description": (
            "Get raw mempool statistics: transaction count, total size in bytes, "
            "memory usage. Shows current congestion level."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "get_mempool_analysis",
        "description": (
            "Get structured mempool analysis: congestion level (low/medium/high), "
            "fee buckets with transaction counts, next-block minimum fee rate."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "get_latest_block",
        "description": (
            "Get the most recently mined block: height, hash, transaction count, "
            "size, weight, median fee rate, and total fees collected."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "get_btc_price",
        "description": (
            "Get current Bitcoin price in USD (and other currencies) with 24-hour "
            "percentage change."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "get_mining_info",
        "description": (
            "Get mining statistics: current difficulty, network hashrate, "
            "block count, and blocks until next difficulty adjustment."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "get_supply_info",
        "description": (
            "Get Bitcoin supply data: circulating supply, percentage mined, "
            "current block subsidy, halvings completed, and blocks until next halving."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "get_network_info",
        "description": (
            "Get network connectivity info: peer connections (in/out), "
            "relay fee, reachable networks (IPv4, IPv6, Tor, I2P, CJDNS)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]

# -- Endpoint mapping --

_TOOL_ENDPOINTS: dict[str, str] = {
    "get_fee_estimates": "/api/v1/fees",
    "get_fee_recommendation": "/api/v1/fees/recommended",
    "get_fee_landscape": "/api/v1/fees/landscape",
    "get_mempool_info": "/api/v1/mempool/info",
    "get_mempool_analysis": "/api/v1/mempool",
    "get_latest_block": "/api/v1/blocks/latest",
    "get_btc_price": "/api/v1/prices",
    "get_mining_info": "/api/v1/mining",
    "get_supply_info": "/api/v1/supply",
    "get_network_info": "/api/v1/network",
}


async def execute_tool(
    tool_name: str,
    tool_input: dict,
    base_url: str,
    client: httpx.AsyncClient,
) -> dict:
    """Execute a tool by calling the corresponding Satoshi API endpoint.

    Returns the parsed JSON response (full envelope with data + meta).
    On HTTP errors, returns an error dict that the agent can interpret.
    """
    endpoint = _TOOL_ENDPOINTS.get(tool_name)
    if not endpoint:
        return {"error": f"Unknown tool: {tool_name}"}

    url = f"{base_url}{endpoint}"
    try:
        response = await client.get(url, timeout=15.0)
        response.raise_for_status()
        return response.json()
    except httpx.TimeoutException:
        return {"error": f"Timeout calling {endpoint} — the API may be slow right now."}
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP {e.response.status_code} from {endpoint}: {e.response.text[:200]}"}
    except httpx.HTTPError as e:
        return {"error": f"Network error calling {endpoint}: {str(e)[:200]}"}
