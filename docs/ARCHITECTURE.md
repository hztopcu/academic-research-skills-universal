# Architecture

Academic Research Skills Universal is a thin adapter layer around the upstream skill content. The core rule is simple: preserve the research methodology, change only the packaging needed by each agent platform.

## Layout

- `ars_universal/assets/` contains the bundled upstream skill packages and support files.
- `ars_universal/platforms.py` is the platform registry. It defines platform keys, aliases, default install locations, install kind, and support status.
- `ars_universal/installers.py` materializes platform-specific layouts and verifies the result.
- `ars_universal/cli.py` exposes `ars <platform> install`, `ars <platform> verify`, and `ars --list`.
- `tools/smoke_all_platforms.py` installs and verifies the stable or full platform matrix.
- `tests/` covers CLI behavior, installer behavior, and package integrity.

## Adapter Types

- `multi-skill`: installs each upstream skill as its own skill folder.
- `codex-bundle`: installs one Codex skill that routes to the bundled upstream skills.
- `rules-bundle`: installs a portable bundle plus editor rules.
- `vscode-instructions`: installs a portable bundle plus Copilot instructions.
- `portable-bundle`: installs neutral Markdown skill packages for platforms still under testing.

## Design Notes

The project borrows a useful product idea from `binary-husky/gpt_academic`: keep the system modular and backend-aware. In this repository that means a platform registry, clear support levels, repeatable smoke tests, and docs for each adapter path.

No code is copied from `gpt_academic`; the transferable idea is architectural discipline: plugins/adapters should be discoverable, testable, and documented.
