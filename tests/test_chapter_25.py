from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-25"
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-06-dependencies.md"

EXPECTED_UNITS = [
    ("u-06-25-01", "逐点收敛为什么不足以控制整体行为？", 1.25, 0.50, "pointwise-uniform", 8, 10),
    ("u-06-25-02", "怎样用统一尾部控制刻画一致收敛？", 1.50, 0.25, "uniform-cauchy", 9, 11),
    ("u-06-25-03", "函数项级数怎样获得一致收敛判别？", 1.50, 0.50, "uniform-series-tests", 10, 12),
    ("u-06-25-04", "极限什么时候可以穿过连续与积分？", 1.50, 0.25, "continuity-integration", 9, 11),
    ("u-06-25-05", "微分为什么需要比积分更强的条件？", 1.25, 0.50, "differentiation", 10, 13),
]

REQUIRED_ANCHORS = {
    "u-06-25-01": (
        "def-u-06-25-01-pointwise",
        "def-u-06-25-01-uniform",
        "ex-u-06-25-01-xn",
        "tbl-u-06-25-01-quantifiers",
    ),
    "u-06-25-02": (
        "def-u-06-25-02-sup-error",
        "thm-u-06-25-02-uniform-cauchy",
        "cor-u-06-25-02-series-tail",
    ),
    "u-06-25-03": (
        "thm-u-06-25-03-m-test",
        "thm-u-06-25-03-uniform-dirichlet",
        "cor-u-06-25-03-uniform-abel",
    ),
    "u-06-25-04": (
        "thm-u-06-25-04-continuous-limit",
        "thm-u-06-25-04-integral-interchange",
        "cor-u-06-25-04-termwise-integration",
    ),
    "u-06-25-05": (
        "thm-u-06-25-05-derivative-interchange",
        "ex-u-06-25-05-uniform-not-enough",
        "tbl-u-06-25-05-exchange-conditions",
    ),
}

FORBIDDEN_CORE_TERMS = (
    "幂级数",
    "Taylor 级数",
    "解析函数",
    "Bernstein 多项式",
    "Fourier 级数",
    "Lebesgue 积分",
)


def unit_path(unit: tuple[str, str, float, float, str, int, int]) -> Path:
    unit_id, _title, _theory, _applied, suffix, _exercises, _answers = unit
    return CHAPTER / f"{unit_id}-{suffix}.md"


def read_unit(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    metadata = yaml.safe_load(text.split("---\n", 2)[1])
    return metadata, text


class ChapterTwentyFiveTests(unittest.TestCase):
    def required_text(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"missing {path}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def test_units_have_final_metadata_hours_anchors_and_training(self) -> None:
        theory = applied = 0.0
        exercises_total = answers_total = 0
        for unit in EXPECTED_UNITS:
            unit_id, title, th, ap, _suffix, exercises, answers = unit
            metadata, text = read_unit(unit_path(unit))
            with self.subTest(unit=unit_id):
                self.assertEqual(unit_id, metadata["unit_id"])
                self.assertEqual(title, metadata["title"])
                self.assertEqual(th, metadata["hours"]["theory"])
                self.assertEqual(ap, metadata["hours"]["applied"])
                self.assertEqual(2, metadata["content_standard"])
                self.assertIn(f"{{#{unit_id}}}", text)
                for anchor in REQUIRED_ANCHORS[unit_id]:
                    self.assertIn(f"{{#{anchor}}}", text)
                self.assertGreaterEqual(text.count("### 例 "), 2)
                checks = 3 if unit_id == "u-06-25-05" else 2
                self.assertGreaterEqual(text.count("### 即时检验 "), checks)
                actual_exercises = text.count(f"{{#pr-{unit_id}-")
                actual_answers = text.count('??? note "答案"')
                self.assertEqual(exercises, actual_exercises)
                self.assertEqual(answers, actual_answers)
                theory += float(metadata["hours"]["theory"])
                applied += float(metadata["hours"]["applied"])
                exercises_total += actual_exercises
                answers_total += actual_answers
        self.assertEqual(7.0, theory)
        self.assertEqual(2.0, applied)
        self.assertEqual(46, exercises_total)
        self.assertEqual(57, answers_total)

    def test_guide_opens_function_series_stage(self) -> None:
        guide = self.required_text(CHAPTER / "index.md")
        self.assertIn("本章共5个核心单元，9学时（理论7，应用2）。", guide)
        for marker in ("逐点收敛", "一致收敛", "一致 Cauchy", "M 判别", "连续", "积分", "微分", "第 24 章", "第 26 章"):
            self.assertIn(marker, guide)
        for unit_id, title, _th, _ap, suffix, _ex, _ans in EXPECTED_UNITS:
            self.assertEqual(1, guide.count(f"[{title}]({unit_id}-{suffix}.md)"))

    def test_pointwise_and_uniform_quantifiers_do_not_blur(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[0]))
        for marker in ("对每个", "依赖于", "与 x 无关", "上确界误差", "[0,1]", "不一致收敛"):
            self.assertIn(marker, text)
        self.assertIn(r"\forall x\in E", text)
        self.assertIn(r"\exists N", text)

    def test_uniform_cauchy_uses_completeness_and_uniform_tail(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[1]))
        for marker in ("实数完备性", "逐点构造", "一致 Cauchy", "任意有限尾段", "上确界为无穷", "不能"):
            self.assertIn(marker, text)
        self.assertIn(r"\|g\|_{\infty,E}=\sup_{x\in E}|g(x)|", text)

    def test_uniform_series_tests_keep_all_conditions(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[2]))
        for marker in ("Weierstrass M 判别", "一致绝对收敛", "逐点绝对收敛", "对 x 一致有界", "单调", "一致有界"):
            self.assertIn(marker, text)

    def test_continuity_and_integration_keep_sufficient_conditions(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[3]))
        for marker in ("连续函数列的一致极限连续", "闭区间", "Riemann 可积", "逐项积分", "逐点收敛不足", "充分条件"):
            self.assertIn(marker, text)

    def test_differentiation_requires_derivatives_and_one_base_point(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[4]))
        for marker in ("C^1([a,b])", "导数列", "一致收敛", "基点", "微积分基本定理", "一致收敛但", "不可微"):
            self.assertIn(marker, text)

    def test_core_does_not_depend_on_later_power_or_approximation_theory(self) -> None:
        for unit in EXPECTED_UNITS:
            core = self.required_text(unit_path(unit)).split("## 常见误区与后续", 1)[0]
            for forbidden in FORBIDDEN_CORE_TERMS:
                self.assertNotIn(forbidden, core)

    def test_publication_scope_reaches_chapter_25_only(self) -> None:
        dependencies = self.required_text(DEPENDENCIES)
        self.assertIn("当前发布边界：第 27 章", dependencies)
        self.assertIn("24 个核心单元、42 学时", dependencies)
        readme = self.required_text(ROOT / "README.md")
        self.assertIn("第六部第 27 章，共 122 个学习单元", readme)
        config = self.required_text(ROOT / "mkdocs.yml")
        self.assertIn("第 25 章：函数列、函数项级数与一致收敛", config)
        self.assertIn("chapters/chapter-27/", config)
