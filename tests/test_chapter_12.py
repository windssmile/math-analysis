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


if __name__ == "__main__":
    unittest.main()
