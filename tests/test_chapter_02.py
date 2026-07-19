"""Regression tests for Chapter 2 learning units."""

from __future__ import annotations

from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"
DEDEKIND_CUTS = ROOT / "book" / "part-01" / "chapter-02" / "u-01-02-02-dedekind-cuts.qmd"
CUT_ORDER_OPERATIONS = (
    ROOT / "book" / "part-01" / "chapter-02" / "u-01-02-03-cut-order-operations.qmd"
)


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

    def test_cut_order_operations_unit_has_its_curriculum_contract(self) -> None:
        with UNITS.open("rb") as handle:
            registry = tomllib.load(handle)
        by_id = {unit["id"]: unit for unit in registry["units"]}

        unit = by_id["u-01-02-03"]
        self.assertEqual(unit["chapter_id"], "chapter-02")
        self.assertEqual(
            unit["path"],
            "book/part-01/chapter-02/u-01-02-03-cut-order-operations.qmd",
        )
        self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (1.50, 0.25))
        self.assertEqual(
            unit["capabilities"],
            ["concepts", "proof", "mathematical_expression"],
        )

    def test_chapter_02_has_three_units_with_closed_hours_and_qmd_paths(self) -> None:
        with UNITS.open("rb") as handle:
            registry = tomllib.load(handle)
        units = [unit for unit in registry["units"] if unit["chapter_id"] == "chapter-02"]

        self.assertEqual(len(units), 3)
        self.assertEqual(sum(unit["theory_hours"] for unit in units), 5.00)
        self.assertEqual(sum(unit["applied_hours"] for unit in units), 0.50)
        for unit in units:
            self.assertTrue((ROOT / unit["path"]).is_file())

    def test_cut_order_operations_keep_stable_definition_and_theorem_anchors(self) -> None:
        content = CUT_ORDER_OPERATIONS.read_text(encoding="utf-8")
        self.assertIn("### 切割的次序 {#def-u-01-02-03-cut-order}", content)
        self.assertIn("### 并集给出上确界 {#thm-u-01-02-03-union-supremum}", content)


if __name__ == "__main__":
    unittest.main()
