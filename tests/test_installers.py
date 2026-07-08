from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from ars_universal.cli import normalize_invocation
from ars_universal.diagnostics import diagnose_install
from ars_universal.installers import get_adapter, install, verify_install
from ars_universal.platforms import SKILL_DIRS, resolve_platform


class InstallerTests(unittest.TestCase):
    def test_resolves_skills_alias(self) -> None:
        platform = resolve_platform("skills")
        self.assertEqual(platform.key, "agents")

    def test_resolves_adapter_class(self) -> None:
        self.assertEqual(get_adapter(resolve_platform("codex")).__class__.__name__, "CodexBundleAdapter")
        self.assertEqual(get_adapter(resolve_platform("claude")).__class__.__name__, "MultiSkillAdapter")

    def test_normalizes_platform_flag_invocation(self) -> None:
        self.assertEqual(
            normalize_invocation("install", "install", "kimi"),
            ("kimi", "install"),
        )

    def test_normalizes_diagnose_platform_flag_invocation(self) -> None:
        self.assertEqual(
            normalize_invocation("diagnose", "install", "kimi"),
            ("kimi", "diagnose"),
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
            self.assertTrue((bundle / "ARS-INSTALL.md").exists())
            self.assertTrue((bundle / "ars-command-map.json").exists())
            self.assertTrue((bundle / "commands" / "ars-plan.md").exists())
            for name in SKILL_DIRS:
                self.assertTrue((bundle / "skills" / name / "SKILL.md").exists())

            manifest = json.loads((target / "ars-universal.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["platform"], "codex")
            self.assertEqual(manifest["status"], "stable")
            self.assertEqual(manifest["based_on"]["author"], "Cheng-I Wu")
            self.assertEqual(verify_install(resolve_platform("codex"), target=target), [])

    def test_claude_install_writes_individual_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            install(resolve_platform("claude"), target=target)

            for name in SKILL_DIRS:
                self.assertTrue((target / name / "SKILL.md").exists())
            self.assertTrue((target / "commands" / "ars-full.md").exists())
            self.assertEqual(verify_install(resolve_platform("claude"), target=target), [])

    def test_portable_install_writes_root_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            install(resolve_platform("kimi"), target=target)

            self.assertTrue((target / "SKILL.md").exists())
            for name in SKILL_DIRS:
                self.assertTrue((target / "skills" / name / "SKILL.md").exists())

            manifest = json.loads((target / "ars-universal.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["platform"], "kimi")
            self.assertEqual(verify_install(resolve_platform("kimi"), target=target), [])

    def test_verify_reports_missing_install(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            errors = verify_install(resolve_platform("codex"), target=Path(tmp))
            self.assertTrue(any("missing manifest" in error for error in errors))
            self.assertTrue(any("missing skill" in error for error in errors))

    def test_command_map_routes_known_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            install(resolve_platform("codex"), target=target)
            mapping = json.loads(
                (target / "academic-research-suite" / "ars-command-map.json").read_text(encoding="utf-8")
            )
            self.assertEqual(mapping["ars-reviewer"]["recommended_skill"], "academic-paper-reviewer")
            self.assertEqual(mapping["ars-full"]["recommended_skill"], "academic-pipeline")
            self.assertEqual(mapping["ars-lit-review"]["recommended_skill"], "deep-research")

    def test_diagnose_reports_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            install(resolve_platform("cursor"), target=target)
            diagnosis = diagnose_install(resolve_platform("cursor"), target=target)
            self.assertTrue(diagnosis.ok)
            self.assertEqual(diagnosis.adapter, "CursorRulesAdapter")
            self.assertEqual(diagnosis.manifest["adapter"], "CursorRulesAdapter")


if __name__ == "__main__":
    unittest.main()
