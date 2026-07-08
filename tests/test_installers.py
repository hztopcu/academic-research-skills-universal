from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from ars_universal.cli import normalize_invocation
from ars_universal.installers import install
from ars_universal.platforms import SKILL_DIRS, resolve_platform


class InstallerTests(unittest.TestCase):
    def test_resolves_skills_alias(self) -> None:
        platform = resolve_platform("skills")
        self.assertEqual(platform.key, "agents")

    def test_normalizes_platform_flag_invocation(self) -> None:
        self.assertEqual(
            normalize_invocation("install", "install", "kimi"),
            ("kimi", "install"),
        )

    def test_rejects_ambiguous_platform_flag_invocation(self) -> None:
        with self.assertRaises(SystemExit):
            normalize_invocation("codex", "install", "kimi")

    def test_codex_install_writes_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            install(resolve_platform("codex"), target=target)

            bundle = target / "academic-research-suite"
            self.assertTrue((bundle / "SKILL.md").exists())
            self.assertTrue((bundle / "commands" / "ars-plan.md").exists())
            for name in SKILL_DIRS:
                self.assertTrue((bundle / "skills" / name / "SKILL.md").exists())

            manifest = json.loads((target / "ars-universal.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["platform"], "codex")
            self.assertEqual(manifest["based_on"]["author"], "Cheng-I Wu")

    def test_claude_install_writes_individual_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            install(resolve_platform("claude"), target=target)

            for name in SKILL_DIRS:
                self.assertTrue((target / name / "SKILL.md").exists())
            self.assertTrue((target / "commands" / "ars-full.md").exists())

    def test_portable_install_writes_root_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            install(resolve_platform("kimi"), target=target)

            self.assertTrue((target / "SKILL.md").exists())
            for name in SKILL_DIRS:
                self.assertTrue((target / "skills" / name / "SKILL.md").exists())

            manifest = json.loads((target / "ars-universal.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["platform"], "kimi")


if __name__ == "__main__":
    unittest.main()
