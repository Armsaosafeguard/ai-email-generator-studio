"""Runs an isolated plugin binary over stdio JSON. Used when a manifest
sets `isolation = "subprocess"`. Binary speaks one JSON request per line."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from studio.host.contracts import EmailDraft, EmailRequest
from studio.utils.logging import get_logger

log = get_logger(__name__)


class SubprocessBridge:
    def __init__(self, binary: Path, timeout: float = 30.0) -> None:
        self.binary = binary
        self.timeout = timeout

    def render(self, req: EmailRequest) -> EmailDraft:
        payload = json.dumps({
            "subject": req.subject,
            "body_seed": req.body_seed,
            "tone": req.tone,
            "variables": req.variables,
        })
        proc = subprocess.run(
            [str(self.binary)],
            input=payload,
            capture_output=True,
            text=True,
            timeout=self.timeout,
        )
        if proc.returncode != 0:
            log.error("bridge failed", extra={"stderr": proc.stderr.strip()})
            raise RuntimeError(f"bridge {self.binary.name} exited {proc.returncode}")
        out = json.loads(proc.stdout)
        return EmailDraft(
            subject=out.get("subject", req.subject),
            body=out["body"],
            provider=f"bridge:{self.binary.name}",
            tokens_used=out.get("tokens_used", 0),
        )