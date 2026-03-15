"""ChainPulse CLI — Typer application."""

from __future__ import annotations

import asyncio
from typing import Optional

import typer
from rich.console import Console

from chainpulse import __version__
from chainpulse.config import Config, ConfigError
from chainpulse.render import (
    render_check_fail,
    render_check_ok,
    render_error,
    render_response,
    render_welcome,
)

app = typer.Typer(
    name="chainpulse",
    help="AI-powered Bitcoin network intelligence in your terminal.",
    no_args_is_help=True,
    add_completion=False,
)

console = Console()


def _load_config() -> Config:
    try:
        return Config.load()
    except ConfigError as e:
        render_error(str(e))
        raise typer.Exit(1)


def _run_query(query: str, config: Config) -> None:
    from chainpulse.agent import run_agent

    try:
        text, block_height = asyncio.run(run_agent(query, config))
        render_response(text, block_height)
    except KeyboardInterrupt:
        console.print("\n[dim]Cancelled.[/dim]")
    except Exception as e:
        render_error(f"Agent error: {e}")
        raise typer.Exit(1)


@app.command()
def main(
    query: Optional[str] = typer.Argument(
        None,
        help="Question about the Bitcoin network (e.g., 'What are current fees?')",
    ),
    interactive: bool = typer.Option(
        False,
        "--interactive",
        "-i",
        help="Start interactive REPL mode.",
    ),
    check: bool = typer.Option(
        False,
        "--check",
        help="Verify API key and connectivity.",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version.",
    ),
) -> None:
    """Ask questions about the Bitcoin network and get AI-powered analysis."""
    if version:
        console.print(f"chainpulse {__version__}")
        raise typer.Exit()

    config = _load_config()

    if check:
        from chainpulse.agent import check_connectivity

        ok, msg, height = asyncio.run(check_connectivity(config))
        if ok:
            render_check_ok(height)
        else:
            render_check_fail(msg)
            raise typer.Exit(1)
        raise typer.Exit()

    if interactive:
        _interactive_mode(config)
        raise typer.Exit()

    if query:
        _run_query(query, config)
    else:
        # no_args_is_help should catch this, but just in case
        console.print("Provide a question or use --interactive mode.")
        raise typer.Exit(1)


def _interactive_mode(config: Config) -> None:
    """Run the interactive REPL."""
    render_welcome()
    console.print()

    while True:
        try:
            query = console.input("[bold cyan]chainpulse>[/bold cyan] ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye.[/dim]")
            break

        if not query:
            continue
        if query.lower() in ("quit", "exit", "q"):
            console.print("[dim]Goodbye.[/dim]")
            break

        _run_query(query, config)
        console.print()
