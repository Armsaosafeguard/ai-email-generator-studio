"""Assembles the final prompt string from a request + tone directives."""
from __future__ import annotations

from studio.host.contracts import EmailRequest

SYSTEM_PREAMBLE = (
    "You are an email drafting engine. Output only the email body. "
    "No preamble, no sign-off placeholders you were not given."
)


class PromptBuilder:
    def __init__(self, generator_cfg: dict) -> None:
        self.max_tokens = generator_cfg.get("max_tokens", 900)
        self.temperature = generator_cfg.get("temperature", 0.7)

    def enrich(self, req: EmailRequest) -> EmailRequest:
        parts = [SYSTEM_PREAMBLE, f"Tone: {req.tone}."]
        if req.recipient_name:
            parts.append(f"Recipient: {req.recipient_name}.")
        if req.sender_name:
            parts.append(f"Sender: {req.sender_name}.")
        for key, val in req.variables.items():
            parts.append(f"{key}: {val}")
        parts.append("---")
        parts.append(req.body_seed)
        return EmailRequest(
            subject=req.subject,
            body_seed="\n".join(parts),
            tone=req.tone,
            recipient_name=req.recipient_name,
            sender_name=req.sender_name,
            variables=req.variables,
        )