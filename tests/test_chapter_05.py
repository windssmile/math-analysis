"""Regression tests for Chapter 5 learning units."""

from __future__ import annotations

from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"


class Chapter05Tests(unittest.TestCase):
    def chapter_units(self) -> list[dict]:
        with UNITS.open("rb") as handle:
            units = tomllib.load(handle)["units"]
        return [unit for unit in units if unit["chapter_id"] == "chapter-05"]

    def test_registry_closes_chapter_hours_paths_and_reading_order(self) -> None:
        chapter_units = self.chapter_units()
        expected = [
            (
                "u-02-05-01",
                "数列怎样记录无限过程？",
                1.50,
                0.50,
                "book/part-02/chapter-05/u-02-05-01-sequences.qmd",
            ),
            (
                "u-02-05-02",
                "“最终任意接近”怎样写成定义？",
                2.00,
                0.25,
                "book/part-02/chapter-05/u-02-05-02-epsilon-n.qmd",
            ),
            (
                "u-02-05-05",
                "极限证明怎样从目标误差反推起点？",
                2.00,
                0.25,
                "book/part-02/chapter-05/u-02-05-05-limit-consequences.qmd",
            ),
            (
                "u-02-05-03",
                "不收敛与趋于无穷怎样区分？",
                1.50,
                0.25,
                "book/part-02/chapter-05/u-02-05-03-divergence-infinity.qmd",
            ),
            (
                "u-02-05-04",
                "迭代数据何时值得相信？",
                1.00,
                0.75,
                "book/part-02/chapter-05/u-02-05-04-iteration-evidence.qmd",
            ),
        ]

        self.assertEqual(
            [unit["id"] for unit in chapter_units],
            [row[0] for row in expected],
        )
        for unit, (unit_id, title, theory, applied, path) in zip(
            chapter_units, expected, strict=True
        ):
            with self.subTest(unit_id=unit_id):
                self.assertEqual(unit["id"], unit_id)
                self.assertEqual(unit["title"], title)
                self.assertEqual(
                    (unit["theory_hours"], unit["applied_hours"]),
                    (theory, applied),
                )
                self.assertEqual(unit["path"], path)
                self.assertEqual(unit["content_standard"], 2)

        self.assertEqual(sum(unit["theory_hours"] for unit in chapter_units), 8.0)
        self.assertEqual(sum(unit["applied_hours"] for unit in chapter_units), 2.0)

    def test_quantifier_and_infinity_language_stays_in_its_boundary(self) -> None:
        content = (
            ROOT / "book/part-02/chapter-05/u-02-05-03-divergence-infinity.qmd"
        ).read_text(encoding="utf-8")
        self.assertIn(r"\forall M>0\;\exists N", content)
        self.assertIn(r"\forall n\ge N", content)
        self.assertIn(r"a_n>M", content)
        self.assertIn(r"a_n<-M", content)
        self.assertIn(r"a_n\to+\infty", content)
        self.assertIn(r"a_n\to-\infty", content)
        self.assertIn("有限不收敛", content)
        self.assertIn("振荡", content)
        self.assertIn("无界", content)
        self.assertIn("发散到正无穷", content)
        self.assertNotIn(r"\overline{\mathbb R}", content)
        self.assertNotIn("扩展实数运算", content)

        chapter_08_content = (
            ROOT / "book/part-02/chapter-08/u-02-08-05-limsup-liminf.qmd"
        ).read_text(encoding="utf-8")
        self.assertIn(r"\overline{\mathbb R}", chapter_08_content)

    def test_reviewed_tex_and_prose_regressions_stay_fixed(self) -> None:
        chapter_content = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((ROOT / "book/part-02/chapter-05").glob("*.qmd"))
        )
        self.assertNotIn(",quad", chapter_content)
        self.assertNotIn(",qquad", chapter_content)
        self.assertNotIn("somewhere", chapter_content)
        self.assertIn("常数数列 $c_n\\equiv0$ 由定义立即收敛于 $0$", chapter_content)


if __name__ == "__main__":
    unittest.main()
