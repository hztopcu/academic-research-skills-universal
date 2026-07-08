# VS Code Copilot Chat

Status: stable

```bash
ars vscode install
ars vscode verify
```

The VS Code adapter installs a portable bundle plus `copilot-instructions.md`. The instruction file points Copilot Chat to the bundled academic research skills.

Use a project-local target when you want the instructions scoped to one repository:

```bash
ars vscode install --target ./.vscode/academic-research-skills
```
