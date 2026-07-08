# Installation

Run from a checkout:

```bash
python -m ars_universal.cli --list
python -m ars_universal.cli codex install
python -m ars_universal.cli codex verify
```

Install for development:

```bash
python -m pip install -e .
ars codex install
ars codex verify
```

Install into a project-local target:

```bash
ars codex install --target ./.codex/skills
ars codex verify --target ./.codex/skills
ars agents install --target ./agent-skills/academic-research-skills
```

Preview writes:

```bash
ars claude install --dry-run
```

Every install writes `ars-universal.json`, `ars-command-map.json`, `ARS-INSTALL.md`, the upstream skill packages, and shared support files. Non-dry-run installs automatically call verification.
