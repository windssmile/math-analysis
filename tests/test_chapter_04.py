"""Regression tests for Chapter 4 learning units."""

from __future__ import annotations

from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"
RECURRENCE = ROOT / "book" / "part-01" / "chapter-04" / "u-01-04-01-recurrence.qmd"
INTERVAL_BISECTION = (
    ROOT / "book" / "part-01" / "chapter-04" / "u-01-04-02-interval-bisection.qmd"
)


class Chapter04RecurrenceTests(unittest.TestCase):
    def test_recurrence_unit_has_its_curriculum_contract(self) -> None:
        with UNITS.open("rb") as handle:
            registry = tomllib.load(handle)
        by_id = {unit["id"]: unit for unit in registry["units"]}

        unit = by_id["u-01-04-01"]
        self.assertEqual(unit["chapter_id"], "chapter-04")
        self.assertEqual(unit["title"], "递推会不会真的“靠近”目标？")
        self.assertEqual(
            unit["path"], "book/part-01/chapter-04/u-01-04-01-recurrence.qmd"
        )
        self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (1.25, 0.50))
        self.assertEqual(unit["book_prerequisites"], ["chapter-03"])
        self.assertEqual(unit["python_prerequisites"], ["变量赋值", "for 循环", "函数定义"])
        self.assertEqual(
            unit["capabilities"],
            ["concepts", "proof", "numerical_algorithm", "mathematical_expression"],
        )

    def test_recurrence_unit_has_stable_anchors_and_static_algorithm(self) -> None:
        content = RECURRENCE.read_text(encoding="utf-8")
        self.assertIn("# 递推会不会真的“靠近”目标？ {#u-01-04-01}", content)
        self.assertIn("### Babylonian 递推 {#def-u-01-04-01-babylonian-recurrence}", content)
        self.assertIn("### 例：从 $2$ 出发逼近 $\\sqrt2$ {#ex-u-01-04-01-sqrt2-table}", content)
        self.assertIn("```python", content)
        self.assertNotIn("```{python", content)
        self.assertIn("for n in range", content)

    def test_recurrence_proves_above_root_positive_and_decreasing_invariants(self) -> None:
        content = RECURRENCE.read_text(encoding="utf-8")
        self.assertIn("x_{n+1}=\\frac12\\left(x_n+\\frac a{x_n}\\right)", content)
        self.assertIn("a>0", content)
        self.assertIn("x_1>\\sqrt a", content)
        self.assertIn("x_{n+1}-\\sqrt a", content)
        self.assertIn("(x_n-\\sqrt a)^2", content)
        self.assertIn("x_n^2\\ge a", content)
        self.assertIn("x_{n+1}-x_n=\\frac{a-x_n^2}{2x_n}", content)
        self.assertIn("x_{n+1}\\le x_n", content)
        self.assertNotIn("收敛到", content)

    def test_recurrence_uses_the_current_reciprocal_and_derives_boundedness(self) -> None:
        content = RECURRENCE.read_text(encoding="utf-8")
        self.assertNotIn("a/x_1$ 平均", content)
        self.assertIn("a/x_n$ 平均", content)
        self.assertIn("x_n\\ge\\sqrt a", content)
        self.assertIn("x_n\\le x_1", content)
        self.assertIn("有界", content)

    def test_recurrence_unit_has_answered_exercises(self) -> None:
        content = RECURRENCE.read_text(encoding="utf-8")
        for index in range(1, 5):
            self.assertIn(f"### ex-u-01-04-01-0{index}", content)
        self.assertIn("**完整解答。**", content)


class Chapter04IntervalBisectionTests(unittest.TestCase):
    def test_interval_bisection_has_its_curriculum_contract(self) -> None:
        with UNITS.open("rb") as handle:
            registry = tomllib.load(handle)
        by_id = {unit["id"]: unit for unit in registry["units"]}

        unit = by_id["u-01-04-02"]
        self.assertEqual(unit["chapter_id"], "chapter-04")
        self.assertEqual(unit["title"], "区间怎样把目标逐步夹住？")
        self.assertEqual(
            unit["path"],
            "book/part-01/chapter-04/u-01-04-02-interval-bisection.qmd",
        )
        self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (1.25, 0.75))
        self.assertEqual(unit["book_prerequisites"], ["chapter-03"])
        self.assertEqual(
            unit["python_prerequisites"], ["while 循环", "条件分支", "函数定义"]
        )
        self.assertIn("numerical_algorithm", unit["capabilities"])

    def test_interval_bisection_has_stable_anchors_and_static_algorithm(self) -> None:
        content = INTERVAL_BISECTION.read_text(encoding="utf-8")
        self.assertIn("# 区间怎样把目标逐步夹住？ {#u-01-04-02}", content)
        self.assertIn(
            "### 平方根的区间二分法 {#def-u-01-04-02-interval-bisection}",
            content,
        )
        self.assertIn(
            "### 例：用区间长度控制 $\\sqrt2$ 的误差 {#ex-u-01-04-02-sqrt2-certificate}",
            content,
        )
        self.assertIn("```python", content)
        self.assertNotIn("```{python", content)
        self.assertIn("while b - a > 2 * tolerance", content)

    def test_interval_bisection_proves_invariant_length_and_error_bound(self) -> None:
        content = INTERVAL_BISECTION.read_text(encoding="utf-8")
        self.assertIn("a_n^2<2<b_n^2", content)
        self.assertIn("m_n=\\frac{a_n+b_n}{2}", content)
        self.assertIn("m_n^2<2", content)
        self.assertIn("m_n^2>2", content)
        self.assertIn("b_n-a_n=\\frac{b_0-a_0}{2^n}", content)
        self.assertIn("|m_n-\\sqrt2|\\le\\frac{b_n-a_n}{2}", content)
        self.assertIn("区间套", content)
        self.assertIn("唯一", content)

    def test_interval_bisection_states_its_pre_continuity_boundary(self) -> None:
        content = INTERVAL_BISECTION.read_text(encoding="utf-8")
        self.assertIn("不是一般连续函数求根", content)
        self.assertIn("介值定理", content)

    def test_interval_bisection_has_answered_exercises(self) -> None:
        content = INTERVAL_BISECTION.read_text(encoding="utf-8")
        for index in range(1, 5):
            self.assertIn(f"### ex-u-01-04-02-0{index}", content)
        self.assertIn("**完整解答。**", content)


if __name__ == "__main__":
    unittest.main()
