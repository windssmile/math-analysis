"""Regression tests for Chapter 10 learning-unit registration."""

from __future__ import annotations

from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"


class Chapter10Tests(unittest.TestCase):
    def test_registry_closes_chapter_hours_and_paths(self) -> None:
        with UNITS.open("rb") as handle:
            by_id = {unit["id"]: unit for unit in tomllib.load(handle)["units"]}
        expected = {
            "u-03-10-01": ("连续性怎样写成局部控制？", 1.60, 0.40, "epsilon-delta-continuity"),
            "u-03-10-02": ("连续性怎样经过运算和复合传递？", 1.50, 0.50, "continuous-operations"),
            "u-03-10-03": ("函数会以哪些方式失去连续性？", 1.50, 0.50, "discontinuities-elementary-functions"),
        }
        for unit_id, (title, theory, applied, suffix) in expected.items():
            with self.subTest(unit_id=unit_id):
                unit = by_id[unit_id]
                self.assertEqual(unit["chapter_id"], "chapter-10")
                self.assertEqual(unit["title"], title)
                self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (theory, applied))
                self.assertEqual(unit["path"], f"book/part-03/chapter-10/{unit_id}-{suffix}.qmd")

    def test_continuity_pages_keep_the_confirmed_boundary(self) -> None:
        definition = (ROOT / "book/part-03/chapter-10/u-03-10-01-epsilon-delta-continuity.qmd").read_text(encoding="utf-8")
        operations = (ROOT / "book/part-03/chapter-10/u-03-10-02-continuous-operations.qmd").read_text(encoding="utf-8")
        discontinuities = (ROOT / "book/part-03/chapter-10/u-03-10-03-discontinuities-elementary-functions.qmd").read_text(encoding="utf-8")

        self.assertIn("def-u-03-10-01-continuity", definition)
        self.assertIn(r"|f(x)-f(a)|<\varepsilon", definition)
        self.assertIn("thm-u-03-10-02-continuous-operations", operations)
        self.assertIn("thm-u-03-10-02-composition", operations)
        self.assertIn("ex-u-03-10-03-discontinuity-types", discontinuities)
        for page in (definition, operations, discontinuities):
            self.assertNotIn("中值定理", page)
            self.assertNotIn("导数", page)
        for marker in ("可去", "跳跃", "振荡"):
            self.assertIn(marker, discontinuities)


if __name__ == "__main__":
    unittest.main()
