from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-19"
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-05-dependencies.md"

EXPECTED_UNITS = [
    (
        "u-05-19-01",
        "怎样用分割和上下和夹住未知总量？",
        1.50,
        0.25,
        "partitions-darboux-sums",
        6,
    ),
    (
        "u-05-19-02",
        "Riemann 和何时拥有与取样无关的极限？",
        1.50,
        0.25,
        "riemann-darboux-equivalence",
        6,
    ),
    (
        "u-05-19-03",
        "哪些函数可积，证明障碍在哪里？",
        1.75,
        0.25,
        "integrable-classes",
        8,
    ),
    (
        "u-05-19-04",
        "可积函数的代数、序与区间结构怎样传递？",
        1.25,
        0.75,
        "integral-properties",
        8,
    ),
]

REQUIRED_ANCHORS = {
    "u-05-19-01": (
        "def-u-05-19-01-partition-mesh",
        "def-u-05-19-01-darboux-sums",
        "thm-u-05-19-01-refinement-monotonicity",
        "ex-u-05-19-01-linear-uniform-partition",
    ),
    "u-05-19-02": (
        "def-u-05-19-02-darboux-integrable",
        "def-u-05-19-02-riemann-integrable",
        "thm-u-05-19-02-darboux-criterion",
        "lem-u-05-19-02-common-refinement-control",
        "thm-u-05-19-02-riemann-darboux-equivalence",
    ),
    "u-05-19-03": (
        "thm-u-05-19-03-continuous-integrable",
        "thm-u-05-19-03-monotone-integrable",
        "cor-u-05-19-03-piecewise-continuous-integrable",
        "ex-u-05-19-03-dirichlet-obstruction",
    ),
    "u-05-19-04": (
        "thm-u-05-19-04-algebra-closure",
        "thm-u-05-19-04-order-bounds",
        "thm-u-05-19-04-interval-additivity",
        "tbl-u-05-19-04-property-conditions",
    ),
}

FORBIDDEN_CORE_TERMS = (
    "Newton–Leibniz",
    "微积分基本定理",
    "积分上限函数",
    "反常积分",
    "Lebesgue",
)


def unit_path(unit: tuple[str, str, float, float, str, int]) -> Path:
    unit_id, _title, _theory, _applied, suffix, _exercises = unit
    return CHAPTER / f"{unit_id}-{suffix}.md"


def read_unit(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    metadata = yaml.safe_load(text.split("---\n", 2)[1])
    return metadata, text


class ChapterNineteenTests(unittest.TestCase):
    def required_text(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"missing {path}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def test_units_have_final_metadata_hours_anchors_and_training(self) -> None:
        theory = 0.0
        applied = 0.0
        total_exercises = 0
        for unit in EXPECTED_UNITS:
            unit_id, title, theory_hours, applied_hours, _suffix, exercises = unit
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
                actual = text.count(f"{{#pr-{unit_id}-")
                self.assertGreaterEqual(actual, exercises)
                self.assertGreaterEqual(text.count('??? note "答案"'), exercises + 2)
                total_exercises += actual
                theory += float(metadata["hours"]["theory"])
                applied += float(metadata["hours"]["applied"])
        self.assertEqual(6.0, theory)
        self.assertEqual(1.5, applied)
        self.assertGreaterEqual(total_exercises, 28)

    def test_chapter_guide_lists_units_hours_route_and_boundaries(self) -> None:
        guide = self.required_text(CHAPTER / "index.md")
        self.assertIn("本章共4个核心单元，7.5学时（理论6，应用1.5）。", guide)
        self.assertIn("Riemann 取样和建立直觉", guide)
        self.assertIn("Darboux 上下和承担证明", guide)
        self.assertIn("第 18 章", guide)
        self.assertIn("第 20 章", guide)
        for unit_id, title, _theory, _applied, suffix, _exercises in EXPECTED_UNITS:
            self.assertEqual(1, guide.count(f"[{title}]({unit_id}-{suffix}.md)"))

    def test_unit_one_builds_partition_and_refinement_language(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[0]))
        for marker in (
            "标记分割",
            "网格",
            "上和",
            "下和",
            "加细",
            "公共加细",
            r"L(f,P)\le",
            r"S(f;P,\xi)",
            r"U(f,P)",
        ):
            self.assertIn(marker, text)

    def test_unit_two_proves_definitions_equivalent_without_refinement_shortcut(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[1]))
        for marker in (
            "所有分割",
            "所有取样点",
            "不一定加细",
            "公共加细",
            "逼近上确界",
            "逼近下确界",
            "等价",
        ):
            self.assertIn(marker, text)
        self.assertIn(r"\|Q\|", text)

    def test_unit_three_proves_classes_with_explicit_controls(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[2]))
        for marker in (
            "一致连续",
            "振幅",
            r"\frac{b-a}{n}",
            "有限分段连续",
            "总长度",
            "Dirichlet",
            "单点尖峰",
            "无界",
        ):
            self.assertIn(marker, text)

    def test_unit_four_proves_properties_without_antiderivative_calculation(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[3]))
        for marker in (
            "线性",
            "乘积",
            "绝对值",
            "最大值",
            "最小值",
            "一致远离零",
            "保序",
            "区间可加",
        ):
            self.assertIn(marker, text)
        self.assertIn(r"\left|\int_a^b f", text)

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
        self.assertIn("当前发布边界：第 22 章", deps)
        self.assertIn("第 19 章：Riemann 积分与可积性", config)
        self.assertIn("本章学时：7.5 小时（理论 6，应用 1.5）。", course_map)
        self.assertIn("第五部第 22 章，共 98 个学习单元", readme)
        for unit_id, title, _theory, _applied, suffix, _exercises in EXPECTED_UNITS:
            path = f"chapters/chapter-19/{unit_id}-{suffix}.md"
            self.assertEqual(1, config.count(f"{title}: {path}"))
            self.assertEqual(1, course_map.count(f"[{title}]({path})"))


if __name__ == "__main__":
    unittest.main()
