"""Contract tests for the machine-readable course outline."""

from __future__ import annotations

import copy
import unittest
from pathlib import Path

from scripts.check_outline import load_outline, validate_outline


ROOT = Path(__file__).resolve().parents[1]
OUTLINE = ROOT / "curriculum" / "outline.toml"


class OutlineValidationTests(unittest.TestCase):
    def load_outline(self) -> dict:
        return load_outline(OUTLINE)

    def test_real_outline_is_valid(self) -> None:
        self.assertEqual(validate_outline(self.load_outline()), [])

    def test_rejects_non_sequential_chapter_numbers(self) -> None:
        data = copy.deepcopy(self.load_outline())
        data["parts"][1]["chapters"][0]["number"] = 1
        self.assertIn(
            "chapter numbers must be exactly 1..54",
            validate_outline(data),
        )

    def test_rejects_incorrect_theory_hour_total(self) -> None:
        data = copy.deepcopy(self.load_outline())
        data["parts"][0]["theory_hours"] = 21
        self.assertIn(
            "theory hours must total 270, got 271",
            validate_outline(data),
        )

    def test_rejects_missing_guiding_question(self) -> None:
        data = copy.deepcopy(self.load_outline())
        data["parts"][0]["question"] = ""
        self.assertIn(
            "part-01 must have a guiding question",
            validate_outline(data),
        )


if __name__ == "__main__":
    unittest.main()
