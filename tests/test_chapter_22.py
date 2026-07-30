from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-22"
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-05-dependencies.md"
MASTER_DESIGN = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-07-18-mathematical-analysis-textbook-design.md"
)

EXPECTED_UNITS = [
    (
        "u-05-22-01",
        "反常积分怎样由逐端点极限定义？",
        1.50,
        0.25,
        "improper-definition",
        6,
        8,
    ),
    (
        "u-05-22-02",
        "正函数怎样比较收敛并控制尾部？",
        1.50,
        0.25,
        "comparison-tests",
        7,
        9,
    ),
    (
        "u-05-22-03",
        "绝对、条件与振荡收敛怎样区分？",
        1.50,
        0.50,
        "absolute-conditional-oscillation",
        8,
        10,
    ),
    (
        "u-05-22-04",
        "中点与梯形公式怎样产生可证明误差界？",
        1.25,
        0.75,
        "midpoint-trapezoid",
        7,
        9,
    ),
    (
        "u-05-22-05",
        "Simpson 方法怎样给出预算与误差证书？",
        1.00,
        1.25,
        "simpson-certificates",
        8,
        10,
    ),
    (
        "u-05-22-06",
        "反常积分怎样完成可靠数值计算？",
        0.50,
        1.75,
        "certified-improper-quadrature",
        12,
        16,
    ),
]

REQUIRED_ANCHORS = {
    "u-05-22-01": (
        "def-u-05-22-01-infinite-interval-improper-integral",
        "def-u-05-22-01-singular-endpoint-improper-integral",
        "thm-u-05-22-01-cauchy-tail-criterion",
        "ex-u-05-22-01-p-integrals",
    ),
    "u-05-22-02": (
        "thm-u-05-22-02-direct-comparison",
        "thm-u-05-22-02-limit-comparison",
        "cor-u-05-22-02-tail-bound",
        "ex-u-05-22-02-tail-budget",
    ),
    "u-05-22-03": (
        "thm-u-05-22-03-absolute-implies-convergence",
        "thm-u-05-22-03-dirichlet-test",
        "cor-u-05-22-03-abel-test",
        "ex-u-05-22-03-conditional-sine-over-x",
        "ex-u-05-22-03-principal-value-boundary",
    ),
    "u-05-22-04": (
        "alg-u-05-22-04-composite-midpoint",
        "thm-u-05-22-04-midpoint-error",
        "alg-u-05-22-04-composite-trapezoid",
        "thm-u-05-22-04-trapezoid-error",
    ),
    "u-05-22-05": (
        "alg-u-05-22-05-composite-simpson",
        "thm-u-05-22-05-simpson-error",
        "alg-u-05-22-05-certified-simpson-budget",
        "ex-u-05-22-05-budget-exhaustion",
    ),
    "u-05-22-06": (
        "alg-u-05-22-06-total-error-workflow",
        "thm-u-05-22-06-total-error-certificate",
        "ex-u-05-22-06-exponential-baseline",
        "ex-u-05-22-06-gaussian-tail-budget",
        "ex-u-05-22-06-uncertified-grid-difference",
    ),
}

MINIMUM_EXAMPLES = {
    "u-05-22-01": 2,
    "u-05-22-02": 2,
    "u-05-22-03": 3,
    "u-05-22-04": 3,
    "u-05-22-05": 3,
    "u-05-22-06": 3,
}

MINIMUM_CHECKS = {
    "u-05-22-01": 2,
    "u-05-22-02": 2,
    "u-05-22-03": 2,
    "u-05-22-04": 2,
    "u-05-22-05": 2,
    "u-05-22-06": 4,
}

FORBIDDEN_CORE_TERMS = (
    "无穷级数判别",
    "幂级数展开",
    "一致收敛",
    "Euler–Maclaurin",
    "Romberg",
    "自适应求积",
    "Gauss 求积",
    "Lebesgue 积分",
    "含参反常积分",
    "Gamma 函数",
    "Beta 函数",
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


class ChapterTwentyTwoTests(unittest.TestCase):
    def required_text(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"missing {path}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def test_units_have_final_metadata_hours_anchors_and_training(self) -> None:
        theory = 0.0
        applied = 0.0
        total_exercises = 0
        total_answers = 0
        for unit in EXPECTED_UNITS:
            (
                unit_id,
                title,
                theory_hours,
                applied_hours,
                _suffix,
                exercises,
                answers,
            ) = unit
            path = unit_path(unit)
            with self.subTest(unit=unit_id):
                self.assertTrue(path.is_file(), f"missing {path.name}")
                if not path.is_file():
                    continue
                metadata, text = read_unit(path)
                self.assertEqual(unit_id, metadata["unit_id"])
                self.assertEqual(title, metadata["title"])
                self.assertEqual(theory_hours, metadata["hours"]["theory"])
                self.assertEqual(applied_hours, metadata["hours"]["applied"])
                self.assertEqual(2, metadata["content_standard"])
                for anchor in REQUIRED_ANCHORS[unit_id]:
                    self.assertIn(f"{{#{anchor}}}", text)
                self.assertGreaterEqual(
                    text.count("### 例 "),
                    MINIMUM_EXAMPLES[unit_id],
                )
                self.assertGreaterEqual(
                    text.count("### 即时检验 "),
                    MINIMUM_CHECKS[unit_id],
                )
                actual_exercises = text.count(f"{{#pr-{unit_id}-")
                actual_answers = text.count('??? note "答案"')
                self.assertEqual(exercises, actual_exercises)
                self.assertEqual(answers, actual_answers)
                total_exercises += actual_exercises
                total_answers += actual_answers
                theory += float(metadata["hours"]["theory"])
                applied += float(metadata["hours"]["applied"])
        self.assertEqual(7.25, theory)
        self.assertEqual(4.75, applied)
        self.assertEqual(48, total_exercises)
        self.assertEqual(62, total_answers)

    def test_chapter_guide_lists_units_hours_routes_and_boundaries(self) -> None:
        guide = self.required_text(CHAPTER / "index.md")
        self.assertIn("本章共6个核心单元，12学时（理论7.25，应用4.75）。", guide)
        for marker in (
            "逐端点极限",
            "Cauchy 尾部",
            "局部近似",
            "误差界",
            "预算与停止状态",
            "第 19 章",
            "第 20 章",
            "第 21 章",
            "第五部",
            "第六部",
        ):
            self.assertIn(marker, guide)
        for unit_id, title, _theory, _applied, suffix, _exercises, _answers in EXPECTED_UNITS:
            self.assertEqual(1, guide.count(f"[{title}]({unit_id}-{suffix}.md)"))

    def test_unit_one_defines_every_improper_endpoint_separately(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[0]))
        for marker in (
            "局部 Riemann 可积",
            "逐端点",
            "Cauchy 尾部判据",
            "切分点无关",
            "内部奇点",
            "对称主值",
        ):
            self.assertIn(marker, text)
        self.assertIn(r"\int_1^\infty x^{-p}\,dx", text)
        self.assertIn(r"\int_0^1 x^{-p}\,dx", text)

    def test_unit_two_keeps_comparison_directions_and_tail_bounds(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[1]))
        for marker in (
            "最终成立",
            "直接比较",
            "极限比较",
            "上方函数收敛",
            "下方函数发散",
            "L=0",
            r"L=\infty",
            "尾部误差",
        ):
            self.assertIn(marker, text)

    def test_unit_three_proves_oscillation_contracts(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[2]))
        for marker in (
            "绝对收敛推出收敛",
            "Dirichlet 判别",
            "Abel 判别",
            "条件收敛",
            "有界原函数",
            "单调递减",
            "Cauchy 主值",
        ):
            self.assertIn(marker, text)
        self.assertIn(r"\int_1^\infty\frac{\sin x}{x}\,dx", text)

    def test_unit_four_has_both_second_derivative_error_constants(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[3]))
        self.assertIn(r"\frac{b-a}{24}M_2h^2", text)
        self.assertIn(r"\frac{b-a}{12}M_2h^2", text)
        self.assertIn("整个区间", text)

    def test_unit_five_keeps_simpson_certificate_semantics(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[4]))
        self.assertIn(r"\frac{b-a}{180}M_4h^4", text)
        for marker in (
            "正偶数",
            "三次多项式",
            "反复 Rolle",
            "调用者",
            "budget_exhausted",
            "target_met",
            "浮点舍入误差",
        ):
            self.assertIn(marker, text)

    def test_unit_six_has_locked_total_error_training(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[5]))
        self.assertEqual(4, text.count("{#pr-u-05-22-06-mixed-"))
        self.assertEqual(3, text.count("{#pr-u-05-22-06-diagnosis-"))
        self.assertEqual(2, text.count("{#pr-u-05-22-06-boundary-"))
        self.assertEqual(3, text.count("{#pr-u-05-22-06-verification-"))
        for marker in (
            "先证明收敛",
            "尾部误差预算",
            "求积误差预算",
            "三角不等式",
            "导数界",
            "总误差证书",
        ):
            self.assertIn(marker, text)

    def test_core_does_not_use_later_or_out_of_scope_theory(self) -> None:
        for unit in EXPECTED_UNITS:
            path = unit_path(unit)
            if not path.is_file():
                continue
            core = path.read_text(encoding="utf-8").split("## 常见误区与后续", 1)[0]
            with self.subTest(unit=unit[0]):
                for term in FORBIDDEN_CORE_TERMS:
                    self.assertNotIn(term, core)

    def test_dependency_map_and_publication_scope(self) -> None:
        deps = self.required_text(DEPENDENCIES)
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        course_map = (ROOT / "content" / "course-map.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        master = self.required_text(MASTER_DESIGN)
        self.assertIn("25 个核心单元", deps)
        self.assertIn("当前发布边界：第 22 章", deps)
        self.assertIn("42.5 学时", deps)
        self.assertIn(
            "| `u-05-22-06` | `u-05-22-01`–`05` |",
            deps,
        )
        self.assertIn("第 22 章：反常积分与数值求积", config)
        self.assertIn(
            "本章学时：12 小时（理论 7.25，应用 4.75）。",
            course_map,
        )
        self.assertIn("第六部第 23 章，共 103 个学习单元", readme)
        self.assertIn(
            "| **当前总计** |  | **292.75** | **101.25** | **394** |",
            master,
        )
        navigation_positions = []
        map_positions = []
        for unit_id, title, _theory, _applied, suffix, _exercises, _answers in EXPECTED_UNITS:
            path = f"chapters/chapter-22/{unit_id}-{suffix}.md"
            self.assertEqual(1, config.count(f"{title}: {path}"))
            self.assertEqual(1, course_map.count(f"[{title}]({path})"))
            navigation_positions.append(config.index(path))
            map_positions.append(course_map.index(path))
        self.assertEqual(sorted(navigation_positions), navigation_positions)
        self.assertEqual(sorted(map_positions), map_positions)


if __name__ == "__main__":
    unittest.main()
