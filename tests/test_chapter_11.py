"""Regression tests for Chapter 11 learning-unit registration."""

from __future__ import annotations

from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"


class Chapter11Tests(unittest.TestCase):
    def test_registry_closes_chapter_hours_and_paths(self) -> None:
        with UNITS.open("rb") as handle:
            by_id = {unit["id"]: unit for unit in tomllib.load(handle)["units"]}
        expected = {
            "u-03-11-01": ("为什么闭区间能把无限局部信息压缩为有限控制？", 1.60, 0.40, "compact-intervals"),
            "u-03-11-02": ("连续函数为何一定有界并取得最值？", 1.50, 0.50, "extreme-value-theorem"),
            "u-03-11-03": ("局部连续何时升级为全局一致控制？", 1.50, 0.50, "uniform-continuity"),
        }
        for unit_id, (title, theory, applied, suffix) in expected.items():
            with self.subTest(unit_id=unit_id):
                unit = by_id[unit_id]
                self.assertEqual(unit["chapter_id"], "chapter-11")
                self.assertEqual(unit["title"], title)
                self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (theory, applied))
                self.assertEqual(unit["path"], f"book/part-03/chapter-11/{unit_id}-{suffix}.qmd")

    def test_compactness_pages_keep_the_confirmed_scope(self) -> None:
        compact = (ROOT / "book/part-03/chapter-11/u-03-11-01-compact-intervals.qmd").read_text(encoding="utf-8")
        extrema = (ROOT / "book/part-03/chapter-11/u-03-11-02-extreme-value-theorem.qmd").read_text(encoding="utf-8")
        uniform = (ROOT / "book/part-03/chapter-11/u-03-11-03-uniform-continuity.qmd").read_text(encoding="utf-8")

        self.assertIn("def-u-03-11-01-open-cover", compact)
        self.assertIn("def-u-03-11-01-compactness", compact)
        self.assertIn("thm-u-03-11-01-heine-borel", compact)
        self.assertIn("上确界", compact)
        self.assertIn("有限子覆盖", compact)
        self.assertIn("thm-u-03-11-02-extreme-value", extrema)
        self.assertIn("thm-u-03-11-03-uniform-continuity", uniform)
        self.assertIn(r"\min", uniform)
        for page in (compact, extrema, uniform):
            self.assertNotIn("一般度量空间", page)


if __name__ == "__main__":
    unittest.main()
