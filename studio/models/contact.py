"""Recipient record used by the batch composer."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Contact:
    email: str
    first_name: str = ""
    last_name: str = ""
    company: str = ""
    notes: str = ""

    @property
    def display(self) -> str:
        full = f"{self.first_name} {self.last_name}".strip()
        return full or self.email

    def as_vars(self) -> dict[str, str]:
        return {
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "company": self.company,
        }