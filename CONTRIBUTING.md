# Contributing to ai-email-generator-studio

Thanks for wanting to push on the generator. This repo is a plugin host —
the core stays small, the interesting stuff lives under `plugins/`.

## Ground rules

- Every plugin must subclass `EmailPlugin` from `host/contracts.py`.
- Plugins declare a `manifest.toml` alongside their module. The loader
  refuses anything without one.
- No plugin may mutate `host/` directly. Use the registry hooks.
- Python 3.12+ is the target. C++/C#/Java plugins are supported through
  the subprocess bridge in `host/bridges/`.

## Dev setup

```bash
python -m venv .venv
. .venv/Scripts/activate   # Windows
pip install -r requirements.txt
python -m studio.bootstrap --list-plugins
```

## Adding a provider plugin

1. Copy `plugins/providers/openai_provider/` to a new folder.
2. Rename the class, rewrite `manifest.toml`, keep the `render()` signature.
3. Register it in `config/plugins.toml` under `[enabled]`.
4. Run `pytest tests/`.

## Style

- `ruff` + `black`. Line length 100.
- Type hints on every public function. `mypy --strict` on `host/`.
- No bare `except:`. Log through `studio.utils.logging`.

## PR checklist

- [ ] New plugin has a manifest and a smoke test
- [ ] No new top-level deps without a note in the PR body
- [ ] `python -m studio.bootstrap --selfcheck` passes