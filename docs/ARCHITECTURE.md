# Architecture

Academic Research Skills Universal is a thin adapter layer around the upstream skill content. The core rule is simple: preserve the research methodology, change only the packaging needed by each agent platform.

## Layout

- `ars_universal/assets/` contains the bundled upstream skill packages and support files.
- `ars_universal/platforms.py` is the platform registry. It defines platform keys, aliases, default install locations, install kind, and support status.
- `ars_universal/adapters.py` contains adapter classes that materialize and verify platform-specific layouts.
- `ars_universal/installers.py` is a compatibility facade for the public installer API.
- `ars_universal/diagnostics.py` produces install health reports for `ars <platform> diagnose`.
- `ars_universal/cli.py` exposes `ars <platform> install`, `ars <platform> verify`, `ars <platform> diagnose`, and `ars --list`.
- `tools/smoke_all_platforms.py` installs and verifies the stable or full platform matrix.
- `tests/` covers CLI behavior, installer behavior, and package integrity.

## Adapter Types

- `multi-skill`: installs each upstream skill as its own skill folder.
- `codex-bundle`: installs one Codex skill that routes to the bundled upstream skills.
- `rules-bundle`: installs a portable bundle plus editor rules.
- `vscode-instructions`: installs a portable bundle plus Copilot instructions.
- `portable-bundle`: installs neutral Markdown skill packages for platforms still under testing.

## Diagnostics

`ars <platform> diagnose` reports the resolved target, support level, adapter class, manifest install kind, warnings, and verification errors. This gives users a single debugging command instead of making them infer which layout a platform uses.

