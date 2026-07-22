"""Regression tests for Chapter 8 learning units."""

from __future__ import annotations

from pathlib import Path
import re
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"
CHAPTER = ROOT / "book" / "part-02" / "chapter-08"


class Chapter08Tests(unittest.TestCase):
    def test_registry_closes_chapter_hours_and_paths(self) -> None:
        with UNITS.open("rb") as handle:
            chapter_units = [
                unit
                for unit in tomllib.load(handle)["units"]
                if unit["chapter_id"] == "chapter-08"
            ]
        expected = (
            (
                "u-02-08-01",
                "子列揭示了原数列的什么行为？",
                1.50,
                0.25,
                "subsequences",
            ),
            (
                "u-02-08-02",
                "有界数列为何总能抽出收敛子列？",
                1.75,
                0.25,
                "bolzano-weierstrass",
            ),
            (
                "u-02-08-03",
                "Cauchy 条件怎样不预知极限而判断收敛？",
                1.75,
                0.25,
                "cauchy-criterion",
            ),
            (
                "u-02-08-04",
                "严格压缩怎样保证迭代找到唯一根？",
                2.00,
                0.25,
                "contraction-mapping",
            ),
            (
                "u-02-08-06",
                "不动点计算需要哪些可核验证书？",
                1.50,
                0.50,
                "fixed-point-certificates",
            ),
            (
                "u-02-08-07",
                "有限迭代轨迹能说明什么、不能说明什么？",
                0.75,
                1.25,
                "iteration-lab",
            ),
            (
                "u-02-08-05",
                "上/下极限怎样总结所有尾部行为？",
                1.75,
                0.25,
                "limsup-liminf",
            ),
            (
                "u-02-08-08",
                "上/下极限怎样由子列真正实现？",
                1.50,
                0.50,
                "limsup-subsequences",
            ),
        )
        self.assertEqual(
            [unit["id"] for unit in chapter_units],
            [row[0] for row in expected],
        )
        self.assertEqual(sum(unit["theory_hours"] for unit in chapter_units), 12.5)
        self.assertEqual(sum(unit["applied_hours"] for unit in chapter_units), 3.5)
        for unit, (unit_id, title, theory, applied, suffix) in zip(
            chapter_units, expected, strict=True
        ):
            with self.subTest(unit_id=unit_id):
                self.assertEqual(unit["title"], title)
                self.assertEqual(
                    (unit["theory_hours"], unit["applied_hours"]),
                    (theory, applied),
                )
                self.assertEqual(unit["content_standard"], 2)
                self.assertEqual(
                    unit["path"],
                    f"book/part-02/chapter-08/{unit_id}-{suffix}.qmd",
                )

    def test_quarto_registers_exact_chapter_order(self) -> None:
        chapter_paths = [
            line.strip().removeprefix("href: ")
            for line in (ROOT / "_quarto.yml").read_text(encoding="utf-8").splitlines()
            if line.strip().startswith("href: book/part-02/chapter-08/")
        ]
        self.assertEqual(
            chapter_paths,
            [
                "book/part-02/chapter-08/u-02-08-01-subsequences.qmd",
                "book/part-02/chapter-08/u-02-08-02-bolzano-weierstrass.qmd",
                "book/part-02/chapter-08/u-02-08-03-cauchy-criterion.qmd",
                "book/part-02/chapter-08/u-02-08-04-contraction-mapping.qmd",
                "book/part-02/chapter-08/u-02-08-06-fixed-point-certificates.qmd",
                "book/part-02/chapter-08/u-02-08-07-iteration-lab.qmd",
                "book/part-02/chapter-08/u-02-08-05-limsup-liminf.qmd",
                "book/part-02/chapter-08/u-02-08-08-limsup-subsequences.qmd",
            ],
        )

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

    def test_reviewed_proof_boundaries_are_explicit(self) -> None:
        subsequences = (CHAPTER / "u-02-08-01-subsequences.qmd").read_text(
            encoding="utf-8"
        )
        cauchy = (CHAPTER / "u-02-08-03-cauchy-criterion.qmd").read_text(
            encoding="utf-8"
        )
        contraction = (CHAPTER / "u-02-08-04-contraction-mapping.qmd").read_text(
            encoding="utf-8"
        )
        tail_subsequences = (
            CHAPTER / "u-02-08-08-limsup-subsequences.qmd"
        ).read_text(encoding="utf-8")

        self.assertIn("### 例题 1：交替数列的两个聚点", subsequences)
        self.assertIn(r"N=\max\{n_{k-1}+1,k\}", subsequences)
        self.assertIn(r"n_k\ge N", subsequences)
        self.assertIn(r"B=\max\{|a_1|,\ldots,|a_{N_0}|\}", cauchy)
        self.assertIn("M=B+1", cauchy)
        self.assertRegex(contraction, r"j=0[^\n]*等式")
        self.assertIn(r"j\ge1", contraction)
        self.assertIn(r"k\ge0", tail_subsequences)
        self.assertIn("设 $n_0=0$", tail_subsequences)
        self.assertIn("令 $m_0=0$", tail_subsequences)
        self.assertIn(r"m_j>m_{j-1}", tail_subsequences)
        self.assertIn(r"a_{m_j}<-j", tail_subsequences)

    def test_chapter_tex_has_no_reviewed_corruption_patterns(self) -> None:
        contents = "\n".join(
            path.read_text(encoding="utf-8") for path in sorted(CHAPTER.glob("*.qmd"))
        )
        corrupt_fragments = {
            "|,|": "ordinary comma used between absolute-value factors",
            "\to": "tab plus o left by a damaged \\to command",
            "+infty": "infinity command missing its backslash",
            "=lim ": "limit command missing its backslash",
        }
        for fragment, description in corrupt_fragments.items():
            with self.subTest(fragment=repr(fragment)):
                self.assertNotIn(fragment, contents, description)

        set_bound_lines = [
            line
            for line in contents.splitlines()
            if re.search(r"\\(?:sup|inf)", line) and r"\{" in line
        ]
        self.assertGreaterEqual(len(set_bound_lines), 2)
        for line in set_bound_lines:
            with self.subTest(line=line):
                self.assertEqual(line.count(r"\{"), line.count(r"\}"))


if __name__ == "__main__":
    unittest.main()
