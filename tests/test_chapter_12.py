"""Regression tests for Chapter 12 learning-unit registration."""

from __future__ import annotations

from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"


class Chapter12Tests(unittest.TestCase):
    def test_registry_closes_chapter_hours_and_paths(self) -> None:
        with UNITS.open("rb") as handle:
            by_id = {unit["id"]: unit for unit in tomllib.load(handle)["units"]}
        expected = {
            "u-03-12-01": ("连续函数怎样保证取遍中间值？", 1.60, 0.40, "intermediate-value-theorem"),
            "u-03-12-02": ("怎样把有根证明变成误差可证的算法？", 1.50, 0.50, "certified-bisection"),
            "u-03-12-03": ("有固定点是否意味着简单迭代会收敛？", 1.50, 0.50, "fixed-points-and-iteration"),
        }
        for unit_id, (title, theory, applied, suffix) in expected.items():
            with self.subTest(unit_id=unit_id):
                unit = by_id[unit_id]
                self.assertEqual(unit["chapter_id"], "chapter-12")
                self.assertEqual(unit["title"], title)
                self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (theory, applied))
                self.assertEqual(unit["path"], f"book/part-03/chapter-12/{unit_id}-{suffix}.qmd")

    def test_existence_and_algorithm_pages_keep_the_confirmed_scope(self) -> None:
        ivt = (ROOT / "book/part-03/chapter-12/u-03-12-01-intermediate-value-theorem.qmd").read_text(encoding="utf-8")
        bisection = (ROOT / "book/part-03/chapter-12/u-03-12-02-certified-bisection.qmd").read_text(encoding="utf-8")
        fixed_point = (ROOT / "book/part-03/chapter-12/u-03-12-03-fixed-points-and-iteration.qmd").read_text(encoding="utf-8")

        for marker in ("thm-u-03-12-01-intermediate-value", "thm-u-03-12-01-zero"):
            self.assertIn(marker, ivt)
        for marker in ("alg-u-03-12-02-bisection", "thm-u-03-12-02-bisection-error"):
            self.assertIn(marker, bisection)
        self.assertIn("先验误差上界", bisection)
        self.assertIn("mathbook_examples.bisection", bisection)
        self.assertIn("残差", bisection)
        self.assertIn("thm-u-03-12-03-fixed-point", fixed_point)
        self.assertIn(r"x_{n+1}=1-x_n", fixed_point)
        self.assertIn("唯一不动点", fixed_point)
        self.assertIn("压缩映射定理", fixed_point)
        for page in (ivt, bisection, fixed_point):
            self.assertNotIn("Newton", page)
            self.assertNotIn("中值定理", page)


if __name__ == "__main__":
    unittest.main()
