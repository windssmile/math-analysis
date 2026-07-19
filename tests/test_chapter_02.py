"""Regression tests for Chapter 2 learning units."""

from __future__ import annotations

from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"
DEDEKIND_CUTS = ROOT / "book" / "part-01" / "chapter-02" / "u-01-02-02-dedekind-cuts.qmd"


class Chapter02RegistryTests(unittest.TestCase):
    def test_rational_gaps_unit_has_its_curriculum_contract(self) -> None:
        with UNITS.open("rb") as handle:
            registry = tomllib.load(handle)
        by_id = {unit["id"]: unit for unit in registry["units"]}

        unit = by_id["u-01-02-01"]
        self.assertEqual(unit["chapter_id"], "chapter-02")
        self.assertEqual(
            unit["path"], "book/part-01/chapter-02/u-01-02-01-rational-gaps.qmd"
        )
        self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (1.50, 0.00))
        self.assertEqual(
            unit["capabilities"],
            ["concepts", "proof", "mathematical_expression"],
        )

    def test_dedekind_cuts_unit_has_its_curriculum_contract(self) -> None:
        with UNITS.open("rb") as handle:
            registry = tomllib.load(handle)
        by_id = {unit["id"]: unit for unit in registry["units"]}

        unit = by_id["u-01-02-02"]
        self.assertEqual(unit["chapter_id"], "chapter-02")
        self.assertEqual(
            unit["path"], "book/part-01/chapter-02/u-01-02-02-dedekind-cuts.qmd"
        )
        self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (2.00, 0.25))
        self.assertEqual(
            unit["capabilities"],
            ["concepts", "proof", "mathematical_expression"],
        )

    def test_dedekind_cuts_keep_stable_definition_and_example_anchors(self) -> None:
        content = DEDEKIND_CUTS.read_text(encoding="utf-8")
        self.assertIn(
            "### Dedekind 分割 {#def-u-01-02-02-dedekind-cut}", content
        )
        self.assertIn(
            "### 例：$A_{\\sqrt2}$ 是一个 Dedekind 分割 "
            "{#ex-u-01-02-02-sqrt2-cut}",
            content,
        )


if __name__ == "__main__":
    unittest.main()
