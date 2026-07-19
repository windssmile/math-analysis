"""Regression tests for Chapter 1 learning units."""

from __future__ import annotations

from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"


class Chapter01RegistryTests(unittest.TestCase):
    def test_sets_unit_has_its_curriculum_contract(self) -> None:
        with UNITS.open("rb") as handle:
            registry = tomllib.load(handle)
        by_id = {unit["id"]: unit for unit in registry["units"]}

        unit = by_id["u-01-01-01"]
        self.assertEqual(unit["chapter_id"], "chapter-01")
        self.assertEqual(
            unit["path"], "book/part-01/chapter-01/u-01-01-01-sets.qmd"
        )
        self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (1.25, 0.25))
        self.assertEqual(
            unit["capabilities"],
            ["concepts", "proof", "mathematical_expression"],
        )


if __name__ == "__main__":
    unittest.main()
