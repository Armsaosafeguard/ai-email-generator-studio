"""Rewrites a draft toward a professional-warm register."""
from __future__ import annotations

import re

from studio.host.contracts import EmailDraft, EmailPlugin, EmailRequest, PluginSpec

HEDGES = re.compile(r"\b(just|kinda|sorta|maybe|i think)\b", re.IGNORECASE)


class ProfessionalTone(EmailPlugin):
    kind = "tone"

    def spec(self) -> PluginSpec:
        return PluginSpec(
            name="tone_professional",
            kind="tone",
            version="0.4.0",
            author="studio-core",
            description="Trims hedges, tightens sentences.",
        )

    def render(self, req: EmailRequest) -> EmailDraft:
        cleaned = HEDGES.sub("", req.body_seed)
        cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
        return EmailDraft(
            subject=req.subject,
            body=cleaned,
            provider="tone_professional",
        )