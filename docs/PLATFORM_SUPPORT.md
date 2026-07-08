# Platform Support

Support levels are intentionally conservative.

| Level | Meaning |
| --- | --- |
| Stable | Installer output and verification are covered by automated tests in this repo. These platforms are first in line for manual end-to-end validation. |
| Experimental | Installer and verification are available, but the platform is still under testing and may need a native adapter. |

## Stable

| Platform | Command | Adapter |
| --- | --- | --- |
| Claude Code | `ars claude install` | `multi-skill` |
| Codex | `ars codex install` | `codex-bundle` |
| VS Code Copilot Chat | `ars vscode install` | `vscode-instructions` |
| Cursor | `ars cursor install` | `rules-bundle` |
| Aider | `ars aider install` | `portable-bundle` |

## Experimental

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

Do not call an experimental platform fully supported until it has a platform-specific adapter and manual end-to-end validation in that environment.
