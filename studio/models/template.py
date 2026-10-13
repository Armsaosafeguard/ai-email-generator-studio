"""Jinja-backed email template with variable validation."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment, StrictUndefined, TemplateError


@dataclass(slots=True)
class EmailTemplate:
    name: str
    body: str
    subject: str
    variables: tuple[str, ...] = ()

    @classmethod
    def load(cls, path: Path) -> "EmailTemplate":
        env = Environment(undefined=StrictUndefined)
        raw = path.read_text(encoding="utf-8")
        subject, _, body = raw.partition("\n---\n")
        tmpl = env.from_string(body)
        declared = tuple(env.from_string(body).find_undeclared_variables(True))
        return cls(name=path.stem, body=body, subject=subject.strip(), variables=declared)

    def render(self, variables: dict[str, str]) -> tuple[str, str]:
        env = Environment(undefined=StrictUndefined)
        try:
            body = env.from_string(self.body).render(**variables)
        except TemplateError as exc:
            raise ValueError(f"template {self.name}: {exc}") from exc
        return self.subject, body