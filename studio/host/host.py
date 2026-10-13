"""PluginHost — wires loader, registry, services, and the compose pipeline."""
from __future__ import annotations

import tomllib
from pathlib import Path

from studio.host.contracts import EmailDraft, EmailRequest
from studio.host.loader import PluginLoader
from studio.host.registry import PluginRegistry
from studio.services.prompt_builder import PromptBuilder
from studio.utils.logging import get_logger

log = get_logger(__name__)


class PluginHost:
    def __init__(self, config_path: Path, plugin_map: Path) -> None:
        self.config = tomllib.loads(config_path.read_text(encoding="utf-8"))
        self.plugin_map = tomllib.loads(plugin_map.read_text(encoding="utf-8"))
        self.registry = PluginRegistry()
        self.prompt_builder = PromptBuilder(self.config["generator"])
        dirs = [Path(p) for p in self.config["paths"]["plugin_dirs"]]
        self.loader = PluginLoader(
            dirs, strict=self.plugin_map.get("loader", {}).get("strict_manifests", True)
        )

    def discover(self) -> None:
        for spec, payload in self.loader.discover():
            enabled = self.plugin_map.get("enabled", {}).get(spec.name)
            if enabled is False:
                log.info("plugin disabled, skipping", extra={"plugin": spec.name})
                continue
            self.registry.register(payload["instance"])

    def load_all(self) -> None:
        log.info("host ready", extra={"plugins": len(self.registry)})

    def generate(self, req: EmailRequest) -> EmailDraft:
        provider_name = self.config["generator"]["default_provider"]
        provider = self.registry.get("provider", provider_name)
        enriched = self.prompt_builder.enrich(req)
        draft = provider.render(enriched)
        for tone in self.registry.of_kind("tone"):
            draft = tone.render(EmailRequest(
                subject=draft.subject, body_seed=draft.body,
                tone=req.tone, variables=req.variables,
            )) if tone.spec().name == req.tone else draft
        return draft

    def export(self, draft: EmailDraft, fmt: str) -> str:
        exporter = self.registry.get("exporter", fmt)
        out_dir = self.config["paths"]["output_dir"]
        path = exporter.export(draft, out_dir)
        log.info("exported draft", extra={"path": path})
        return path

    def selfcheck(self) -> bool:
        return len(self.registry) > 0 and any(self.registry.of_kind("provider"))