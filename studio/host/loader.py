"""Discovers plugin folders, validates manifests, imports modules."""
from __future__ import annotations

import importlib.util
import tomllib
from pathlib import Path

from studio.host.contracts import PluginSpec
from studio.utils.logging import get_logger

log = get_logger(__name__)

REQUIRED_MANIFEST_KEYS = {"name", "kind", "version", "author", "entry"}


class ManifestError(RuntimeError):
    pass


class PluginLoader:
    def __init__(self, plugin_dirs: list[Path], strict: bool = True) -> None:
        self.plugin_dirs = plugin_dirs
        self.strict = strict

    def iter_manifests(self):
        for base in self.plugin_dirs:
            if not base.exists():
                continue
            for manifest in base.glob("*/manifest.toml"):
                yield manifest

    def read_manifest(self, path: Path) -> dict:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        missing = REQUIRED_MANIFEST_KEYS - data.keys()
        if missing:
            raise ManifestError(f"{path}: missing keys {sorted(missing)}")
        return data

    def load_module(self, manifest_path: Path, manifest: dict):
        entry = manifest_path.parent / manifest["entry"]
        if not entry.exists():
            raise ManifestError(f"entry not found: {entry}")
        spec = importlib.util.spec_from_file_location(
            f"studio_plugin_{manifest['name']}", entry
        )
        if spec is None or spec.loader is None:
            raise ManifestError(f"cannot import {entry}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def discover(self) -> list[tuple[PluginSpec, dict]]:
        found: list[tuple[PluginSpec, dict]] = []
        for manifest_path in self.iter_manifests():
            try:
                manifest = self.read_manifest(manifest_path)
            except ManifestError as exc:
                if self.strict:
                    raise
                log.warning("skipping manifest: %s", exc)
                continue
            module = self.load_module(manifest_path, manifest)
            plugin_cls = getattr(module, manifest["class"], None)
            if plugin_cls is None:
                raise ManifestError(f"{manifest_path}: class {manifest['class']} missing")
            instance = plugin_cls()
            found.append((instance.spec(), {"instance": instance, "manifest": manifest}))
        return found