"""Regression tests for Chapter 6 learning units."""

from __future__ import annotations

from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"


class Chapter06Tests(unittest.TestCase):
    def test_registry_closes_chapter_hours_and_paths(self) -> None:
        with UNITS.open("rb") as handle:
            by_id = {unit["id"]: unit for unit in tomllib.load(handle)["units"]}
        expected = {
            "u-02-06-01": ("极限怎样通过代数运算传递？", 2.00, 0.25, "limit-laws"),
            "u-02-06-02": ("序关系怎样给出极限估计？", 1.75, 0.25, "order-squeeze"),
            "u-02-06-03": ("误差如何穿过一次迭代？", 1.75, 0.50, "error-propagation"),
        }
        for unit_id, (title, theory, applied, suffix) in expected.items():
            with self.subTest(unit_id=unit_id):
                unit = by_id[unit_id]
                self.assertEqual(unit["chapter_id"], "chapter-06")
                self.assertEqual(unit["title"], title)
                self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (theory, applied))
                self.assertEqual(unit["path"], f"book/part-02/chapter-06/{unit_id}-{suffix}.qmd")

    def test_error_propagation_is_algebraic_not_calculus(self) -> None:
        content = (ROOT / "book/part-02/chapter-06/u-02-06-03-error-propagation.qmd").read_text(encoding="utf-8")
        self.assertIn(r"|g(x)-g(y)|=\frac{|x-y|}{(2+x)(2+y)}", content)
        self.assertIn("一次迭代", content)
        self.assertNotIn("g'(x)", content)
        self.assertNotIn("中值定理", content)


if __name__ == "__main__":
    unittest.main()
