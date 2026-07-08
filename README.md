# Academic Research Skills Universal

Cross-platform installer and adapter layer for [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills).

This project is based on and extends Academic Research Skills by Cheng-I Wu. The goal is to make the research, writing, peer-review, and publication pipeline usable across more coding-agent platforms while preserving upstream attribution, methodology, and license terms.

## Status

Early adapter scaffold.

Implemented:

- Shared CLI: `ars <platform> install`
- Platform registry for Claude Code, Codex, Cursor, Aider, Gemini CLI, OpenCode, CodeBuddy, Kilo Code, Copilot, VS Code Copilot Chat, OpenClaw, Factory Droid, Trae, Trae CN, Hermes, Kimi Code, Amp, Agent Skills, Kiro, Pi, Devin, and Google Antigravity
- Codex bundled skill adapter
- Claude multi-skill adapter
- Cursor and VS Code instruction adapters
- Portable bundle fallback for platforms without a formal skill format
- Attribution manifest written at install time

Not yet guaranteed:

- Full subagent orchestration parity on every platform
- Platform-native marketplace publishing
- pipx/PyPI package-data hardening
- End-to-end tests inside every target agent

## Install From This Repository

For this first scaffold, run the CLI from the repository checkout or install it editable:

```bash
python -m ars_universal.cli --list
python -m ars_universal.cli codex install
python -m ars_universal.cli claude install
python -m ars_universal.cli cursor install
python -m ars_universal.cli install --platform kimi
```

Editable install:

```bash
python -m pip install -e .
ars codex install
```

Non-editable `pipx install git+...` packaging is planned, but not guaranteed in this first scaffold because the installer needs the bundled skill folders at runtime.

Use `--dry-run` to preview writes:

```bash
python -m ars_universal.cli codex install --dry-run
```

Use `--target` for project-local installs:

```bash
python -m ars_universal.cli codex install --target ./.codex/skills
python -m ars_universal.cli agents install --target ./agent-skills/academic-research-skills
```

## Platform Commands

| Platform | Command |
| --- | --- |
| Claude Code | `ars claude install` |
| CodeBuddy | `ars codebuddy install` |
| Codex | `ars codex install` |
| OpenCode | `ars opencode install` |
| Kilo Code | `ars kilo install` |
| GitHub Copilot CLI | `ars copilot install` |
| VS Code Copilot Chat | `ars vscode install` |
| Aider | `ars aider install` |
| OpenClaw | `ars claw install` |
| Factory Droid | `ars droid install` |
| Trae | `ars trae install` |
| Trae CN | `ars trae-cn install` |
| Cursor | `ars cursor install` |
| Gemini CLI | `ars gemini install` |
| Hermes | `ars hermes install` |
| Kimi Code | `ars install --platform kimi` |
| Amp | `ars amp install` |
| Agent Skills | `ars agents install` or `ars skills install` |
| Kiro IDE/CLI | `ars kiro install` |
| Pi coding agent | `ars pi install` |
| Devin CLI | `ars devin install` |
| Google Antigravity | `ars antigravity install` |

## How The Adapters Work

The upstream methodology is kept in four core skill packages:

- `deep-research`
- `academic-paper`
- `academic-paper-reviewer`
- `academic-pipeline`

Platform adapters only change packaging and routing. They do not rewrite the research protocols.

There are two support levels:

- **Portable skill support:** the platform can read the skill instructions and use the research workflows.
- **Orchestrated pipeline support:** the platform can also run subagents, file handoffs, hooks, or task orchestration close to Claude Code's native behavior.

Many platforms start at portable support. Full orchestration should be added platform by platform, with tests.

## Attribution

This project is based on:

- Academic Research Skills
- Author: Cheng-I Wu
- Repository: <https://github.com/Imbad0202/academic-research-skills>
- License: CC BY-NC 4.0

See [NOTICE.md](NOTICE.md) for attribution and modification notes.

## License

The upstream Academic Research Skills content is licensed under CC BY-NC 4.0. This adapter distribution preserves that license. Do not use it for commercial purposes unless you have appropriate permission from the upstream rights holder.
