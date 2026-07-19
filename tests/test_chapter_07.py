"""Regression tests for Chapter 7 learning units."""

from __future__ import annotations

from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"


class Chapter07Tests(unittest.TestCase):
    def test_registry_closes_chapter_hours_and_paths(self) -> None:
        with UNITS.open("rb") as handle:
            by_id = {unit["id"]: unit for unit in tomllib.load(handle)["units"]}
        expected = {
            "u-02-07-01": ("单调数列为什么会有极限？", 1.50, 0.50, "monotone-sequences"),
            "u-02-07-02": ("递推的界与单调性怎样建立？", 2.00, 0.25, "recursive-invariants"),
            "u-02-07-03": ("区间套怎样保证唯一目标？", 1.75, 0.25, "nested-intervals"),
            "u-02-07-04": ("完备性怎样成为收敛准则？", 1.75, 0.00, "completeness-criteria"),
        }
        for unit_id, (title, theory, applied, suffix) in expected.items():
            with self.subTest(unit_id=unit_id):
                unit = by_id[unit_id]
                self.assertEqual(unit["chapter_id"], "chapter-07")
                self.assertEqual(unit["title"], title)
                self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (theory, applied))
                self.assertEqual(unit["path"], f"book/part-02/chapter-07/{unit_id}-{suffix}.qmd")

    def test_chapter_keeps_subsequences_and_cauchy_for_chapter_eight(self) -> None:
        content = (ROOT / "book/part-02/chapter-07/u-02-07-04-completeness-criteria.qmd").read_text(encoding="utf-8")
        self.assertIn("单调有界", content)
        self.assertIn("区间套", content)
        self.assertNotIn("Bolzano", content)
        self.assertNotIn("Cauchy 准则", content)


if __name__ == "__main__":
    unittest.main()
