"""Thin HTTP client shared by network-backed provider plugins."""
from __future__ import annotations

import httpx
import os
import time

from studio.utils.logging import get_logger

log = get_logger(__name__)


class ProviderClient:
    def __init__(self, base_url: str, api_key_env: str, retries: int = 3) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = os.environ.get(api_key_env, "")
        self.retries = retries

    def post_json(self, path: str, payload: dict, timeout: float = 45.0) -> dict:
        if not self.api_key:
            raise RuntimeError("missing API key in environment")
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        last_exc: Exception | None = None
        for attempt in range(1, self.retries + 1):
            try:
                resp = httpx.post(
                    f"{self.base_url}{path}", json=payload,
                    headers=headers, timeout=timeout,
                )
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPError as exc:
                last_exc = exc
                backoff = 0.5 * (2 ** (attempt - 1))
                log.warning("provider retry %d in %.1fs: %s", attempt, backoff, exc)
                time.sleep(backoff)
        raise RuntimeError(f"provider call failed after {self.retries} tries") from last_exc