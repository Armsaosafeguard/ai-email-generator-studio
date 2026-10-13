"""Writes an RFC-822-ish .eml file to disk."""
from __future__ import annotations

from pathlib import Path
from email.message import EmailMessage

from studio.host.contracts import EmailDraft, ExporterPlugin, PluginSpec


class EmlExporter(ExporterPlugin):
    kind = "exporter"

    def spec(self) -> PluginSpec:
        return PluginSpec(
            name="exporter_eml",
            kind="exporter",
            version="0.5.2",
            author="community-verified",
            description="Saves drafts as .eml files.",
        )

    def export(self, draft: EmailDraft, out_dir: str) -> str:
        target_dir = Path(out_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        msg = EmailMessage()
        msg["Subject"] = draft.subject
        msg["X-Provider"] = draft.provider
        msg.set_content(draft.body)
        safe = "".join(c if c.isalnum() else "_" for c in draft.subject)[:60]
        path = target_dir / f"{safe or 'draft'}.eml"
        path.write_bytes(msg.as_bytes())
        return str(path)