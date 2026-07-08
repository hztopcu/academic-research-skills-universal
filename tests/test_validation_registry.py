from __future__ import annotations

import json
import unittest
from pathlib import Path

from ars_universal.platforms import PLATFORMS


ROOT = Path(__file__).resolve().parents[1]
VALID_STATUSES = {
    "partial-local",
    "environment-detected",
    "blocked-not-installed",
    "pending-external",
}


class ValidationRegistryTests(unittest.TestCase):
    def test_every_platform_has_validation_entry(self) -> None:
        registry = json.loads((ROOT / "validation" / "platform-validation.json").read_text(encoding="utf-8"))
        entries = registry["platforms"]
        self.assertEqual(set(entries), set(PLATFORMS))

    def test_validation_entries_have_required_fields(self) -> None:
        registry = json.loads((ROOT / "validation" / "platform-validation.json").read_text(encoding="utf-8"))
        for key, entry in registry["platforms"].items():
            with self.subTest(platform=key):
                self.assertEqual(entry["automated_install_smoke"], "passed")
                self.assertIn(entry["manual_e2e"], VALID_STATUSES)
                self.assertTrue(entry["evidence"])


if __name__ == "__main__":
    unittest.main()
