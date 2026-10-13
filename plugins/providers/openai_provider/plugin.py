"""OpenAI-backed provider plugin."""
from __future__ import annotations

from studio.host.contracts import EmailDraft, EmailPlugin, EmailRequest, PluginSpec
from studio.services.provider_client import ProviderClient

DEFAULT_MODEL = "gpt-4o-mini"


class OpenAIProvider(EmailPlugin):
    kind = "provider"

    def __init__(self) -> None:
        self.client = ProviderClient("https://api.openai.com/v1", "OPENAI_API_KEY")

    def spec(self) -> PluginSpec:
        return PluginSpec(
            name="openai_provider",
            kind="provider",
            version="0.6.1",
            author="studio-core",
            description="Drafts emails via the OpenAI chat completions API.",
            capabilities=("network",),
        )

    def render(self, req: EmailRequest) -> EmailDraft:
        payload = {
            "model": DEFAULT_MODEL,
            "messages": [
                {"role": "system", "content": req.body_seed.split("---")[0].strip()},
                {"role": "user", "content": req.body_seed.split("---")[-1].strip()},
            ],
            "max_tokens": 900,
            "temperature": 0.7,
        }
        data = self.client.post_json("/chat/completions", payload)
        choice = data["choices"][0]["message"]["content"]
        return EmailDraft(
            subject=req.subject,
            body=choice.strip(),
            provider="openai_provider",
            tokens_used=data.get("usage", {}).get("total_tokens", 0),
        )