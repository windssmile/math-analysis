"""Regression tests for Chapter 6 learning units."""

from __future__ import annotations

from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"
QUARTO = ROOT / "_quarto.yml"


class Chapter06Tests(unittest.TestCase):
    def test_registry_closes_chapter_hours_and_paths(self) -> None:
        with UNITS.open("rb") as handle:
            units = tomllib.load(handle)["units"]
        chapter_units = [unit for unit in units if unit["chapter_id"] == "chapter-06"]
        expected = [
            ("u-02-06-01", "极限怎样通过代数运算传递？", 2.00, 0.25, "limit-laws"),
            ("u-02-06-04", "倒数与商法则为何必须远离零？", 1.75, 0.25, "reciprocal-quotient"),
            ("u-02-06-02", "序关系怎样给出极限估计？", 1.75, 0.25, "order-squeeze"),
            ("u-02-06-03", "误差如何穿过一次迭代？", 1.00, 0.75, "error-propagation"),
        ]
        self.assertEqual([unit["id"] for unit in chapter_units], [row[0] for row in expected])
        by_id = {unit["id"]: unit for unit in chapter_units}
        for unit_id, title, theory, applied, suffix in expected:
            with self.subTest(unit_id=unit_id):
                unit = by_id[unit_id]
                self.assertEqual(unit["chapter_id"], "chapter-06")
                self.assertEqual(unit["title"], title)
                self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (theory, applied))
                self.assertEqual(unit["path"], f"book/part-02/chapter-06/{unit_id}-{suffix}.qmd")
                self.assertEqual(unit["content_standard"], 2)
        self.assertEqual(sum(unit["theory_hours"] for unit in chapter_units), 6.5)
        self.assertEqual(sum(unit["applied_hours"] for unit in chapter_units), 1.5)

    def test_quarto_publishes_chapter_in_registry_order(self) -> None:
        quarto = QUARTO.read_text(encoding="utf-8")
        paths = [
            "book/part-02/chapter-06/u-02-06-01-limit-laws.qmd",
            "book/part-02/chapter-06/u-02-06-04-reciprocal-quotient.qmd",
            "book/part-02/chapter-06/u-02-06-02-order-squeeze.qmd",
            "book/part-02/chapter-06/u-02-06-03-error-propagation.qmd",
        ]
        positions = [quarto.find(path) for path in paths]
        self.assertNotIn(-1, positions)
        self.assertEqual(positions, sorted(positions))

    def test_limit_laws_separate_bounded_tail_from_reciprocal(self) -> None:
        content = (ROOT / "book/part-02/chapter-06/u-02-06-01-limit-laws.qmd").read_text(encoding="utf-8")
        self.assertIn("{#lem-u-02-06-01-bounded-tail}", content)
        self.assertIn("{#thm-u-02-06-01-product}", content)
        self.assertNotIn("商法则", content)

    def test_reciprocal_unit_states_zero_boundary(self) -> None:
        content = (ROOT / "book/part-02/chapter-06/u-02-06-04-reciprocal-quotient.qmd").read_text(encoding="utf-8")
        self.assertIn("{#lem-u-02-06-04-away-from-zero}", content)
        self.assertIn("{#thm-u-02-06-04-reciprocal}", content)
        self.assertIn("{#thm-u-02-06-04-quotient}", content)
        self.assertIn("未定式", content)

    def test_error_propagation_is_algebraic_not_calculus(self) -> None:
        content = (ROOT / "book/part-02/chapter-06/u-02-06-03-error-propagation.qmd").read_text(encoding="utf-8")
        self.assertIn(r"|g(x)-g(y)|=\frac{|x-y|}{(2+x)(2+y)}", content)
        self.assertIn("一次迭代", content)
        self.assertIn("第 8 章", content)
        self.assertNotIn("g'(x)", content)
        self.assertNotIn("中值定理", content)


if __name__ == "__main__":
    unittest.main()
