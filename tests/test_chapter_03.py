"""Regression tests for Chapter 3 learning units."""

from __future__ import annotations

from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"
BOUNDS = ROOT / "book" / "part-01" / "chapter-03" / "u-01-03-01-bounds.qmd"


class Chapter03BoundsTests(unittest.TestCase):
    def test_bounds_unit_has_its_curriculum_contract(self) -> None:
        with UNITS.open("rb") as handle:
            registry = tomllib.load(handle)
        by_id = {unit["id"]: unit for unit in registry["units"]}

        unit = by_id["u-01-03-01"]
        self.assertEqual(unit["chapter_id"], "chapter-03")
        self.assertEqual(
            unit["path"], "book/part-01/chapter-03/u-01-03-01-bounds.qmd"
        )
        self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (1.50, 0.00))
        self.assertEqual(unit["capabilities"], ["concepts", "proof", "mathematical_expression"])
        self.assertEqual(unit["book_prerequisites"], ["chapter-02"])

    def test_bounds_unit_keeps_stable_definition_and_example_anchors(self) -> None:
        content = BOUNDS.read_text(encoding="utf-8")
        self.assertIn("### 上界、下界与确界 {#def-u-01-03-01-bounds}", content)
        self.assertIn("### 例：有理数中的缺失上确界 {#ex-u-01-03-01-rational-supremum}", content)

    def test_rational_upper_bound_argument_does_not_assume_strictness(self) -> None:
        content = BOUNDS.read_text(encoding="utf-8")
        self.assertIn("由于 $0\\in D$，有 $u\\ge0$", content)
        self.assertIn("若 $u\\in D$", content)
        self.assertIn("所以 $u\\notin D$ 且 $u\\ge0$，从而 $u>0$ 且 $u^2>2$", content)

    def test_bounds_unit_makes_chapter_two_its_explicit_prerequisite(self) -> None:
        content = BOUNDS.read_text(encoding="utf-8")
        self.assertIn(
            "[第 2 章：实数系与完备性公理](../../curriculum-map.qmd#chapter-02)",
            content,
        )
        self.assertIn("有理数缺口", content)
        self.assertIn("Dedekind 分割", content)


if __name__ == "__main__":
    unittest.main()
