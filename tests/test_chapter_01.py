"""Regression tests for Chapter 1 learning units."""

from __future__ import annotations

from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"


class Chapter01RegistryTests(unittest.TestCase):
    def test_quantifiers_unit_has_its_curriculum_contract(self) -> None:
        with UNITS.open("rb") as handle:
            registry = tomllib.load(handle)
        by_id = {unit["id"]: unit for unit in registry["units"]}

        unit = by_id["u-01-01-02"]
        self.assertEqual(unit["chapter_id"], "chapter-01")
        self.assertEqual(
            unit["path"], "book/part-01/chapter-01/u-01-01-02-quantifiers.qmd"
        )
        self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (1.25, 0.25))
        self.assertEqual(
            unit["capabilities"],
            ["concepts", "proof", "mathematical_expression"],
        )

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

    def test_powerset_example_uses_a_real_subset_of_its_base_set(self) -> None:
        content = (
            ROOT / "book/part-01/chapter-01/u-01-01-01-sets.qmd"
        ).read_text(encoding="utf-8")

        self.assertIn(
            r"$\{1,\{1\}\}\in\mathcal P(\{1,\{1\}\})$",
            content,
        )
        self.assertNotIn(
            r"$\{\varnothing,\{1\}\}\in\mathcal P(\{1,\{1\}\})$",
            content,
        )

    def test_quantifier_migration_distinguishes_divisibility_from_factors(self) -> None:
        content = (
            ROOT / "book/part-01/chapter-01/u-01-01-02-quantifiers.qmd"
        ).read_text(encoding="utf-8")

        self.assertIn("每个质数都整除 $0$", content)
        self.assertIn("质因子通常用于非零整数", content)

    def test_first_quantifier_exercise_uses_only_integer_addition(self) -> None:
        content = (
            ROOT / "book/part-01/chapter-01/u-01-01-02-quantifiers.qmd"
        ).read_text(encoding="utf-8")

        self.assertIn("每个整数都有一个相反数", content)
        self.assertIn(r"$(\forall n\in\mathbb Z)(\exists m\in\mathbb Z)\ n+m=0$", content)
        self.assertNotIn("每个实数都有一个不小于它的整数", content)


if __name__ == "__main__":
    unittest.main()
