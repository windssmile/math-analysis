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
            chapter_units = [
                unit
                for unit in tomllib.load(handle)["units"]
                if unit["chapter_id"] == "chapter-08"
            ]
        expected = (
            ("u-02-08-01", 1.50, 0.25, "subsequences"),
            ("u-02-08-02", 1.75, 0.25, "bolzano-weierstrass"),
            ("u-02-08-03", 1.75, 0.25, "cauchy-criterion"),
            ("u-02-08-04", 2.00, 0.25, "contraction-mapping"),
            ("u-02-08-06", 1.50, 0.50, "fixed-point-certificates"),
            ("u-02-08-07", 0.75, 1.25, "iteration-lab"),
            ("u-02-08-05", 1.75, 0.25, "limsup-liminf"),
            ("u-02-08-08", 1.50, 0.50, "limsup-subsequences"),
        )
        self.assertEqual([unit["id"] for unit in chapter_units], [row[0] for row in expected])
        self.assertEqual(sum(unit["theory_hours"] for unit in chapter_units), 12.5)
        self.assertEqual(sum(unit["applied_hours"] for unit in chapter_units), 3.5)
        for unit, (unit_id, theory, applied, suffix) in zip(chapter_units, expected):
            with self.subTest(unit_id=unit_id):
                self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (theory, applied))
                self.assertEqual(unit["content_standard"], 2)
                self.assertEqual(unit["path"], f"book/part-02/chapter-08/{unit_id}-{suffix}.qmd")

    def test_quarto_registers_exact_chapter_order(self) -> None:
        import yaml

        config = yaml.safe_load((ROOT / "_quarto.yml").read_text(encoding="utf-8"))
        part = next(item for item in config["book"]["chapters"] if isinstance(item, dict) and item.get("part", "").startswith("第二部"))
        chapter_paths = [path for path in part["chapters"] if "/chapter-08/" in path]
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


if __name__ == "__main__":
    unittest.main()
