"""Regression tests for Chapter 9 learning-unit registration."""

from __future__ import annotations

from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"


class Chapter09Tests(unittest.TestCase):
    def test_registry_closes_chapter_hours_and_paths(self) -> None:
        with UNITS.open("rb") as handle:
            by_id = {unit["id"]: unit for unit in tomllib.load(handle)["units"]}
        expected = {
            "u-03-09-01": ("函数在一点附近意味着什么？", 1.60, 0.40, "local-neighborhoods"),
            "u-03-09-02": ("“任意接近”怎样定义函数极限？", 1.60, 0.40, "epsilon-delta-limit"),
            "u-03-09-03": ("局部估计怎样传递极限？", 1.50, 0.50, "function-limit-laws"),
            "u-03-09-04": ("用点列靠近能否判别函数极限？", 1.50, 0.50, "sequential-function-limits"),
        }
        for unit_id, (title, theory, applied, suffix) in expected.items():
            with self.subTest(unit_id=unit_id):
                unit = by_id[unit_id]
                self.assertEqual(unit["chapter_id"], "chapter-09")
                self.assertEqual(unit["title"], title)
                self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (theory, applied))
                self.assertEqual(unit["path"], f"book/part-03/chapter-09/{unit_id}-{suffix}.qmd")

    def test_function_limit_pages_keep_epsilon_delta_as_the_main_language(self) -> None:
        local = (ROOT / "book/part-03/chapter-09/u-03-09-01-local-neighborhoods.qmd").read_text(encoding="utf-8")
        epsilon_delta = (ROOT / "book/part-03/chapter-09/u-03-09-02-epsilon-delta-limit.qmd").read_text(encoding="utf-8")
        laws = (ROOT / "book/part-03/chapter-09/u-03-09-03-function-limit-laws.qmd").read_text(encoding="utf-8")
        sequential = (ROOT / "book/part-03/chapter-09/u-03-09-04-sequential-function-limits.qmd").read_text(encoding="utf-8")

        self.assertIn("def-u-03-09-01-neighborhood", local)
        self.assertIn("def-u-03-09-02-function-limit", epsilon_delta)
        self.assertIn(r"0<|x-a|<\delta", epsilon_delta)
        self.assertIn("thm-u-03-09-03-squeeze", laws)
        self.assertIn("thm-u-03-09-04-sequential-criterion", sequential)
        self.assertIn("反设", sequential)
        self.assertNotIn("连续函数", epsilon_delta)


if __name__ == "__main__":
    unittest.main()
