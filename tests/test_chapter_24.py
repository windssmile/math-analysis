from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-24"
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-06-dependencies.md"

EXPECTED_UNITS = [
    ("u-06-24-01", "绝对收敛为什么能够控制符号变化？", 1.50, 0.25, "absolute-conditional", 8, 10),
    ("u-06-24-02", "交错与振荡级数怎样利用抵消？", 1.50, 0.50, "leibniz-dirichlet-abel", 9, 11),
    ("u-06-24-03", "改变求和次序为什么可能改变结果？", 1.75, 0.25, "rearrangements", 10, 12),
    ("u-06-24-04", "两个无穷和什么时候可以相乘？", 1.75, 0.25, "cauchy-products", 9, 11),
    ("u-06-24-05", "怎样选择判别法并给出收敛证书？", 1.00, 0.75, "series-diagnosis", 12, 15),
]

REQUIRED_ANCHORS = {
    "u-06-24-01": (
        "def-u-06-24-01-absolute-conditional",
        "thm-u-06-24-01-absolute-implies-convergence",
        "thm-u-06-24-01-positive-negative-parts",
    ),
    "u-06-24-02": (
        "thm-u-06-24-02-leibniz",
        "cor-u-06-24-02-alternating-remainder",
        "lem-u-06-24-02-summation-by-parts",
        "thm-u-06-24-02-dirichlet",
        "cor-u-06-24-02-abel",
    ),
    "u-06-24-03": (
        "def-u-06-24-03-rearrangement",
        "thm-u-06-24-03-absolute-rearrangement",
        "lem-u-06-24-03-positive-negative-diverge",
        "thm-u-06-24-03-riemann-rearrangement",
    ),
    "u-06-24-04": (
        "def-u-06-24-04-cauchy-product",
        "thm-u-06-24-04-mertens",
        "ex-u-06-24-04-conditional-failure",
    ),
    "u-06-24-05": (
        "alg-u-06-24-05-decision-workflow",
        "tbl-u-06-24-05-test-boundaries",
        "tbl-u-06-24-05-operation-safety",
    ),
}

FORBIDDEN_CORE_TERMS = (
    "函数项级数",
    "一致收敛",
    "幂级数",
    "Fourier 级数",
    "Lebesgue 积分",
    "Fubini",
    "Tonelli",
)


def unit_path(unit: tuple[str, str, float, float, str, int, int]) -> Path:
    unit_id, _title, _theory, _applied, suffix, _exercises, _answers = unit
    return CHAPTER / f"{unit_id}-{suffix}.md"


def read_unit(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    metadata = yaml.safe_load(text.split("---\n", 2)[1])
    return metadata, text


class ChapterTwentyFourTests(unittest.TestCase):
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
                checks = 3 if unit_id == "u-06-24-05" else 2
                self.assertGreaterEqual(text.count("### 即时检验 "), checks)
                actual_exercises = text.count(f"{{#pr-{unit_id}-")
                actual_answers = text.count('??? note "答案"')
                self.assertEqual(exercises, actual_exercises)
                self.assertEqual(answers, actual_answers)
                theory += float(metadata["hours"]["theory"])
                applied += float(metadata["hours"]["applied"])
                exercises_total += actual_exercises
                answers_total += actual_answers
        self.assertEqual(7.5, theory)
        self.assertEqual(2.0, applied)
        self.assertEqual(48, exercises_total)
        self.assertEqual(59, answers_total)

    def test_guide_closes_the_number_series_stage(self) -> None:
        guide = self.required_text(CHAPTER / "index.md")
        self.assertIn("本章共5个核心单元，9.5学时（理论7.5，应用2）。", guide)
        for marker in (
            "绝对值控制",
            "条件抵消",
            "分部求和",
            "Dirichlet–Abel",
            "重排",
            "乘积",
            "综合诊断",
            "第 23 章",
            "第 25 章",
        ):
            self.assertIn(marker, guide)
        for unit_id, title, _th, _ap, suffix, _ex, _ans in EXPECTED_UNITS:
            self.assertEqual(1, guide.count(f"[{title}]({unit_id}-{suffix}.md)"))

    def test_absolute_convergence_uses_cauchy_tails_and_parts(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[0]))
        for marker in ("绝对收敛推出收敛", "Cauchy 尾部", "正部", "负部", "条件收敛", "抵消"):
            self.assertIn(marker, text)
        self.assertIn(r"a_n^+=\max\{a_n,0\}", text)
        self.assertIn(r"a_n^-=\max\{-a_n,0\}", text)

    def test_leibniz_dirichlet_abel_conditions_are_visible(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[1]))
        for marker in (
            "单调递减",
            "趋于零",
            "首个被舍项",
            "有限分部求和",
            "部分和有界",
            "Dirichlet 判别",
            "Abel 判别",
        ):
            self.assertIn(marker, text)

    def test_rearrangement_proofs_keep_absolute_and_conditional_boundaries(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[2]))
        for marker in (
            "双射",
            "绝对收敛级数重排不变",
            "正项总量",
            "负项总量",
            "越过目标",
            "回拉",
            "超调趋于零",
        ):
            self.assertIn(marker, text)

    def test_mertens_keeps_square_triangle_and_absolute_factor(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[3]))
        for marker in (
            "方形截断",
            "三角截断",
            "至少一个",
            "绝对收敛",
            "Mertens 定理",
            "形式乘法",
        ):
            self.assertIn(marker, text)

    def test_diagnosis_separates_inconclusive_from_divergent(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[4]))
        for marker in (
            "判别失败不等于发散",
            "对象类型",
            "条件检查",
            "结论强度",
            "余项上界",
            "重排",
            "乘积",
        ):
            self.assertIn(marker, text)

    def test_core_does_not_use_later_function_series_theory(self) -> None:
        for unit in EXPECTED_UNITS:
            core = self.required_text(unit_path(unit)).split("## 常见误区与后续", 1)[0]
            for forbidden in FORBIDDEN_CORE_TERMS:
                self.assertNotIn(forbidden, core)

    def test_publication_scope_includes_chapter_24_without_future_placeholders(self) -> None:
        dependencies = self.required_text(DEPENDENCIES)
        self.assertIn("当前发布边界：第 26 章", dependencies)
        self.assertIn("20 个核心单元、35 学时", dependencies)
        readme = self.required_text(ROOT / "README.md")
        self.assertIn("第六部第 26 章，共 118 个学习单元", readme)
        config = self.required_text(ROOT / "mkdocs.yml")
        self.assertIn("第 24 章：一般项级数、重排与乘积", config)
        self.assertNotIn("chapters/chapter-27/", config)
