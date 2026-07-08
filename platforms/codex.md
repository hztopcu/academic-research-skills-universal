# Codex

Status: stable

```bash
ars codex install
ars codex verify
```

The Codex adapter installs one bundled skill named `academic-research-suite`. That skill routes `ars-*` commands to the four bundled upstream skill packages.

Use a project-local target when testing:

```bash
ars codex install --target ./.codex/skills
ars codex verify --target ./.codex/skills
```
