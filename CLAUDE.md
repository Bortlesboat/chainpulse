# ChainPulse — Development Guide

## What This Is
AI-powered Bitcoin network intelligence CLI. Users ask natural language questions, an Anthropic-powered agent calls Satoshi API endpoints, and results render as beautiful Rich terminal panels.

## Architecture
- `cli.py` — Typer app, entry point. Single query + interactive REPL.
- `agent.py` — Anthropic tool_use loop. Sends system prompt + tools, handles multi-turn tool calls.
- `tools.py` — 10 tool functions, each wraps an httpx GET to bitcoinsapi.com.
- `render.py` — Rich formatting. Panels, tables, color-coded output.
- `prompts.py` — System prompt defining the Bitcoin analyst persona.
- `config.py` — Environment variable loading and validation.

## Key Patterns
- All API calls go through `tools.py` → httpx → bitcoinsapi.com/api/v1/...
- Response envelope: `{data: ..., meta: {timestamp, node_height, ...}}`
- Agent loop: send messages → check for tool_use → execute tools → feed results back → repeat until text response
- Default model: claude-sonnet-4-20250514 (optimized for users' API costs)

## Testing
- `pytest` — all tests use mocked httpx (respx) and mocked Anthropic responses
- No real API calls in tests

## Commands
- `chainpulse "question"` — single query
- `chainpulse -i` — interactive REPL
- `chainpulse --check` — verify API key + connectivity
- `ruff check src/ tests/` — lint
- `pytest` — run tests
