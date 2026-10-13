"""In-memory registry of loaded plugins, keyed by kind."""
from __future__ import annotations

from collections import defaultdict
from typing import Iterator

from studio.host.contracts import EmailPlugin, PluginSpec


class PluginRegistry:
    def __init__(self) -> None:
        self._by_kind: dict[str, dict[str, EmailPlugin]] = defaultdict(dict)
        self._specs: dict[str, PluginSpec] = {}

    def register(self, plugin: EmailPlugin) -> None:
        spec = plugin.spec()
        if spec.name in self._specs:
            raise ValueError(f"duplicate plugin name: {spec.name}")
        self._by_kind[spec.kind][spec.name] = plugin
        self._specs[spec.name] = spec

    def get(self, kind: str, name: str) -> EmailPlugin:
        try:
            return self._by_kind[kind][name]
        except KeyError as exc:
            raise LookupError(f"no {kind} plugin named {name}") from exc

    def of_kind(self, kind: str) -> Iterator[EmailPlugin]:
        yield from self._by_kind.get(kind, {}).values()

    def all_specs(self) -> list[PluginSpec]:
        return list(self._specs.values())

    def __len__(self) -> int:
        return len(self._specs)