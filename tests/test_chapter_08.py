"""Regression tests for Chapter 8 learning units."""

from __future__ import annotations

from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"


class Chapter08Tests(unittest.TestCase):
    def test_registry_closes_chapter_hours_and_paths(self) -> None:
        with UNITS.open("rb") as handle:
            by_id = {unit["id"]: unit for unit in tomllib.load(handle)["units"]}
        expected = {
            "u-02-08-01": ("子列揭示了原数列的什么行为？", 1.00, 0.25, "subsequences"),
            "u-02-08-02": ("有界数列为何总能抽出收敛子列？", 1.50, 0.25, "bolzano-weierstrass"),
            "u-02-08-03": ("Cauchy 条件怎样不预知极限而判断收敛？", 1.75, 0.50, "cauchy-criterion"),
            "u-02-08-04": ("严格压缩怎样保证迭代找到唯一根？", 1.25, 1.00, "contraction-mapping"),
            "u-02-08-05": ("上/下极限怎样总结所有尾部行为？", 1.50, 0.50, "limsup-liminf"),
        }
        for unit_id, (title, theory, applied, suffix) in expected.items():
            with self.subTest(unit_id=unit_id):
                unit = by_id[unit_id]
                self.assertEqual(unit["chapter_id"], "chapter-08")
                self.assertEqual(unit["title"], title)
                self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (theory, applied))
                self.assertEqual(unit["path"], f"book/part-02/chapter-08/{unit_id}-{suffix}.qmd")

    def test_contraction_and_tail_limits_keep_the_confirmed_scope(self) -> None:
        contraction = (ROOT / "book/part-02/chapter-08/u-02-08-04-contraction-mapping.qmd").read_text(encoding="utf-8")
        tail_limits = (ROOT / "book/part-02/chapter-08/u-02-08-05-limsup-liminf.qmd").read_text(encoding="utf-8")
        self.assertIn(r"g:[a,b]\to[a,b]", contraction)
        self.assertIn(r"0\le q<1", contraction)
        self.assertIn(r"x_{n+1}=1-x_n", contraction)
        self.assertIn(r"x_{n+1}=\frac{x_n}{1+x_n}", contraction)
        self.assertNotIn("g'(x)", contraction)
        self.assertNotIn("中值定理", contraction)
        self.assertIn(r"\overline{\mathbb R}", tail_limits)
        self.assertIn(r"\sup_{k\ge n}", tail_limits)
        self.assertIn(r"\inf_{k\ge n}", tail_limits)
        self.assertNotIn("开覆盖", tail_limits)
        self.assertNotIn("紧致空间", tail_limits)


if __name__ == "__main__":
    unittest.main()
