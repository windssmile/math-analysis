"""Regression tests for Chapter 7 learning units."""

from __future__ import annotations

from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"
CHAPTER = ROOT / "book" / "part-02" / "chapter-07"


class Chapter07Tests(unittest.TestCase):
    def test_registry_closes_chapter_hours_and_paths(self) -> None:
        with UNITS.open("rb") as handle:
            by_id = {unit["id"]: unit for unit in tomllib.load(handle)["units"]}
        expected = {
            "u-02-07-01": ("单调数列为什么会有极限？", 2.00, 0.25, "monotone-sequences"),
            "u-02-07-02": ("递推的界与单调性怎样建立？", 1.75, 0.50, "recursive-invariants"),
            "u-02-07-03": ("区间套怎样保证唯一目标？", 1.75, 0.25, "nested-intervals"),
            "u-02-07-04": ("完备性怎样成为收敛准则？", 1.50, 0.00, "completeness-criteria"),
        }
        chapter_units = [unit for unit in by_id.values() if unit["chapter_id"] == "chapter-07"]
        for unit_id, (title, theory, applied, suffix) in expected.items():
            with self.subTest(unit_id=unit_id):
                unit = by_id[unit_id]
                self.assertEqual(unit["chapter_id"], "chapter-07")
                self.assertEqual(unit["title"], title)
                self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (theory, applied))
                self.assertEqual(unit["path"], f"book/part-02/chapter-07/{unit_id}-{suffix}.qmd")
                self.assertEqual(unit.get("content_standard"), 2)
        self.assertEqual(sum(unit["theory_hours"] for unit in chapter_units), 7.0)
        self.assertEqual(sum(unit["applied_hours"] for unit in chapter_units), 1.0)

    def test_monotone_unit_proves_both_directions_and_marks_hypotheses(self) -> None:
        content = (CHAPTER / "u-02-07-01-monotone-sequences.qmd").read_text(encoding="utf-8")
        for marker in (
            "{#thm-u-02-07-01-increasing}",
            "{#thm-u-02-07-01-decreasing}",
            "非空性",
            "有界性",
            "单调但无界",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, content)

    def test_recursive_unit_separates_certificate_from_fixed_point_candidate(self) -> None:
        content = (CHAPTER / "u-02-07-02-recursive-invariants.qmd").read_text(encoding="utf-8")
        self.assertIn("{#prop-u-02-07-02-invariant}", content)
        self.assertIn("{#prop-u-02-07-02-monotone}", content)
        self.assertIn("{#ex-u-02-07-02-oscillation}", content)
        self.assertIn(r"x_{n+1}=1-x_n", content)
        self.assertIn("先证明收敛", content)

    def test_nested_intervals_separate_existence_uniqueness_and_hypotheses(self) -> None:
        content = (CHAPTER / "u-02-07-03-nested-intervals.qmd").read_text(encoding="utf-8")
        for marker in (
            "{#thm-u-02-07-03-nonempty}",
            "{#thm-u-02-07-03-unique}",
            "{#ex-u-02-07-03-without-nesting}",
            "{#ex-u-02-07-03-without-shrinking}",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, content)

    def test_completeness_map_preserves_chapter_boundary(self) -> None:
        content = (CHAPTER / "u-02-07-04-completeness-criteria.qmd").read_text(encoding="utf-8")
        self.assertIn("确界原理", content)
        self.assertIn("确界原理 → 单调有界定理 → 区间套", content)
        self.assertIn("有界数列", content)
        self.assertIn("不保证收敛", content)
        self.assertNotIn("Cauchy", content)
        self.assertNotIn("Bolzano-Weierstrass", content)

    def test_chapter_keeps_subsequences_and_cauchy_for_chapter_eight(self) -> None:
        content = "\n".join(
            path.read_text(encoding="utf-8") for path in sorted(CHAPTER.glob("*.qmd"))
        )
        self.assertIn("确界原理", content)
        self.assertIn("单调有界", content)
        self.assertIn("区间套", content)
        self.assertNotIn("Bolzano", content)
        self.assertNotIn("Cauchy 准则", content)

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


if __name__ == "__main__":
    unittest.main()
