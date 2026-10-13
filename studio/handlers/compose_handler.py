"""Single-email compose flow used by the UI view."""
from __future__ import annotations

from studio.host.contracts import EmailDraft, EmailRequest


class ComposeHandler:
    def __init__(self, host) -> None:
        self.host = host

    def draft(
        self,
        subject: str,
        seed: str,
        tone: str,
        recipient: str | None = None,
    ) -> EmailDraft:
        req = EmailRequest(
            subject=subject,
            body_seed=seed,
            tone=tone,
            recipient_name=recipient,
        )
        return self.host.generate(req)

    def save(self, draft: EmailDraft, fmt: str) -> str:
        return self.host.export(draft, fmt)