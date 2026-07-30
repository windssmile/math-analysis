from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-23"
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-06-dependencies.md"

EXPECTED_UNITS = [
    ("u-06-23-01", "无限求和怎样由部分和定义？", 1.25, 0.25, "partial-sums", 7, 9),
    ("u-06-23-02", "Cauchy 尾部判据怎样控制无限求和？", 1.50, 0.25, "cauchy-tail", 7, 9),
    ("u-06-23-03", "正项级数怎样通过比较判断收敛？", 1.25, 0.50, "comparison-tests", 8, 10),
    ("u-06-23-04", "局部增长率怎样产生比值与根值判别？", 1.25, 0.50, "ratio-root-tests", 8, 10),
    ("u-06-23-05", "积分与凝聚怎样提供判别和余项证书？", 1.25, 0.50, "integral-condensation", 10, 13),
]

REQUIRED_ANCHORS = {
    "u-06-23-01": (
        "def-u-06-23-01-series-convergence",
        "def-u-06-23-01-remainder",
        "thm-u-06-23-01-term-necessary",
        "ex-u-06-23-01-geometric",
        "ex-u-06-23-01-telescoping",
    ),
    "u-06-23-02": (
        "thm-u-06-23-02-cauchy-tail",
        "ex-u-06-23-02-harmonic-failure",
        "ex-u-06-23-02-epsilon-budget",
        "tbl-u-06-23-02-evidence-boundary",
    ),
    "u-06-23-03": (
        "thm-u-06-23-03-positive-monotone",
        "thm-u-06-23-03-direct-comparison",
        "thm-u-06-23-03-limit-comparison",
        "cor-u-06-23-03-tail-bound",
    ),
    "u-06-23-04": (
        "thm-u-06-23-04-ratio-test",
        "thm-u-06-23-04-root-test",
        "thm-u-06-23-04-limsup-forms",
        "ex-u-06-23-04-critical-one",
    ),
    "u-06-23-05": (
        "thm-u-06-23-05-integral-test",
        "cor-u-06-23-05-integral-tail-bounds",
        "thm-u-06-23-05-cauchy-condensation",
        "ex-u-06-23-05-p-series",
        "ex-u-06-23-05-logarithmic-family",
        "alg-u-06-23-05-certified-truncation",
    ),
}

FORBIDDEN_CORE_TERMS = (
    "交错级数判别",
    "Riemann 重排",
    "Cauchy 乘积",
    "Mertens 定理",
    "函数项级数",
    "一致收敛",
    "幂级数",
    "Fourier 级数",
    "Lebesgue 积分",
)


def unit_path(
    unit: tuple[str, str, float, float, str, int, int],
) -> Path:
    unit_id, _title, _theory, _applied, suffix, _exercises, _answers = unit
    return CHAPTER / f"{unit_id}-{suffix}.md"


def read_unit(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    metadata = yaml.safe_load(text.split("---\n", 2)[1])
    return metadata, text


class ChapterTwentyThreeTests(unittest.TestCase):
    def required_text(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"missing {path}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def test_units_have_final_metadata_hours_anchors_and_training(self) -> None:
        theory = 0.0
        applied = 0.0
        total_exercises = 0
        total_answers = 0
        for unit in EXPECTED_UNITS:
            unit_id, title, theory_hours, applied_hours, _suffix, exercises, answers = unit
            path = unit_path(unit)
            with self.subTest(unit=unit_id):
                metadata, text = read_unit(path)
                self.assertEqual(unit_id, metadata["unit_id"])
                self.assertEqual(title, metadata["title"])
                self.assertEqual(theory_hours, metadata["hours"]["theory"])
                self.assertEqual(applied_hours, metadata["hours"]["applied"])
                self.assertEqual(2, metadata["content_standard"])
                self.assertIn(f"{{#{unit_id}}}", text)
                for anchor in REQUIRED_ANCHORS[unit_id]:
                    self.assertIn(f"{{#{anchor}}}", text)
                self.assertGreaterEqual(text.count("### 例 "), 2)
                self.assertGreaterEqual(text.count("### 即时检验 "), 2)
                actual_exercises = text.count(f"{{#pr-{unit_id}-")
                actual_answers = text.count('??? note "答案"')
                self.assertEqual(exercises, actual_exercises)
                self.assertEqual(answers, actual_answers)
                theory += float(metadata["hours"]["theory"])
                applied += float(metadata["hours"]["applied"])
                total_exercises += actual_exercises
                total_answers += actual_answers
        self.assertEqual(6.5, theory)
        self.assertEqual(2.0, applied)
        self.assertEqual(40, total_exercises)
        self.assertEqual(51, total_answers)

    def test_chapter_guide_lists_units_hours_route_and_boundaries(self) -> None:
        guide = self.required_text(CHAPTER / "index.md")
        self.assertIn("本章共5个核心单元，8.5学时（理论6.5，应用2）。", guide)
        for marker in (
            "部分和",
            "Cauchy 尾部",
            "正项级数",
            "比较判别",
            "比值与根值",
            "积分与凝聚",
            "余项证书",
            "第 22 章",
            "第 24 章",
        ):
            self.assertIn(marker, guide)
        for unit_id, title, _theory, _applied, suffix, _exercises, _answers in EXPECTED_UNITS:
            self.assertEqual(1, guide.count(f"[{title}]({unit_id}-{suffix}.md)"))

    def test_unit_one_does_not_confuse_terms_and_partial_sums(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[0]))
        for marker in ("部分和", "通项趋于零只是必要条件", "有限项", "余项", "几何级数", "伸缩级数"):
            self.assertIn(marker, text)
        self.assertIn(r"\sum_{n=1}^{\infty}\frac1n", text)

    def test_unit_two_uses_arbitrary_finite_tails(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[1]))
        for marker in ("任意有限尾段", "n>m", "实数完备性", "相邻部分和差", "不能证明收敛"):
            self.assertIn(marker, text)

    def test_unit_three_keeps_both_comparison_directions(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[2]))
        for marker in ("最终成立", "上方级数收敛", "下方级数发散", "正有限极限", "L=0", r"L=\infty", "余项上界"):
            self.assertIn(marker, text)

    def test_unit_four_keeps_critical_value_and_limsup_boundaries(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[3]))
        for marker in ("临界值 1", "无结论", "上极限", "最终几何控制", "比值极限不存在", "根值判别"):
            self.assertIn(marker, text)

    def test_unit_five_requires_positive_decreasing_integral_model(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[4]))
        for marker in ("最终非负", "单调递减", "积分判别", "Cauchy 凝聚", "尾项上下界", "截断预算", "调用者已经证明"):
            self.assertIn(marker, text)
        self.assertIn(r"\sum_{n=1}^{\infty}\frac1{n^p}", text)

    def test_core_does_not_use_later_series_theory(self) -> None:
        for unit in EXPECTED_UNITS:
            text = self.required_text(unit_path(unit))
            core = text.split("## 常见误区与后续", 1)[0]
            for forbidden in FORBIDDEN_CORE_TERMS:
                self.assertNotIn(forbidden, core)

    def test_dependency_map_and_publication_scope(self) -> None:
        dependencies = self.required_text(DEPENDENCIES)
        self.assertIn("24 个核心单元，42 学时", dependencies)
        self.assertIn("当前发布边界：第 24 章", dependencies)
        self.assertIn("当前已发布第六部 10 个核心单元、18 学时", dependencies)
        readme = self.required_text(ROOT / "README.md")
        self.assertIn("第六部第 24 章，共 108 个学习单元", readme)
        config = self.required_text(ROOT / "mkdocs.yml")
        self.assertIn("第六部：无穷级数与函数逼近", config)
        self.assertIn("第 23 章：数项级数的收敛与正项判别", config)
