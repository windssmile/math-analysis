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
APPROXIMATION_ERROR = (
    ROOT / "book" / "part-01" / "chapter-04" / "u-01-04-03-approximation-error.qmd"
)
FAILURE_OF_INFINITE_APPROXIMATION = (
    ROOT
    / "book"
    / "part-01"
    / "chapter-04"
    / "u-01-04-04-failure-of-infinite-approximation.qmd"
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
        self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (1.25, 1.00))
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
        self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (1.25, 1.00))
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
        self.assertIn("0<a_n<\\sqrt2<b_n", content)
        self.assertIn("a_n,b_n\\in\\mathbb Q", content)
        self.assertIn("0<a_0=1<\\sqrt2<2=b_0", content)
        self.assertIn("a_n<m_n<b_n", content)
        self.assertIn("m_n\\in\\mathbb Q", content)
        self.assertIn("m_n\\ne\\sqrt2", content)
        self.assertIn("恰有", content)
        self.assertIn("a_n^2<2<b_n^2", content)
        self.assertIn("m_n=\\frac{a_n+b_n}{2}", content)
        self.assertIn("m_n^2<2", content)
        self.assertIn("m_n^2>2", content)
        self.assertIn("b_n-a_n=\\frac{b_0-a_0}{2^n}", content)
        self.assertIn("|m_n-\\sqrt2|\\le\\frac{b_n-a_n}{2}", content)
        self.assertIn("区间套", content)
        self.assertIn("唯一", content)

    def test_interval_bisection_exercise_preserves_positive_order_invariant(self) -> None:
        content = INTERVAL_BISECTION.read_text(encoding="utf-8")
        self.assertIn("设 $0<a_0<\\sqrt2<b_0$", content)
        self.assertIn("0<a_n<\\sqrt2<b_n", content)

    def test_interval_bisection_states_its_pre_continuity_boundary(self) -> None:
        content = INTERVAL_BISECTION.read_text(encoding="utf-8")
        self.assertIn("不是一般连续函数求根", content)
        self.assertIn("介值定理", content)

    def test_interval_bisection_has_answered_exercises(self) -> None:
        content = INTERVAL_BISECTION.read_text(encoding="utf-8")
        for index in range(1, 5):
            self.assertIn(f"### ex-u-01-04-02-0{index}", content)
        self.assertIn("**完整解答。**", content)


class Chapter04ApproximationErrorTests(unittest.TestCase):
    def test_approximation_error_has_its_curriculum_contract(self) -> None:
        with UNITS.open("rb") as handle:
            registry = tomllib.load(handle)
        by_id = {unit["id"]: unit for unit in registry["units"]}

        unit = by_id["u-01-04-03"]
        self.assertEqual(unit["chapter_id"], "chapter-04")
        self.assertEqual(unit["title"], "“越来越近”怎样说得严格？")
        self.assertEqual(
            unit["path"],
            "book/part-01/chapter-04/u-01-04-03-approximation-error.qmd",
        )
        self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (1.50, 0.50))
        self.assertEqual(unit["book_prerequisites"], ["chapter-03"])
        self.assertEqual(
            unit["capabilities"], ["concepts", "proof", "mathematical_expression"]
        )

    def test_approximation_error_has_stable_anchors_and_no_executable_code(self) -> None:
        content = APPROXIMATION_ERROR.read_text(encoding="utf-8")
        self.assertIn("# “越来越近”怎样说得严格？ {#u-01-04-03}", content)
        self.assertIn(
            "### 给定误差的有限步骤保证 {#def-u-01-04-03-error-guarantee}",
            content,
        )
        self.assertIn(
            "### 例：先算清二分次数 {#ex-u-01-04-03-bisection-step-count}",
            content,
        )
        self.assertIn(
            "### 二分中点的步数定理 {#thm-u-01-04-03-bisection-step-count}",
            content,
        )
        self.assertNotIn("```{python", content)

    def test_approximation_error_derives_the_correct_midpoint_bisection_count(self) -> None:
        content = APPROXIMATION_ERROR.read_text(encoding="utf-8")
        self.assertIn(r"|m_n-r|\le\frac{b-a}{2^{n+1}}", content)
        self.assertIn(r"\frac{b-a}{2^{n+1}}\le\varepsilon", content)
        self.assertIn(r"n\ge\left\lceil\log_2\frac{b-a}{\varepsilon}\right\rceil-1", content)
        self.assertIn("输出端点", content)
        self.assertIn(r"n\ge\left\lceil\log_2\frac{b-a}{\varepsilon}\right\rceil", content)
        self.assertIn("第 3 章的整数部分（取整）结论", content)
        self.assertIn(
            r"N=\max\left\{1,\left\lceil\log_2\frac{b-a}{\varepsilon}\right\rceil-1\right\}",
            content,
        )
        self.assertNotIn(
            r"N=\max\left\{0,\left\lceil\log_2\frac{b-a}{\varepsilon}\right\rceil-1\right\}",
            content,
        )
        self.assertIn("即使容许误差不小于初始长度", content)

    def test_approximation_error_teaches_quantifier_order_without_defining_convergence(self) -> None:
        content = APPROXIMATION_ERROR.read_text(encoding="utf-8")
        self.assertIn(r"\forall\varepsilon>0\;\exists N", content)
        self.assertIn(r"\forall n\ge N", content)
        self.assertIn("先给出容许误差", content)
        self.assertIn("不是本单元的数列收敛定义", content)
        self.assertNotIn("数列收敛当且仅当", content)

    def test_approximation_error_has_answered_exercises(self) -> None:
        content = APPROXIMATION_ERROR.read_text(encoding="utf-8")
        for index in range(1, 5):
            self.assertIn(f"### ex-u-01-04-03-0{index}", content)
        self.assertIn("**完整解答。**", content)


class Chapter04FailureOfInfiniteApproximationTests(unittest.TestCase):
    def test_chapter_four_has_four_units_and_planned_hours(self) -> None:
        with UNITS.open("rb") as handle:
            registry = tomllib.load(handle)
        chapter_units = [
            unit for unit in registry["units"] if unit["chapter_id"] == "chapter-04"
        ]

        self.assertEqual(
            [unit["id"] for unit in chapter_units],
            ["u-01-04-01", "u-01-04-02", "u-01-04-03", "u-01-04-04"],
        )
        self.assertEqual(sum(unit["theory_hours"] for unit in chapter_units), 5.0)
        self.assertEqual(sum(unit["applied_hours"] for unit in chapter_units), 2.5)

    def test_part_one_has_closed_hour_budget(self) -> None:
        with UNITS.open("rb") as handle:
            registry = tomllib.load(handle)
        part_one_units = [
            unit
            for unit in registry["units"]
            if unit["path"].startswith("book/part-01/")
        ]

        self.assertEqual(len(part_one_units), 14)
        self.assertEqual(sum(unit["theory_hours"] for unit in part_one_units), 20.0)
        self.assertEqual(sum(unit["applied_hours"] for unit in part_one_units), 4.0)

    def test_failure_unit_has_its_curriculum_contract(self) -> None:
        with UNITS.open("rb") as handle:
            registry = tomllib.load(handle)
        by_id = {unit["id"]: unit for unit in registry["units"]}

        unit = by_id["u-01-04-04"]
        self.assertEqual(unit["chapter_id"], "chapter-04")
        self.assertEqual(unit["title"], "无限逼近何时会失败？")
        self.assertEqual(
            unit["path"],
            "book/part-01/chapter-04/u-01-04-04-failure-of-infinite-approximation.qmd",
        )
        self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (1.00, 0.00))
        self.assertEqual(unit["book_prerequisites"], ["chapter-03"])
        self.assertEqual(
            unit["capabilities"], ["concepts", "proof", "mathematical_expression"]
        )

    def test_failure_unit_has_stable_anchors_and_all_answered_exercises(self) -> None:
        content = FAILURE_OF_INFINITE_APPROXIMATION.read_text(encoding="utf-8")
        self.assertIn("# 无限逼近何时会失败？ {#u-01-04-04}", content)
        self.assertIn(
            "### 无证书近似 {#def-u-01-04-04-uncertified-approximation}", content
        )
        self.assertIn(
            "### 例：小残差并不锁定位置 {#ex-u-01-04-04-small-residual}", content
        )
        self.assertIn(
            "### 例：伪二分法怎样丢失目标 {#ex-u-01-04-04-false-bisection}", content
        )
        for index in range(1, 5):
            self.assertIn(f"### ex-u-01-04-04-0{index}", content)
        self.assertIn("**完整解答。**", content)

    def test_failure_unit_distinguishes_required_failure_modes_without_future_tools(self) -> None:
        content = FAILURE_OF_INFINITE_APPROXIMATION.read_text(encoding="utf-8")
        self.assertIn(r"x_n=(-1)^n", content)
        self.assertIn("周期", content)
        self.assertIn("振荡", content)
        self.assertIn("发散", content)
        self.assertIn(r"f(x)=10^{-12}(x-1)", content)
        self.assertIn(r"x=1001", content)
        self.assertIn("残差", content)
        self.assertIn("位置误差", content)
        self.assertIn("不变量", content)
        self.assertIn("介值定理", content)
        self.assertIn("第二部", content)
        self.assertNotIn("柯西列", content)


if __name__ == "__main__":
    unittest.main()
