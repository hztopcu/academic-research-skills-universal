from __future__ import annotations

from pathlib import Path
import json
import shutil

from .platforms import Platform, SKILL_DIRS, SUPPORT_DIRS


ROOT = Path(__file__).resolve().parent.parent


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
    return target


def ensure_assets() -> None:
    missing = [name for name in SKILL_DIRS if not (ROOT / name / "SKILL.md").exists()]
    if missing:
        names = ", ".join(missing)
        raise SystemExit(
            "Bundled skill assets are missing: "
            f"{names}. Run this CLI from the repository checkout or use an editable install."
        )


def install_multi_skill(target: Path, dry_run: bool) -> None:
    for name in SKILL_DIRS:
        copy_tree(ROOT / name, target / name, dry_run)
    copy_support(target, dry_run)


def install_portable_bundle(target: Path, dry_run: bool) -> None:
    for name in SKILL_DIRS:
        copy_tree(ROOT / name, target / "skills" / name, dry_run)
    copy_support(target, dry_run)
    write_text(target / "SKILL.md", portable_skill_md(), dry_run)


def install_codex_bundle(target: Path, dry_run: bool) -> None:
    bundle = target / "academic-research-suite"
    for name in SKILL_DIRS:
        copy_tree(ROOT / name, bundle / "skills" / name, dry_run)
    copy_support(bundle, dry_run)
    write_text(bundle / "SKILL.md", codex_skill_md(), dry_run)


def copy_support(target: Path, dry_run: bool) -> None:
    for name in SUPPORT_DIRS:
        src = ROOT / name
        if src.exists():
            copy_tree(src, target / name, dry_run)


def write_manifest(platform: Platform, target: Path, dry_run: bool) -> None:
    manifest = {
        "name": "academic-research-skills-universal",
        "version": "0.1.0",
        "platform": platform.key,
        "platform_label": platform.label,
        "install_kind": platform.install_kind,
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
