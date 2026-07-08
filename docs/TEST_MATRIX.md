# Test Matrix

## Automated

Run the local suite:

```bash
python -m compileall ars_universal tests tools
python -m unittest discover -s tests
python -m pip install . --target tmp-install/pkg-test --no-deps --no-cache-dir
python tools/smoke_all_platforms.py --stable-only
python tools/smoke_all_platforms.py --all
```

The smoke script installs each selected platform into an isolated temporary directory and then runs `verify_install`.

## Manual End-to-End

Manual end-to-end validation should be recorded per platform before moving it beyond experimental. Minimum checks:

- Install with the documented command.
- Start the target agent or editor.
- Ask for a literature review, outline, article draft, citation check, and review pass.
- Confirm the agent loads the intended skill package and follows the integrity gates.
- Save the date, platform version, and notes in a release checklist or issue.

## Current Local Smoke

A local Codex writing smoke was performed with a generated academic article draft under `tmp-install/local-article-test/`. The directory is intentionally ignored because it is a run artifact, not package source.
