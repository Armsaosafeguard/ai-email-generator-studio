"""Minimal console shell. Real windowing is out of scope for the host."""
from __future__ import annotations

from rich.console import Console
from rich.table import Table

from studio.handlers.compose_handler import ComposeHandler

console = Console()


class MainWindow:
    def __init__(self, host) -> None:
        self.host = host
        self.compose = ComposeHandler(host)

    def run(self) -> None:
        table = Table(title="ai-email-generator-studio")
        table.add_column("plugin")
        table.add_column("kind")
        table.add_column("version")
        for spec in self.host.registry.all_specs():
            table.add_row(spec.name, spec.kind, spec.version)
        console.print(table)
        console.print("[dim]Press Ctrl+C to exit.[/dim]")
        try:
            while True:
                subject = console.input("[bold]subject>[/bold] ")
                seed = console.input("[bold]seed>[/bold] ")
                draft = self.compose.draft(subject, seed, tone="professional-warm")
                console.print(draft.body)
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]bye.[/dim]")