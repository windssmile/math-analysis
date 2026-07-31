from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-21"
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-05-dependencies.md"

EXPECTED_UNITS = [
    (
        "u-05-21-01",
        "面积怎样从局部条带与有向积分产生？",
        1.00,
        0.25,
        "area-models",
        6,
        8,
    ),
    (
        "u-05-21-02",
        "截面怎样重建立体体积？",
        1.00,
        0.50,
        "volume-models",
        8,
        10,
    ),
    (
        "u-05-21-03",
        "折线长度怎样逼近光滑图像的弧长？",
        1.00,
        0.25,
        "arc-length",
        6,
        8,
    ),
    (
        "u-05-21-04",
        "功、质量与平均值怎样选择局部贡献？",
        0.75,
        0.50,
        "work-mass-average",
        6,
        8,
    ),
    (
        "u-05-21-05",
        "几何与物理综合建模怎样选变量并回验？",
        0.25,
        1.50,
        "modeling-practice",
        12,
        16,
    ),
]

REQUIRED_ANCHORS = {
    "u-05-21-01": (
        "def-u-05-21-01-riemann-area",
        "thm-u-05-21-01-area-between-curves",
        "ex-u-05-21-01-signed-vs-geometric",
    ),
    "u-05-21-02": (
        "thm-u-05-21-02-cross-section-volume",
        "thm-u-05-21-02-washer-volume",
        "lem-u-05-21-02-shell-remainder",
        "thm-u-05-21-02-shell-volume",
    ),
    "u-05-21-03": (
        "def-u-05-21-03-polygonal-length",
        "def-u-05-21-03-graph-arc-length",
        "lem-u-05-21-03-refinement-monotonicity",
        "thm-u-05-21-03-c1-graph-arc-length",
    ),
    "u-05-21-04": (
        "thm-u-05-21-04-variable-force-work",
        "thm-u-05-21-04-linear-density-mass",
        "def-u-05-21-04-average-value",
        "tbl-u-05-21-04-unit-check",
    ),
    "u-05-21-05": (
        "alg-u-05-21-05-modeling-workflow",
        "tbl-u-05-21-05-model-selection",
        "ex-u-05-21-05-cross-model",
        "ex-u-05-21-05-error-diagnosis",
    ),
}

MINIMUM_EXAMPLES = {
    "u-05-21-01": 2,
    "u-05-21-02": 3,
    "u-05-21-03": 2,
    "u-05-21-04": 3,
    "u-05-21-05": 4,
}

MINIMUM_CHECKS = {
    "u-05-21-01": 2,
    "u-05-21-02": 2,
    "u-05-21-03": 2,
    "u-05-21-04": 2,
    "u-05-21-05": 4,
}

FORBIDDEN_CORE_TERMS = (
    "反常积分",
    "数值求积",
    "Simpson",
    "参数曲线",
    "曲面面积",
    "流体压力",
    "多重积分",
    "Lebesgue",
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


class ChapterTwentyOneTests(unittest.TestCase):
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
        self.assertEqual(4.0, theory)
        self.assertEqual(3.0, applied)
        self.assertEqual(38, total_exercises)
        self.assertEqual(50, total_answers)

    def test_chapter_guide_lists_units_hours_route_and_boundaries(self) -> None:
        guide = self.required_text(CHAPTER / "index.md")
        normalized_guide = "".join(guide.split())
        self.assertNotIn("本章验收后停在第21章", normalized_guide)
        self.assertNotIn("不创建第22章空白页面", normalized_guide)
        self.assertIn("本章共5个核心单元，7学时（理论4，应用3）。", guide)
        for marker in (
            "局部贡献",
            "分割近似",
            "Riemann 和极限",
            "单位、符号与数量级检查",
            "第 19 章",
            "第 20 章",
            "第 22 章",
        ):
            self.assertIn(marker, guide)
        for unit_id, title, _theory, _applied, suffix, _exercises, _answers in EXPECTED_UNITS:
            self.assertEqual(1, guide.count(f"[{title}]({unit_id}-{suffix}.md)"))

    def test_unit_one_separates_signed_and_geometric_area(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[0]))
        for marker in (
            "Riemann 面积",
            "有向积分",
            "几何面积",
            "上减下",
            "右减左",
            "换号点",
            "交点",
            "局部高度差",
        ):
            self.assertIn(marker, text)
        self.assertIn(r"A_{\mathrm{geom}}=\int_a^b |f(x)|\,dx", text)

    def test_unit_two_controls_shell_oscillation_and_remainder(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[1]))
        for marker in (
            "截面面积",
            "圆盘",
            "垫片",
            "柱壳",
            "一致连续",
            "振幅",
            "二次余项",
            "网格",
            "外半径",
            "内半径",
        ):
            self.assertIn(marker, text)
        self.assertIn(r"\pi M\lVert P\rVert(b-a)", text)
        self.assertIn(r"2\pi\int_a^b r\,h(r)\,dr", text)

    def test_unit_three_closes_polygonal_supremum_proof(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[2]))
        for marker in (
            "内接折线",
            "上确界",
            "分割加细",
            "三角不等式",
            "Lagrange 中值定理",
            "一致连续",
            "公共加细",
            "向量中值定理",
        ):
            self.assertIn(marker, text)
        self.assertIn(r"\sqrt{1+[f'(x)]^2}", text)
        self.assertIn(r"L(f,Q)\le L(f,P_n)", text)

    def test_unit_four_keeps_sign_density_and_unit_contracts(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[3]))
        for marker in (
            "局部功",
            "有向功",
            "位移方向",
            "线密度",
            "非负",
            "平均值",
            "端点平均",
            "单位",
        ):
            self.assertIn(marker, text)
        self.assertIn(r"W=\int_a^b F(x)\,dx", text)
        self.assertIn(r"\rho(x)\ge 0", text)

    def test_unit_five_has_mixed_training_and_diagnosis_density(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[4]))
        self.assertEqual(4, text.count("{#pr-u-05-21-05-mixed-"))
        self.assertEqual(3, text.count("{#pr-u-05-21-05-diagnosis-"))
        self.assertEqual(2, text.count("{#pr-u-05-21-05-boundary-"))
        self.assertEqual(3, text.count("{#pr-u-05-21-05-verification-"))
        for marker in (
            "识别所求量",
            "选择积分变量",
            "局部贡献",
            "确定区间与分段",
            "首个非法步骤",
            "横条",
            "竖条",
            "垫片",
            "柱壳",
            "弧长下界",
            "数量级",
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
        self.assertIn("25 个核心单元", deps)
        self.assertIn("当前发布边界：第 22 章", deps)
        self.assertIn("42.5 学时", deps)
        self.assertIn(
            "| `u-05-21-05` | `u-05-21-01`–`04`、`u-05-20-05` |",
            deps,
        )
        self.assertIn("第 21 章：积分的几何与物理模型", config)
        self.assertIn("本章学时：7 小时（理论 4，应用 3）。", course_map)
        self.assertIn("第六部第 27 章，共 125 个学习单元", readme)
        navigation_positions = []
        map_positions = []
        for unit_id, title, _theory, _applied, suffix, _exercises, _answers in EXPECTED_UNITS:
            path = f"chapters/chapter-21/{unit_id}-{suffix}.md"
            self.assertEqual(1, config.count(f"{title}: {path}"))
            self.assertEqual(1, course_map.count(f"[{title}]({path})"))
            navigation_positions.append(config.index(path))
            map_positions.append(course_map.index(path))
        self.assertEqual(sorted(navigation_positions), navigation_positions)
        self.assertEqual(sorted(map_positions), map_positions)


if __name__ == "__main__":
    unittest.main()
