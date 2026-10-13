"""Entry point. Boots the host, loads plugins, opens the compose view."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from studio.host.host import PluginHost
from studio.utils.logging import get_logger
from studio.utils.paths import repo_root

log = get_logger(__name__)


def build_host() -> PluginHost:
    root = repo_root()
    host = PluginHost(
        config_path=root / "config" / "settings.toml",
        plugin_map=root / "config" / "plugins.toml",
    )
    host.discover()
    host.load_all()
    return host


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ai-email-generator-studio")
    parser.add_argument("--list-plugins", action="store_true")
    parser.add_argument("--selfcheck", action="store_true")
    parser.add_argument("--compose", metavar="TEMPLATE")
    args = parser.parse_args(argv)

    host = build_host()

    if args.list_plugins:
        for spec in host.registry.all_specs():
            print(f"{spec.name:<24} {spec.kind:<10} v{spec.version}")
        return 0

    if args.selfcheck:
        ok = host.selfcheck()
        log.info("selfcheck", extra={"ok": ok, "plugins": len(host.registry)})
        return 0 if ok else 1

    if args.compose:
        from studio.ui.compose_view import ComposeView
        ComposeView(host).run(template=args.compose)
        return 0

    from studio.ui.main_window import MainWindow
    MainWindow(host).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())