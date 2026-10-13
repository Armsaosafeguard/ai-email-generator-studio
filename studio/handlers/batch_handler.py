"""Batch generation over a contact list, one draft per recipient."""
from __future__ import annotations

from collections.abc import Iterable

from studio.host.contracts import EmailDraft
from studio.models.contact import Contact
from studio.utils.logging import get_logger

log = get_logger(__name__)


class BatchHandler:
    def __init__(self, host) -> None:
        self.host = host

    def run(
        self,
        contacts: Iterable[Contact],
        subject: str,
        seed: str,
        tone: str,
        fmt: str = "exporter_markdown",
    ) -> list[str]:
        paths: list[str] = []
        for contact in contacts:
            draft = self.host.generate(
                __import__("studio.host.contracts", fromlist=["EmailRequest"]).EmailRequest(
                    subject=subject,
                    body_seed=seed,
                    tone=tone,
                    recipient_name=contact.display,
                    variables=contact.as_vars(),
                )
            )
            paths.append(self.host.export(draft, fmt))
            log.info("batch draft saved", extra={"contact": contact.email})
        return paths