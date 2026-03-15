"""Rich terminal output formatting for ChainPulse."""

from __future__ import annotations

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

console = Console()


def render_response(text: str, block_height: int | None = None) -> None:
    """Render the agent's final response as a Rich panel with markdown."""
    md = Markdown(text)

    footer_parts = ["Data: bitcoinsapi.com"]
    if block_height:
        footer_parts.append(f"block {block_height:,}")
    footer = " · ".join(footer_parts)

    panel = Panel(
        md,
        title="[bold cyan]⚡ ChainPulse[/bold cyan]",
        subtitle=f"[dim]{footer}[/dim]",
        border_style="cyan",
        padding=(1, 2),
    )
    console.print(panel)


def render_error(message: str) -> None:
    """Render an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def render_tool_call(tool_name: str) -> None:
    """Show which tool the agent is calling (during thinking)."""
    friendly = tool_name.replace("get_", "").replace("_", " ").title()
    console.print(f"  [dim]→ Fetching {friendly}...[/dim]")


def render_thinking() -> None:
    """Show that the agent is synthesizing."""
    console.print("  [dim]→ Analyzing...[/dim]")


def render_welcome() -> None:
    """Render the interactive mode welcome banner."""
    text = Text()
    text.append("⚡ ChainPulse ", style="bold cyan")
    text.append("Interactive Mode\n", style="bold")
    text.append("Ask anything about the Bitcoin network. Type ", style="dim")
    text.append("quit", style="dim bold")
    text.append(" to exit.", style="dim")

    panel = Panel(text, border_style="cyan", padding=(0, 2))
    console.print(panel)


def render_check_ok(block_height: int | None = None) -> None:
    """Render a successful connectivity check."""
    msg = "[bold green]✓[/bold green] API key valid, Satoshi API reachable"
    if block_height:
        msg += f" (block {block_height:,})"
    console.print(msg)


def render_check_fail(reason: str) -> None:
    """Render a failed connectivity check."""
    console.print(f"[bold red]✗[/bold red] Check failed: {reason}")
