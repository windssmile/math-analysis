from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-20"
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-05-dependencies.md"

EXPECTED_UNITS = [
    (
        "u-05-20-01",
        "变上限累积函数为什么连续？",
        1.25,
        0.25,
        "accumulation-continuity",
        6,
        8,
    ),
    (
        "u-05-20-02",
        "局部平均怎样恢复被积函数？",
        1.50,
        0.25,
        "fundamental-theorem-part-one",
        6,
        8,
    ),
    (
        "u-05-20-03",
        "原函数怎样把分割极限化为端点差？",
        1.25,
        0.50,
        "newton-leibniz",
        6,
        8,
    ),
    (
        "u-05-20-04",
        "定积分的换元与分部积分怎样合法使用？",
        1.00,
        1.00,
        "definite-substitution-parts",
        8,
        10,
    ),
    (
        "u-05-20-05",
        "定积分综合计算怎样处理端点、对称与错误诊断？",
        0.25,
        0.75,
        "definite-integral-practice",
        12,
        14,
    ),
]

REQUIRED_ANCHORS = {
    "u-05-20-01": (
        "def-u-05-20-01-accumulation-function",
        "thm-u-05-20-01-lipschitz-continuity",
        "cor-u-05-20-01-basepoint-shift",
        "ex-u-05-20-01-step-accumulation",
    ),
    "u-05-20-02": (
        "lem-u-05-20-02-local-average-control",
        "thm-u-05-20-02-ftc-part-one-pointwise",
        "cor-u-05-20-02-continuous-integrand",
        "ex-u-05-20-02-jump-boundary",
        "ex-u-05-20-02-single-point-redefinition",
    ),
    "u-05-20-03": (
        "thm-u-05-20-03-continuous-primitive-existence",
        "thm-u-05-20-03-newton-leibniz-continuous",
        "thm-u-05-20-03-newton-leibniz-integrable-derivative",
        "tbl-u-05-20-03-existence-representation-computation",
        "ex-u-05-20-03-gaussian-boundary",
    ),
    "u-05-20-04": (
        "thm-u-05-20-04-definite-substitution",
        "tbl-u-05-20-04-forward-vs-inverse-substitution",
        "ex-u-05-20-04-decreasing-substitution",
        "thm-u-05-20-04-definite-integration-by-parts",
        "cor-u-05-20-04-piecewise-rules",
    ),
    "u-05-20-05": (
        "tbl-u-05-20-05-method-selection",
        "thm-u-05-20-05-reflection-symmetry",
        "cor-u-05-20-05-even-odd",
        "cor-u-05-20-05-period-shift",
        "ex-u-05-20-05-cyclic-parts",
        "ex-u-05-20-05-illegal-substitution",
    ),
}

MINIMUM_EXAMPLES = {
    "u-05-20-01": 2,
    "u-05-20-02": 2,
    "u-05-20-03": 2,
    "u-05-20-04": 3,
    "u-05-20-05": 4,
}

MINIMUM_CHECKS = {
    "u-05-20-01": 2,
    "u-05-20-02": 2,
    "u-05-20-03": 2,
    "u-05-20-04": 2,
    "u-05-20-05": 4,
}

FORBIDDEN_CORE_TERMS = (
    "反常积分",
    "主值积分",
    "数值求积",
    "Simpson",
    "积分号下求导",
    "Lebesgue",
    "旋转体",
    "弧长公式",
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


class ChapterTwentyTests(unittest.TestCase):
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
                self.assertGreaterEqual(actual_exercises, exercises)
                self.assertGreaterEqual(actual_answers, answers)
                total_exercises += actual_exercises
                total_answers += actual_answers
                theory += float(metadata["hours"]["theory"])
                applied += float(metadata["hours"]["applied"])
        self.assertEqual(5.25, theory)
        self.assertEqual(2.75, applied)
        self.assertGreaterEqual(total_exercises, 38)
        self.assertGreaterEqual(total_answers, 48)

    def test_chapter_guide_lists_units_hours_route_and_boundaries(self) -> None:
        guide = self.required_text(CHAPTER / "index.md")
        self.assertIn("本章共5个核心单元，8学时（理论5.25，应用2.75）。", guide)
        for marker in (
            "Riemann 分割极限",
            "变上限累积函数",
            "局部变化率",
            "原函数端点差",
            "第 18 章",
            "第 19 章",
            "第 21 章",
        ):
            self.assertIn(marker, guide)
        for unit_id, title, _theory, _applied, suffix, _exercises, _answers in EXPECTED_UNITS:
            self.assertEqual(1, guide.count(f"[{title}]({unit_id}-{suffix}.md)"))

    def test_unit_one_proves_continuity_from_integral_bounds(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[0]))
        for marker in (
            "Riemann 可积",
            "有界",
            "区间可加",
            "Lipschitz",
            "一致连续",
            "不同基点",
            r"|A_c(y)-A_c(x)|",
            r"M|y-x|",
        ):
            self.assertIn(marker, text)

    def test_unit_two_recovers_only_continuity_points(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[1]))
        for marker in (
            "局部平均",
            "连续点",
            "右导数",
            "左导数",
            "阶跃",
            "单点改值",
            "充分条件",
            "不是必要条件",
        ):
            self.assertIn(marker, text)
        self.assertIn(r"A'(x_0)=f(x_0)", text)

    def test_unit_three_separates_two_newton_leibniz_levels(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[2]))
        for marker in (
            "连续函数",
            "原函数存在",
            "相差常数",
            "已有原函数",
            "Lagrange 中值定理",
            "Riemann 和",
            "初等原函数",
            r"e^{-x^2}",
        ):
            self.assertIn(marker, text)
        self.assertIn(r"G(b)-G(a)", text)

    def test_unit_four_derives_rules_with_conditions(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[3]))
        for marker in (
            "链式法则",
            "乘积法则",
            "不要求",
            "单调",
            "反解变量",
            "递减",
            "边界项",
            "分段",
            "全局连续",
        ):
            self.assertIn(marker, text)
        self.assertIn(r"\phi\in C^1", text)
        self.assertIn(r"[u(x)v(x)]_a^b", text)

    def test_unit_five_has_mixed_training_and_diagnosis_density(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[4]))
        self.assertGreaterEqual(text.count("{#pr-u-05-20-05-mixed-"), 4)
        self.assertGreaterEqual(text.count("{#pr-u-05-20-05-diagnosis-"), 3)
        self.assertGreaterEqual(text.count("{#pr-u-05-20-05-boundary-"), 2)
        for marker in (
            "区间与定义域",
            "结构识别",
            "路线选择",
            "中点反射",
            "奇函数",
            "偶函数",
            "周期",
            "循环分部积分",
            "首个非法步骤",
            "数值点检只能",
        ):
            self.assertIn(marker, text)

    def test_core_does_not_use_later_integral_theory(self) -> None:
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
        self.assertIn("25 个核心单元", deps)
        self.assertIn("当前发布边界：第 22 章", deps)
        self.assertIn(
            "| `u-05-20-05` | `u-05-20-04`、`u-05-19-04` |",
            deps,
        )
        self.assertIn("第 20 章：微积分基本定理", config)
        self.assertIn("本章学时：8 小时（理论 5.25，应用 2.75）。", course_map)
        self.assertIn("第六部第 24 章，共 108 个学习单元", readme)
        navigation_positions = []
        map_positions = []
        for unit_id, title, _theory, _applied, suffix, _exercises, _answers in EXPECTED_UNITS:
            path = f"chapters/chapter-20/{unit_id}-{suffix}.md"
            self.assertEqual(1, config.count(f"{title}: {path}"))
            self.assertEqual(1, course_map.count(f"[{title}]({path})"))
            navigation_positions.append(config.index(path))
            map_positions.append(course_map.index(path))
        self.assertEqual(sorted(navigation_positions), navigation_positions)
        self.assertEqual(sorted(map_positions), map_positions)


if __name__ == "__main__":
    unittest.main()
