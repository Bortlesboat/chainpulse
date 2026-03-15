"""Anthropic tool_use agent loop for ChainPulse."""

from __future__ import annotations

import json

import anthropic
import httpx

from chainpulse.config import Config
from chainpulse.prompts import SYSTEM_PROMPT
from chainpulse.render import render_thinking, render_tool_call
from chainpulse.tools import TOOL_DEFINITIONS, execute_tool

MAX_TOOL_ROUNDS = 10


async def run_agent(query: str, config: Config) -> tuple[str, int | None]:
    """Run the agent loop: send query, handle tool calls, return final text.

    Returns (response_text, block_height) where block_height is extracted
    from the last API response's meta field.
    """
    client = anthropic.Anthropic(api_key=config.anthropic_api_key)
    messages: list[dict] = [{"role": "user", "content": query}]
    block_height: int | None = None

    async with httpx.AsyncClient() as http_client:
        for _ in range(MAX_TOOL_ROUNDS):
            response = client.messages.create(
                model=config.model,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                tools=TOOL_DEFINITIONS,
                messages=messages,
            )

            # Check if we got a final text response (no more tool calls)
            if response.stop_reason == "end_turn":
                text_parts = [
                    block.text
                    for block in response.content
                    if block.type == "text"
                ]
                return "\n".join(text_parts), block_height

            # Process tool calls
            tool_results = []
            has_tool_use = False

            for block in response.content:
                if block.type == "tool_use":
                    has_tool_use = True
                    render_tool_call(block.name)

                    result = await execute_tool(
                        tool_name=block.name,
                        tool_input=block.input,
                        base_url=config.api_base_url,
                        client=http_client,
                    )

                    # Extract block height from meta
                    if isinstance(result, dict) and "meta" in result:
                        meta_height = result["meta"].get("node_height")
                        if meta_height:
                            block_height = meta_height

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    })

            if not has_tool_use:
                # No tool calls and not end_turn — extract text anyway
                text_parts = [
                    block.text
                    for block in response.content
                    if block.type == "text"
                ]
                text = "\n".join(text_parts) if text_parts else "No response generated."
                return text, block_height

            # Add assistant's response and tool results to conversation
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

            render_thinking()

    return "Reached maximum tool rounds without a final response.", block_height


async def check_connectivity(config: Config) -> tuple[bool, str, int | None]:
    """Check API key validity and Satoshi API reachability.

    Returns (success, message, block_height).
    """
    # Check Anthropic API key
    try:
        client = anthropic.Anthropic(api_key=config.anthropic_api_key)
        client.messages.create(
            model=config.model,
            max_tokens=10,
            messages=[{"role": "user", "content": "ping"}],
        )
    except anthropic.AuthenticationError:
        return False, "Invalid ANTHROPIC_API_KEY", None
    except anthropic.APIError as e:
        return False, f"Anthropic API error: {e}", None

    # Check Satoshi API
    try:
        async with httpx.AsyncClient() as http_client:
            resp = await http_client.get(
                f"{config.api_base_url}/api/v1/blocks/tip/height",
                timeout=10.0,
            )
            resp.raise_for_status()
            data = resp.json()
            height = data.get("data") if isinstance(data, dict) else None
            return True, "OK", height
    except Exception as e:
        return False, f"Satoshi API unreachable: {e}", None
