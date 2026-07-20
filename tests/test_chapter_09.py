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


if __name__ == "__main__":
    unittest.main()
