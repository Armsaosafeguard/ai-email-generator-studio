"""Shared contracts every plugin must satisfy. Core never imports plugins."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(slots=True)
class EmailRequest:
    subject: str
    body_seed: str
    tone: str = "professional-warm"
    recipient_name: str | None = None
    sender_name: str | None = None
    variables: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class EmailDraft:
    subject: str
    body: str
    provider: str
    tokens_used: int = 0
    warnings: list[str] = field(default_factory=list)


class EmailPlugin(ABC):
    """Base for provider / tone / exporter plugins."""

    kind: str = "provider"

    @abstractmethod
    def spec(self) -> "PluginSpec": ...

    @abstractmethod
    def render(self, req: EmailRequest) -> EmailDraft: ...


class ExporterPlugin(Protocol):
    kind: str

    def export(self, draft: EmailDraft, out_dir: str) -> str: ...


@dataclass(slots=True, frozen=True)
class PluginSpec:
    name: str
    kind: str
    version: str
    author: str
    description: str = ""
    isolation: str = "inproc"
    capabilities: tuple[str, ...] = ()

    def as_row(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "kind": self.kind,
            "version": self.version,
            "author": self.author,
            "isolation": self.isolation,
        }