"""Rough token counter for the UI meter. Not a real tokenizer — heuristic."""
from __future__ import annotations


class TokenMeter:
    CHARS_PER_TOKEN = 4.0

    def __init__(self, hard_cap: int = 900) -> None:
        self.hard_cap = hard_cap

    def count(self, text: str) -> int:
        return int(len(text) / self.CHARS_PER_TOKEN)

    def over_budget(self, text: str) -> bool:
        return self.count(text) > self.hard_cap

    def pct(self, text: str) -> float:
        return min(1.0, self.count(text) / self.hard_cap)