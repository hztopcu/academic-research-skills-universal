from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "ars_universal.cli", *args],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_list_platforms(self) -> None:
        result = self.run_cli("--list")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("codex", result.stdout)
        self.assertIn("Claude Code", result.stdout)
        self.assertIn("stable", result.stdout)
        self.assertIn("experimental", result.stdout)

    def test_cli_installs_to_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_cli("codex", "install", "--target", tmp)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((Path(tmp) / "academic-research-suite" / "SKILL.md").exists())
            self.assertIn("Verification: OK", result.stdout)

            verify = self.run_cli("codex", "verify", "--target", tmp)
            self.assertEqual(verify.returncode, 0, verify.stderr)
            self.assertIn("Verification OK", verify.stdout)

    def test_platform_flag_form(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_cli("install", "--platform", "kimi", "--target", tmp)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((Path(tmp) / "SKILL.md").exists())

            verify = self.run_cli("verify", "--platform", "kimi", "--target", tmp)
            self.assertEqual(verify.returncode, 0, verify.stderr)


if __name__ == "__main__":
    unittest.main()
