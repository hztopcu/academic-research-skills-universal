# Academic Research Skills Universal

[![Tests](https://github.com/hztopcu/academic-research-skills-universal/actions/workflows/tests.yml/badge.svg)](https://github.com/hztopcu/academic-research-skills-universal/actions/workflows/tests.yml)

Academic Research Skills Universal is a cross-platform installer, adapter architecture, and validation suite for academic research workflows across coding-agent platforms.

It packages research, writing, peer-review, and publication-pipeline skills for Codex, Claude Code, VS Code, Cursor, Aider, and other agent environments. Upstream attribution and license details are recorded in [NOTICE.md](NOTICE.md).

This repository is not affiliated with, endorsed by, or maintained by the upstream author or by any platform vendor named below.

## Status

Early adapter scaffold. Treat platform support as installer support unless a platform is explicitly marked as end-to-end tested.

Implemented:

- Shared CLI: `ars <platform> install`
- Diagnostics CLI: `ars <platform> diagnose`
- Platform registry entries for Claude Code, Codex, Cursor, Aider, Gemini CLI, OpenCode, CodeBuddy, Kilo Code, Copilot, VS Code Copilot Chat, OpenClaw, Factory Droid, Trae, Trae CN, Hermes, Kimi Code, Amp, Agent Skills, Kiro, Pi, Devin, and Google Antigravity
- Codex bundled skill adapter
- Claude multi-skill adapter
- Cursor and VS Code instruction adapters
- Portable bundle fallback for platforms without a formal skill format
- Attribution manifest written at install time
- Install verification with `ars <platform> verify`

Not yet guaranteed:

- Full subagent orchestration parity on every platform
- Platform-native marketplace publishing
- End-to-end tests inside every target agent

## Support Matrix

| Level | Meaning |
| --- | --- |
| Stable | Installer output and verification are covered by automated tests in this repo. These are the first platforms targeted for local/manual E2E validation. |
| Experimental | Installer and verification are available, but the platform is still under testing and may need a native adapter. |

| Platform | Current level |
| --- | --- |
| Codex | Stable |
| Claude Code | Stable |
| VS Code Copilot Chat | Stable |
| Cursor | Stable |
| Aider | Stable |
| Agent Skills, Gemini CLI, OpenCode, CodeBuddy, Kilo Code, Copilot CLI, OpenClaw, Factory Droid, Trae, Trae CN, Hermes, Kimi Code, Amp, Kiro, Pi, Devin, Google Antigravity | Experimental |

Do not describe a platform as "fully supported" until it has a platform-specific adapter and an end-to-end manual test in that environment.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Installation](docs/INSTALLATION.md)
- [Platform support](docs/PLATFORM_SUPPORT.md)
- [Test matrix](docs/TEST_MATRIX.md)
- [Validation](docs/VALIDATION.md)
- [Release checklist](docs/RELEASE_CHECKLIST.md)
- [Changelog](CHANGELOG.md)
- [GitHub setup](docs/GITHUB_SETUP.md)
- Platform notes: [Codex](platforms/codex.md), [Claude Code](platforms/claude.md), [VS Code](platforms/vscode.md), [Cursor](platforms/cursor.md), [Aider](platforms/aider.md), [experimental platforms](platforms/experimental.md)

## Install From This Repository

```bash
python -m ars_universal.cli --list
python -m ars_universal.cli codex install
python -m ars_universal.cli codex verify
python -m ars_universal.cli codex diagnose
python -m ars_universal.cli claude install
python -m ars_universal.cli cursor install
python -m ars_universal.cli install --platform kimi
python -m ars_universal.cli verify --platform kimi
```

Editable install for development:

```bash
python -m pip install -e .
ars codex install
```

Regular package installs are supported by bundling the upstream skill assets under `ars_universal/assets/`.

Use `--dry-run` to preview writes:

```bash
python -m ars_universal.cli codex install --dry-run
```

Use `--target` for project-local installs:

```bash
python -m ars_universal.cli codex install --target ./.codex/skills
python -m ars_universal.cli codex verify --target ./.codex/skills
python -m ars_universal.cli agents install --target ./agent-skills/academic-research-skills
```

## Stable Platform Commands

| Platform | Command |
| --- | --- |
| Claude Code | `ars claude install` |
| Codex | `ars codex install` |
| VS Code Copilot Chat | `ars vscode install` |
| Aider | `ars aider install` |
| Cursor | `ars cursor install` |

## Experimental Platform Commands

These install a portable bundle and are under testing.

| Platform | Command |
| --- | --- |
| Agent Skills | `ars agents install` or `ars skills install` |
| Gemini CLI | `ars gemini install` |
| OpenCode | `ars opencode install` |
| CodeBuddy | `ars codebuddy install` |
| Kilo Code | `ars kilo install` |
| GitHub Copilot CLI | `ars copilot install` |
| OpenClaw | `ars claw install` |
| Factory Droid | `ars droid install` |
| Trae | `ars trae install` |
| Trae CN | `ars trae-cn install` |
| Hermes | `ars hermes install` |
| Kimi Code | `ars install --platform kimi` |
| Amp | `ars amp install` |
| Kiro IDE/CLI | `ars kiro install` |
| Pi coding agent | `ars pi install` |
| Devin CLI | `ars devin install` |
| Google Antigravity | `ars antigravity install` |

Every install runs verification automatically. You can also verify a target explicitly:

```bash
ars codex verify --target ./.codex/skills
ars verify --platform kimi --target ./tmp/kimi
```

## Test

```bash
python -m compileall ars_universal tests tools
python -m unittest discover -s tests
python -m pip install . --target tmp-install/pkg-test --no-deps --no-cache-dir
python tools/smoke_all_platforms.py --stable-only
python tools/smoke_all_platforms.py --all
python -m ars_universal.cli codex install --target tmp-install/codex
python -m ars_universal.cli codex verify --target tmp-install/codex
```

## How The Adapters Work

The upstream methodology is kept in four bundled skill packages under `ars_universal/assets/`:

- `deep-research`
- `academic-paper`
- `academic-paper-reviewer`
- `academic-pipeline`

Platform adapters only change packaging and routing. They do not rewrite the research protocols.

There are two support levels:

- **Portable skill support:** the platform can read the skill instructions and use the research workflows.
- **Orchestrated pipeline support:** the platform can also run subagents, file handoffs, hooks, or task orchestration close to Claude Code's native behavior.

Many platforms start at portable support. Full orchestration should be added platform by platform, with tests.

## License

The upstream Academic Research Skills content is licensed under CC BY-NC 4.0. This adapter distribution preserves that license. Do not use it for commercial purposes unless you have appropriate permission from the upstream rights holder.

See [NOTICE.md](NOTICE.md) for attribution and modification notes.

Creative Commons licenses are not software licenses in the usual package-manager sense, and the NonCommercial restriction can be interpreted differently across contexts. If you need commercial use, redistribution inside a paid product, marketplace publication, or institutional deployment, get permission from the upstream rights holder first.
