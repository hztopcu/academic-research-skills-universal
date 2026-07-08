# Release Checklist

Before publishing a release:

- Confirm README, NOTICE, license notes, and support tables are current.
- Run `python -m compileall ars_universal tests tools`.
- Run `python -m unittest discover -s tests`.
- Run `python tools/smoke_all_platforms.py --stable-only`.
- Run `python tools/smoke_all_platforms.py --all`.
- Run `python -m pip install . --target tmp-install/pkg-release --no-deps --no-cache-dir`.
- Install and verify at least Codex, Claude Code, VS Code, Cursor, and Aider locally when possible.
- Check `git status --short` for accidental build artifacts.
- Create a tag and release notes that mention upstream attribution and support-level changes.
