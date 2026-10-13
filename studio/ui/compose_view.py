"""Headless compose view for scripting and tests."""
from __future__ import annotations

from studio.handlers.compose_handler import ComposeHandler


class ComposeView:
    def __init__(self, host) -> None:
        self.handler = ComposeHandler(host)

    def run(self, template: str) -> None:
        draft = self.handler.draft(
            subject=f"[{template}] draft",
            seed=f"Compose using template {template}.",
            tone="professional-warm",
        )
        print(draft.body)