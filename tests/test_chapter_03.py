"""Regression tests for Chapter 3 learning units."""

from __future__ import annotations

from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"
BOUNDS = ROOT / "book" / "part-01" / "chapter-03" / "u-01-03-01-bounds.qmd"
SUPREMUM_PRINCIPLE = (
    ROOT / "book" / "part-01" / "chapter-03" / "u-01-03-02-supremum-principle.qmd"
)
COMPLETENESS_CONSEQUENCES = (
    ROOT
    / "book"
    / "part-01"
    / "chapter-03"
    / "u-01-03-03-completeness-consequences.qmd"
)


class Chapter03BoundsTests(unittest.TestCase):
    def test_bounds_unit_has_its_curriculum_contract(self) -> None:
        with UNITS.open("rb") as handle:
            registry = tomllib.load(handle)
        by_id = {unit["id"]: unit for unit in registry["units"]}

        unit = by_id["u-01-03-01"]
        self.assertEqual(unit["chapter_id"], "chapter-03")
        self.assertEqual(
            unit["path"], "book/part-01/chapter-03/u-01-03-01-bounds.qmd"
        )
        self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (1.50, 0.00))
        self.assertEqual(unit["capabilities"], ["concepts", "proof", "mathematical_expression"])
        self.assertEqual(unit["book_prerequisites"], ["chapter-02"])

    def test_bounds_unit_keeps_stable_definition_and_example_anchors(self) -> None:
        content = BOUNDS.read_text(encoding="utf-8")
        self.assertIn("### 上界、下界与确界 {#def-u-01-03-01-bounds}", content)
        self.assertIn("### 例：有理数中的缺失上确界 {#ex-u-01-03-01-rational-supremum}", content)

    def test_rational_upper_bound_argument_does_not_assume_strictness(self) -> None:
        content = BOUNDS.read_text(encoding="utf-8")
        self.assertIn("由于 $0\\in D$，有 $u\\ge0$", content)
        self.assertIn("若 $u\\in D$", content)
        self.assertIn("所以 $u\\notin D$ 且 $u\\ge0$，从而 $u>0$ 且 $u^2>2$", content)

    def test_bounds_unit_makes_chapter_two_its_explicit_prerequisite(self) -> None:
        content = BOUNDS.read_text(encoding="utf-8")
        self.assertIn(
            "[第 2 章：实数系与完备性公理](../../curriculum-map.qmd#chapter-02)",
            content,
        )
        self.assertIn("有理数缺口", content)
        self.assertIn("Dedekind 分割", content)


class Chapter03SupremumPrincipleTests(unittest.TestCase):
    def test_supremum_principle_unit_has_its_curriculum_contract(self) -> None:
        with UNITS.open("rb") as handle:
            registry = tomllib.load(handle)
        by_id = {unit["id"]: unit for unit in registry["units"]}

        unit = by_id["u-01-03-02"]
        self.assertEqual(unit["chapter_id"], "chapter-03")
        self.assertEqual(
            unit["title"], "最小上界怎样保证存在？"
        )
        self.assertEqual(
            unit["path"],
            "book/part-01/chapter-03/u-01-03-02-supremum-principle.qmd",
        )
        self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (2.00, 0.00))
        self.assertEqual(
            unit["capabilities"], ["concepts", "proof", "mathematical_expression"]
        )
        self.assertEqual(unit["book_prerequisites"], ["chapter-02"])
        self.assertEqual(
            unit["higher_algebra_prerequisites"],
            ["不等式的基本性质", "平方差分解"],
        )
        self.assertEqual(unit["analytic_geometry_prerequisites"], [])
        self.assertEqual(unit["python_prerequisites"], [])

    def test_supremum_principle_keeps_stable_theorem_and_example_anchors(self) -> None:
        content = SUPREMUM_PRINCIPLE.read_text(encoding="utf-8")
        self.assertIn(
            "### 确界原理 {#thm-u-01-03-02-supremum-principle}", content
        )
        self.assertIn(
            "### 例：正数的平方根存在 {#ex-u-01-03-02-square-root-existence}",
            content,
        )
        self.assertIn("切割族的并集", content)

    def test_square_root_proof_uses_explicit_perturbations_without_continuity(self) -> None:
        content = SUPREMUM_PRINCIPLE.read_text(encoding="utf-8")
        self.assertIn("S=\\{x\\in\\mathbb R:x\\ge0,\\ x^2<a\\}", content)
        self.assertIn("$s=\\sup S$", content)
        self.assertIn("$s^2<a$", content)
        self.assertIn("$(s+\\varepsilon)^2<a$", content)
        self.assertIn("$s^2>a$", content)
        self.assertIn("$(s-\\varepsilon)^2>a$", content)
        self.assertIn("$s-\\varepsilon$ 是 $S$ 的上界", content)
        self.assertNotIn("连续性", content)

    def test_supremum_principle_unit_has_six_answered_exercises(self) -> None:
        content = SUPREMUM_PRINCIPLE.read_text(encoding="utf-8")
        for index in range(1, 7):
            self.assertIn(f"### ex-u-01-03-02-0{index}", content)
        self.assertIn("**完整解答。**", content)

    def test_open_interval_supremum_argument_uses_a_witness_for_every_lower_number(
        self,
    ) -> None:
        content = SUPREMUM_PRINCIPLE.read_text(encoding="utf-8")
        self.assertIn("$x=(\\max\\{M,0\\}+1)/2$", content)
        self.assertIn("$x\\in(0,1)$", content)
        self.assertIn("$x>M$", content)


class Chapter03CompletenessConsequencesTests(unittest.TestCase):
    def test_completeness_consequences_unit_has_its_curriculum_contract(self) -> None:
        with UNITS.open("rb") as handle:
            registry = tomllib.load(handle)
        by_id = {unit["id"]: unit for unit in registry["units"]}

        unit = by_id["u-01-03-03"]
        self.assertEqual(unit["chapter_id"], "chapter-03")
        self.assertEqual(unit["title"], "确界原理能推出什么？")
        self.assertEqual(
            unit["path"],
            "book/part-01/chapter-03/u-01-03-03-completeness-consequences.qmd",
        )
        self.assertEqual((unit["theory_hours"], unit["applied_hours"]), (1.50, 0.00))
        self.assertEqual(
            unit["capabilities"], ["concepts", "proof", "mathematical_expression"]
        )
        self.assertEqual(unit["book_prerequisites"], ["chapter-02"])
        self.assertEqual(
            unit["higher_algebra_prerequisites"], ["整数与有理数的基本性质"]
        )

    def test_unit_has_stable_anchors_and_full_archimedean_proof(self) -> None:
        content = COMPLETENESS_CONSEQUENCES.read_text(encoding="utf-8")
        self.assertIn(
            "### 阿基米德性质 {#thm-u-01-03-03-archimedean}", content
        )
        self.assertIn(
            "### 例：在两个实数之间找到有理数 {#ex-u-01-03-03-rational-density}",
            content,
        )
        self.assertIn("若 $\\mathbb N$ 有上界", content)
        self.assertIn("令 $s=\\sup\\mathbb N$", content)
        self.assertIn("$s-1$ 不是 $\\mathbb N$ 的上界", content)
        self.assertIn("$n>s-1$", content)
        self.assertIn("$n+1>s$", content)
        self.assertIn("与 $s$ 是 $\\mathbb N$ 的上界矛盾", content)

    def test_unit_proves_density_or_square_root_and_has_answered_exercises(self) -> None:
        content = COMPLETENESS_CONSEQUENCES.read_text(encoding="utf-8")
        self.assertIn("$x<q<y$", content)
        self.assertIn("$q=m/n$", content)
        self.assertIn("$n(y-x)>1$", content)
        self.assertIn("$m-1\\le nx<m$", content)
        self.assertIn("正数平方根存在", content)
        for index in range(1, 5):
            self.assertIn(f"### ex-u-01-03-03-0{index}", content)
        self.assertIn("**完整解答。**", content)


if __name__ == "__main__":
    unittest.main()
