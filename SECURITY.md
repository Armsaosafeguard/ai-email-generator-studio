# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.6.x   | yes       |
| 0.5.x   | yes       |
| < 0.5   | no        |

## Threat model

`ai-email-generator-studio` loads third-party plugin code in-process.
That is the entire point of the host architecture, and it is also the
entire attack surface.

- **Plugin code runs with host privileges.** Treat any plugin you did
  not write as untrusted. Sandboxing via `host/bridges/subprocess_bridge.py`
  is opt-in per manifest (`isolation = "subprocess"`).
- **API keys** live in `config/secrets.toml`, which is gitignored. Never
  commit a real key. The loader will refuse to start if it finds
  `sk-` prefixed strings in tracked files.
- **Prompt injection** is not treated as a security bug. The generator
  is a text tool. If a template renders hostile output, that is a
  content bug, file it as such.

## Reporting

Open a private security advisory on GitHub, or mail `security@` on the
repo domain. Include: version, plugin set, repro script, and whether
`isolation = "subprocess"` was set. We aim to triage within 72h.

## Out of scope

- Rate-limit evasion against provider APIs. That is your account, your
  problem.
- Deliverability of generated mail. The studio renders text; it does
  not send it.