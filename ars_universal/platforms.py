from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


SKILL_DIRS = (
    "deep-research",
    "academic-paper",
    "academic-paper-reviewer",
    "academic-pipeline",
)

SUPPORT_DIRS = (
    "shared",
    "scripts",
    "commands",
)


@dataclass(frozen=True)
class Platform:
    key: str
    label: str
    default_subdir: str
    install_kind: str
    status: str = "experimental"
    aliases: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()

    def default_target(self) -> Path:
        home = Path.home()
        return Path(os.path.expandvars(str(home / self.default_subdir))).expanduser()


PLATFORMS: dict[str, Platform] = {
    "claude": Platform(
        key="claude",
        label="Claude Code",
        default_subdir=".claude/skills",
        install_kind="multi-skill",
        status="stable",
        notes=(
            "Installs the four upstream skills as separate Claude Code skills.",
            "Claude-specific plugin and hook behavior remains upstream-native.",
        ),
    ),
    "codex": Platform(
        key="codex",
        label="Codex",
        default_subdir=".codex/skills",
        install_kind="codex-bundle",
        status="stable",
        notes=(
            "Installs one bundled skill named academic-research-suite with ars-* aliases.",
            "Full multi-agent parity depends on the active Codex runtime capabilities.",
        ),
    ),
    "agents": Platform(
        key="agents",
        label="Agent Skills",
        default_subdir=".agent-skills/academic-research-skills",
        install_kind="portable-bundle",
        aliases=("skills",),
        notes=("Installs a neutral bundle for agents that read SKILL.md packages.",),
    ),
    "cursor": Platform(
        key="cursor",
        label="Cursor",
        default_subdir=".cursor/rules/academic-research-skills",
        install_kind="rules-bundle",
        status="stable",
        notes=("Installs Markdown rules that point Cursor at the bundled skill content.",),
    ),
    "aider": Platform(
        key="aider",
        label="Aider",
        default_subdir=".aider/academic-research-skills",
        install_kind="portable-bundle",
        status="stable",
        notes=("Installs reusable prompts and a recommended include file.",),
    ),
    "gemini": Platform(
        key="gemini",
        label="Gemini CLI",
        default_subdir=".gemini/academic-research-skills",
        install_kind="portable-bundle",
    ),
    "opencode": Platform(
        key="opencode",
        label="OpenCode",
        default_subdir=".opencode/skills/academic-research-skills",
        install_kind="portable-bundle",
    ),
    "codebuddy": Platform(
        key="codebuddy",
        label="CodeBuddy",
        default_subdir=".codebuddy/skills/academic-research-skills",
        install_kind="portable-bundle",
    ),
    "kilo": Platform(
        key="kilo",
        label="Kilo Code",
        default_subdir=".kilo/skills/academic-research-skills",
        install_kind="portable-bundle",
    ),
    "copilot": Platform(
        key="copilot",
        label="GitHub Copilot CLI",
        default_subdir=".copilot/skills/academic-research-skills",
        install_kind="portable-bundle",
    ),
    "vscode": Platform(
        key="vscode",
        label="VS Code Copilot Chat",
        default_subdir=".vscode/academic-research-skills",
        install_kind="vscode-instructions",
        status="stable",
    ),
    "claw": Platform(
        key="claw",
        label="OpenClaw",
        default_subdir=".openclaw/skills/academic-research-skills",
        install_kind="portable-bundle",
    ),
    "droid": Platform(
        key="droid",
        label="Factory Droid",
        default_subdir=".factory-droid/skills/academic-research-skills",
        install_kind="portable-bundle",
    ),
    "trae": Platform(
        key="trae",
        label="Trae",
        default_subdir=".trae/skills/academic-research-skills",
        install_kind="portable-bundle",
    ),
    "trae-cn": Platform(
        key="trae-cn",
        label="Trae CN",
        default_subdir=".trae-cn/skills/academic-research-skills",
        install_kind="portable-bundle",
    ),
    "hermes": Platform(
        key="hermes",
        label="Hermes",
        default_subdir=".hermes/skills/academic-research-skills",
        install_kind="portable-bundle",
    ),
    "kimi": Platform(
        key="kimi",
        label="Kimi Code",
        default_subdir=".kimi/skills/academic-research-skills",
        install_kind="portable-bundle",
    ),
    "amp": Platform(
        key="amp",
        label="Amp",
        default_subdir=".amp/skills/academic-research-skills",
        install_kind="portable-bundle",
    ),
    "kiro": Platform(
        key="kiro",
        label="Kiro IDE/CLI",
        default_subdir=".kiro/skills/academic-research-skills",
        install_kind="portable-bundle",
    ),
    "pi": Platform(
        key="pi",
        label="Pi coding agent",
        default_subdir=".pi/skills/academic-research-skills",
        install_kind="portable-bundle",
    ),
    "devin": Platform(
        key="devin",
        label="Devin CLI",
        default_subdir=".devin/skills/academic-research-skills",
        install_kind="portable-bundle",
    ),
    "antigravity": Platform(
        key="antigravity",
        label="Google Antigravity",
        default_subdir=".antigravity/skills/academic-research-skills",
        install_kind="portable-bundle",
    ),
}


ALIASES = {
    alias: platform.key
    for platform in PLATFORMS.values()
    for alias in platform.aliases
}


def resolve_platform(value: str) -> Platform:
    key = ALIASES.get(value, value)
    try:
        return PLATFORMS[key]
    except KeyError as exc:
        supported = ", ".join(sorted(PLATFORMS))
        raise SystemExit(f"Unknown platform '{value}'. Supported platforms: {supported}") from exc
