from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SmokeScriptTests(unittest.TestCase):
    def test_stable_smoke_script(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    "tools/smoke_all_platforms.py",
                    "--stable-only",
                    "--target-root",
                    tmp,
                ],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Smoke OK: 5 platform(s)", result.stdout)
            self.assertTrue((Path(tmp) / "codex" / "academic-research-suite" / "SKILL.md").exists())


if __name__ == "__main__":
    unittest.main()
