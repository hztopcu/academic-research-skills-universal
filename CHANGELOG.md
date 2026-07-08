# Changelog

## v0.1.0 - 2026-07-08

First public release of Academic Research Skills Universal.

### Added

- Cross-platform `ars` CLI for install, verify, diagnose, and platform listing.
- Adapter architecture for Codex, Claude Code, VS Code Copilot Chat, Cursor, Aider, and portable agent bundles.
- Platform registry covering 22 coding-agent environments.
- Install-time manifest and command map generation.
- Automated install verification for all registered platforms.
- Full platform smoke script: `tools/smoke_all_platforms.py`.
- GitHub Actions test matrix for Python 3.10, 3.11, and 3.12.
- Validation registry for automated smoke status and manual E2E status.
- GitHub issue template for external platform validation reports.
- Documentation for architecture, installation, platform support, validation, testing, release process, and GitHub setup.

### Support Status

- Stable installer support: Codex, Claude Code, VS Code Copilot Chat, Cursor, Aider.
- Experimental installer support: Agent Skills, Gemini CLI, OpenCode, CodeBuddy, Kilo Code, GitHub Copilot CLI, OpenClaw, Factory Droid, Trae, Trae CN, Hermes, Kimi Code, Amp, Kiro IDE/CLI, Pi coding agent, Devin CLI, Google Antigravity.

### Validation

- Local unit tests passed.
- Full installer smoke passed for all 22 registered platforms.
- GitHub Actions passed before release.
- Manual runtime E2E remains tracked separately in `validation/platform-validation.json`.

### Attribution And License

Upstream attribution and license details are recorded in `NOTICE.md`. The bundled upstream skill content remains under CC BY-NC 4.0.
