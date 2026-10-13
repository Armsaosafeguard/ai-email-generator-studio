from __future__ import annotations

from pathlib import Path

import pytest

from studio.host.loader import ManifestError, PluginLoader


def test_loader_rejects_missing_manifest(tmp_path: Path) -> None:
    loader = PluginLoader([tmp_path], strict=True)
    bad = tmp_path / "broken"
    bad.mkdir()
    (bad / "manifest.toml").write_text('name = "x"\nkind = "provider"\n', encoding="utf-8")
    with pytest.raises(ManifestError):
        list(loader.discover())


def test_loader_reads_valid_manifest(tmp_path: Path) -> None:
    loader = PluginLoader([tmp_path])
    good = tmp_path / "ok"
    good.mkdir()
    (good / "manifest.toml").write_text(
        'name = "ok"\nkind = "provider"\nversion = "0.1.0"\n'
        'author = "me"\nentry = "plugin.py"\nclass = "P"\n',
        encoding="utf-8",
    )
    (good / "plugin.py").write_text(
        "from studio.host.contracts import EmailPlugin, PluginSpec, EmailDraft, EmailRequest\n"
        "class P(EmailPlugin):\n"
        "    kind = 'provider'\n"
        "    def spec(self):