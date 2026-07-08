from __future__ import annotations

from pathlib import Path
import json
import shutil

from .platforms import Platform, SKILL_DIRS, SUPPORT_DIRS


ASSET_ROOT = Path(__file__).resolve().parent / "assets"
COMMAND_PREFIX = "ars-"


def copy_tree(src: Path, dst: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"would copy {src} -> {dst}")
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def write_text(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        print(f"would write {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def install(platform: Platform, target: Path | None = None, dry_run: bool = False) -> Path:
    ensure_assets()
    target = (target or platform.default_target()).expanduser().resolve()
    if not dry_run:
        target.mkdir(parents=True, exist_ok=True)

    if platform.install_kind == "multi-skill":
        install_multi_skill(target, dry_run)
    elif platform.install_kind == "codex-bundle":
        install_codex_bundle(target, dry_run)
    elif platform.install_kind == "rules-bundle":
        install_portable_bundle(target, dry_run)
        write_cursor_rule(target, dry_run)
    elif platform.install_kind == "vscode-instructions":
        install_portable_bundle(target, dry_run)
        write_vscode_instructions(target, dry_run)
    else:
        install_portable_bundle(target, dry_run)

    write_manifest(platform, target, dry_run)
    if not dry_run:
        errors = verify_install(platform, target)
        if errors:
            joined = "\n".join(f"- {error}" for error in errors)
            raise SystemExit(f"Install verification failed for {platform.label}:\n{joined}")
    return target


def ensure_assets() -> None:
    missing = [name for name in SKILL_DIRS if not (ASSET_ROOT / name / "SKILL.md").exists()]
    if missing:
        names = ", ".join(missing)
        raise SystemExit(
            "Bundled skill assets are missing: "
            f"{names}. Reinstall the package or run from a complete repository checkout."
        )


def install_multi_skill(target: Path, dry_run: bool) -> None:
    for name in SKILL_DIRS:
        copy_tree(ASSET_ROOT / name, target / name, dry_run)
    copy_support(target, dry_run)
    write_text(target / "ars-command-map.json", json.dumps(command_map(), indent=2) + "\n", dry_run)
    write_text(target / "ARS-INSTALL.md", install_notes_md("claude"), dry_run)


def install_portable_bundle(target: Path, dry_run: bool) -> None:
    for name in SKILL_DIRS:
        copy_tree(ASSET_ROOT / name, target / "skills" / name, dry_run)
    copy_support(target, dry_run)
    write_text(target / "SKILL.md", portable_skill_md(), dry_run)
    write_text(target / "ars-command-map.json", json.dumps(command_map(), indent=2) + "\n", dry_run)
    write_text(target / "ARS-INSTALL.md", install_notes_md("portable"), dry_run)


def install_codex_bundle(target: Path, dry_run: bool) -> None:
    bundle = target / "academic-research-suite"
    for name in SKILL_DIRS:
        copy_tree(ASSET_ROOT / name, bundle / "skills" / name, dry_run)
    copy_support(bundle, dry_run)
    write_text(bundle / "SKILL.md", codex_skill_md(), dry_run)
    write_text(bundle / "ars-command-map.json", json.dumps(command_map(), indent=2) + "\n", dry_run)
    write_text(bundle / "ARS-INSTALL.md", install_notes_md("codex"), dry_run)


def copy_support(target: Path, dry_run: bool) -> None:
    for name in SUPPORT_DIRS:
        src = ASSET_ROOT / name
        if src.exists():
            copy_tree(src, target / name, dry_run)


def write_manifest(platform: Platform, target: Path, dry_run: bool) -> None:
    manifest = {
        "name": "academic-research-skills-universal",
        "version": "0.1.0",
        "platform": platform.key,
        "platform_label": platform.label,
        "install_kind": platform.install_kind,
        "status": platform.status,
        "based_on": {
            "name": "academic-research-skills",
            "author": "Cheng-I Wu",
            "repository": "https://github.com/Imbad0202/academic-research-skills",
            "license": "CC-BY-NC-4.0",
        },
        "skills": list(SKILL_DIRS),
        "notes": list(platform.notes),
    }
    write_text(
        target / "ars-universal.json",
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        dry_run,
    )


def command_map() -> dict[str, dict[str, str]]:
    commands_dir = ASSET_ROOT / "commands"
    mapping: dict[str, dict[str, str]] = {}
    for command_file in sorted(commands_dir.glob(f"{COMMAND_PREFIX}*.md")):
        command = command_file.stem
        mapping[command] = {
            "command_file": f"commands/{command_file.name}",
            "recommended_skill": recommended_skill_for_command(command),
        }
    return mapping


def recommended_skill_for_command(command: str) -> str:
    if command in {"ars-reviewer", "ars-rebuttal-audit"}:
        return "academic-paper-reviewer"
    if command in {"ars-full"}:
        return "academic-pipeline"
    if command in {"ars-lit-review"}:
        return "deep-research"
    return "academic-paper"


def verify_install(platform: Platform, target: Path | None = None) -> list[str]:
    ensure_assets()
    target = (target or platform.default_target()).expanduser().resolve()
    errors: list[str] = []

    manifest_path = target / "ars-universal.json"
    if not manifest_path.exists():
        errors.append(f"missing manifest: {manifest_path}")
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid manifest JSON: {exc}")
        else:
            if manifest.get("platform") != platform.key:
                errors.append(f"manifest platform mismatch: expected {platform.key}, got {manifest.get('platform')}")

    if platform.install_kind == "codex-bundle":
        base = target / "academic-research-suite"
        skill_base = base / "skills"
        support_base = base
        required = [base / "SKILL.md", base / "ARS-INSTALL.md", base / "ars-command-map.json"]
    elif platform.install_kind == "multi-skill":
        base = target
        skill_base = target
        support_base = target
        required = [target / "ARS-INSTALL.md", target / "ars-command-map.json"]
    else:
        base = target
        skill_base = target / "skills"
        support_base = target
        required = [target / "SKILL.md", target / "ARS-INSTALL.md", target / "ars-command-map.json"]

    for path in required:
        if not path.exists():
            errors.append(f"missing required file: {path}")

    for name in SKILL_DIRS:
        skill_file = skill_base / name / "SKILL.md"
        if not skill_file.exists():
            errors.append(f"missing skill: {skill_file}")

    for name in SUPPORT_DIRS:
        if not (support_base / name).exists():
            errors.append(f"missing support directory: {support_base / name}")

    if platform.install_kind == "rules-bundle" and not (base / "academic-research-skills.mdc").exists():
        errors.append(f"missing Cursor rule file: {base / 'academic-research-skills.mdc'}")
    if platform.install_kind == "vscode-instructions" and not (base / "copilot-instructions.md").exists():
        errors.append(f"missing VS Code instructions file: {base / 'copilot-instructions.md'}")

    command_map_path = required[-1]
    if command_map_path.exists():
        try:
            mapping = json.loads(command_map_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid command map JSON: {exc}")
        else:
            for command, info in mapping.items():
                command_file = support_base / info.get("command_file", "")
                recommended = info.get("recommended_skill", "")
                if not command_file.exists():
                    errors.append(f"command {command} points to missing file: {command_file}")
                if recommended not in SKILL_DIRS:
                    errors.append(f"command {command} has unknown recommended skill: {recommended}")

    return errors


def portable_skill_md() -> str:
    return """---
name: academic-research-skills
description: "Portable Academic Research Skills bundle: deep research, paper writing, peer review, and research-to-publication pipeline. Based on Imbad0202/academic-research-skills."
---

# Academic Research Skills - Portable Bundle

Use the skill packages under `skills/`:

- `deep-research`
- `academic-paper`
- `academic-paper-reviewer`
- `academic-pipeline`

Start with `academic-pipeline` for an end-to-end research -> write -> review -> revise workflow. Use individual skills when your platform does not support multi-agent orchestration.

Attribution: based on Academic Research Skills by Cheng-I Wu, https://github.com/Imbad0202/academic-research-skills, licensed CC BY-NC 4.0.
"""


def codex_skill_md() -> str:
    return """---
name: academic-research-suite
description: "Codex bundle for Academic Research Skills. Aliases: ars-plan, ars-full, ars-lit-review, ars-reviewer, ars-revision, ars-citation-check, ars-format-convert."
---

# Academic Research Suite

Route requests to the bundled skills in `skills/`:

- Planning, outlines, paper writing, revisions, abstracts, citation checks, and format conversion: `skills/academic-paper/SKILL.md`
- Literature reviews, systematic review, and deep research: `skills/deep-research/SKILL.md`
- Peer review and rebuttal audit: `skills/academic-paper-reviewer/SKILL.md`
- End-to-end research -> write -> review -> revise -> finalize: `skills/academic-pipeline/SKILL.md`

When the user invokes an `ars-*` alias, load the matching command file from `commands/` and then the appropriate skill package. Preserve the human-in-the-loop checkpoints and integrity gates from the upstream methodology.

Attribution: based on Academic Research Skills by Cheng-I Wu, https://github.com/Imbad0202/academic-research-skills, licensed CC BY-NC 4.0.
"""


def install_notes_md(kind: str) -> str:
    if kind == "codex":
        layout = "`academic-research-suite/` is a single Codex skill bundle. Load `SKILL.md` first, then route `ars-*` requests through `ars-command-map.json`."
    elif kind == "claude":
        layout = "Each upstream skill is installed as its own folder. Shared commands and support files are installed next to them."
    else:
        layout = "This is a portable bundle. Platforms without native skill discovery should load the root `SKILL.md` and then route to `skills/<name>/SKILL.md`."

    return f"""# Academic Research Skills Universal Install

{layout}

## Required files

- `ars-universal.json`: install manifest and attribution record
- `ars-command-map.json`: maps `ars-*` command aliases to command files and recommended skills
- `commands/`: upstream command prompts
- `shared/`: shared contracts, templates, and references
- `scripts/`: upstream helper scripts

## Verification

Run:

```bash
ars verify --platform PLATFORM --target PATH
```

or:

```bash
python -m ars_universal.cli verify --platform PLATFORM --target PATH
```
"""


def write_cursor_rule(target: Path, dry_run: bool) -> None:
    write_text(
        target / "academic-research-skills.mdc",
        """---
description: Academic Research Skills routing and usage
globs:
  - "**/*"
alwaysApply: false
---

Use the bundled Academic Research Skills content in this directory when the user asks for literature review, academic writing, paper review, citation checks, rebuttal audit, or a research-to-publication pipeline.

Prefer `skills/academic-pipeline/SKILL.md` for end-to-end workflows. Use individual skill packages for focused tasks.
""",
        dry_run,
    )


def write_vscode_instructions(target: Path, dry_run: bool) -> None:
    write_text(
        target / "copilot-instructions.md",
        """# Academic Research Skills

Use this folder as a local instruction bundle for academic research workflows.

- End-to-end pipeline: `skills/academic-pipeline/SKILL.md`
- Deep literature review: `skills/deep-research/SKILL.md`
- Paper writing: `skills/academic-paper/SKILL.md`
- Peer review: `skills/academic-paper-reviewer/SKILL.md`

The bundle is based on Imbad0202/academic-research-skills and remains under CC BY-NC 4.0.
""",
        dry_run,
    )
