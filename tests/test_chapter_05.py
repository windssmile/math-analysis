"""Regression tests for Chapter 5 learning units."""

from __future__ import annotations

from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"


class Chapter05Tests(unittest.TestCase):
    def test_registry_closes_chapter_hours_and_paths(self) -> None:
        with UNITS.open("rb") as handle:
            by_id = {unit["id"]: unit for unit in tomllib.load(handle)["units"]}

        expected = {
            "u-02-05-01": ("数列怎样记录无限过程？", 1.25, 0.50, "sequences"),
            "u-02-05-02": ("“最终任意接近”怎样写成定义？", 1.75, 0.25, "epsilon-n"),
            "u-02-05-03": ("不收敛与趋于无穷怎样区分？", 1.75, 0.25, "divergence-infinity"),
            "u-02-05-04": ("迭代数据何时值得相信？", 1.75, 0.50, "iteration-evidence"),
        }
        for unit_id, (title, theory, applied, suffix) in expected.items():
            with self.subTest(unit_id=unit_id):
                unit = by_id[unit_id]
                self.assertEqual(unit["chapter_id"], "chapter-05")
                self.assertEqual(unit["title"], title)
                self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (theory, applied))
                self.assertEqual(unit["path"], f"book/part-02/chapter-05/{unit_id}-{suffix}.qmd")

    def test_quantifier_and_infinity_language_stays_in_its_boundary(self) -> None:
        content = (ROOT / "book/part-02/chapter-05/u-02-05-03-divergence-infinity.qmd").read_text(encoding="utf-8")
        self.assertIn(r"\forall M>0\;\exists N", content)
        self.assertIn(r"a_n\to+\infty", content)
        self.assertIn(r"a_n\to-\infty", content)
        self.assertIn("不是有限极限", content)
        self.assertNotIn("\\overline{\\mathbb R}", content)


if __name__ == "__main__":
    unittest.main()
