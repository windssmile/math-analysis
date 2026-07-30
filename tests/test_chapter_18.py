from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-18"
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-05-dependencies.md"

EXPECTED_UNITS = [
    ("u-05-18-01", "导数能否反向恢复原函数？", 1.25, 0.25, "antiderivatives"),
    ("u-05-18-02", "复合函数的导数怎样反向产生换元法？", 1.00, 0.50, "substitution"),
    ("u-05-18-03", "乘积法则怎样反向产生分部积分法？", 1.00, 0.50, "integration-by-parts"),
    ("u-05-18-04", "有理函数怎样通过代数分解获得原函数？", 1.00, 0.50, "rational-functions"),
    ("u-05-18-05", "怎样选择积分方法并用求导可靠回验？", 0.25, 1.75, "method-selection"),
]

REQUIRED_ANCHORS = {
    "u-05-18-01": (
        "def-u-05-18-01-antiderivative",
        "thm-u-05-18-01-constant-difference",
        "ex-u-05-18-01-darboux-obstruction",
    ),
    "u-05-18-02": (
        "thm-u-05-18-02-substitution",
        "tbl-u-05-18-02-domain-checks",
    ),
    "u-05-18-03": (
        "thm-u-05-18-03-integration-by-parts",
        "tbl-u-05-18-03-route-selection",
    ),
    "u-05-18-04": (
        "thm-u-05-18-04-partial-fractions",
        "tbl-u-05-18-04-factor-forms",
    ),
    "u-05-18-05": (
        "alg-u-05-18-05-method-selection",
        "tbl-u-05-18-05-verification",
    ),
}

FORBIDDEN_CORE_TERMS = (
    "Riemann 和",
    "Darboux 和",
    "微积分基本定理",
    "Newton–Leibniz",
    "积分上限函数",
    "Lebesgue",
)


def unit_path(unit: tuple[str, str, float, float, str]) -> Path:
    unit_id, _title, _theory, _applied, suffix = unit
    return CHAPTER / f"{unit_id}-{suffix}.md"


def read_unit(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    metadata = yaml.safe_load(text.split("---\n", 2)[1])
    return metadata, text


class ChapterEighteenTests(unittest.TestCase):
    def required_text(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"missing {path}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def test_units_have_final_metadata_hours_and_anchors(self) -> None:
        theory = 0.0
        applied = 0.0
        for unit in EXPECTED_UNITS:
            unit_id, title, theory_hours, applied_hours, _suffix = unit
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
                theory += float(metadata["hours"]["theory"])
                applied += float(metadata["hours"]["applied"])
        self.assertEqual(4.5, theory)
        self.assertEqual(3.5, applied)

    def test_chapter_guide_lists_units_hours_and_boundaries(self) -> None:
        guide = self.required_text(CHAPTER / "index.md")
        self.assertIn("本章共5个核心单元，8学时（理论4.5，应用3.5）。", guide)
        self.assertIn("第 14.5 单元", guide)
        self.assertIn("第 17 章", guide)
        self.assertIn("第 19 章", guide)
        self.assertIn("不使用 Riemann 积分或微积分基本定理", guide)
        for unit_id, title, _theory, _applied, suffix in EXPECTED_UNITS:
            self.assertEqual(1, guide.count(f"[{title}]({unit_id}-{suffix}.md)"))

    def test_core_does_not_use_later_integral_theory(self) -> None:
        for unit in EXPECTED_UNITS:
            path = unit_path(unit)
            if not path.is_file():
                continue
            core = path.read_text(encoding="utf-8").split("## 常见误区与后续", 1)[0]
            with self.subTest(unit=unit[0]):
                for term in FORBIDDEN_CORE_TERMS:
                    self.assertNotIn(term, core)

    def test_antiderivative_unit_keeps_interval_and_existence_boundaries(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[0]))
        for marker in (
            "区间",
            "相差一个常数",
            "互不相连",
            "Darboux",
            "必要条件",
            "不是充分条件",
        ):
            self.assertIn(marker, text)

    def test_substitution_unit_requires_chain_factor_and_domain_checks(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[1]))
        for marker in (
            r"F'(u)=f(u)",
            r"g(I)\subseteq J",
            r"f(g(x))g'(x)",
            "内层导数",
            "定义域",
            "求导回验",
        ):
            self.assertIn(marker, text)

    def test_parts_unit_is_identity_not_simplification_promise(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[2]))
        for marker in (
            "乘积法则",
            "恒等式",
            "不保证",
            r"\int xe^x",
            r"\int \log x",
            r"\int e^x\cos x",
        ):
            self.assertIn(marker, text)

    def test_rational_unit_reduces_before_decomposing(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[3]))
        for marker in (
            "多项式除法",
            "真分式",
            "重线性因子",
            "不可约二次因子",
            "待定系数",
            "求导回验",
        ):
            self.assertIn(marker, text)

    def test_method_selection_unit_has_mixed_training_and_honest_boundary(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[4]))
        self.assertGreaterEqual(text.count("{#pr-u-05-18-05-"), 12)
        self.assertGreaterEqual(text.count('??? note "答案"'), 14)
        for marker in (
            "识别结构",
            "选择方法",
            "求导回验",
            "失败路线",
            "没有初等原函数",
            r"e^{-x^2}",
        ):
            self.assertIn(marker, text)

    def test_dependency_map_covers_all_twenty_four_units(self) -> None:
        text = self.required_text(DEPENDENCIES)
        for chapter, count in ((18, 5), (19, 4), (20, 5), (21, 5), (22, 5)):
            for unit in range(1, count + 1):
                self.assertIn(f"u-05-{chapter:02d}-{unit:02d}", text)
        self.assertIn("当前发布边界：第 22 章", text)

    def test_navigation_course_map_and_release_scope(self) -> None:
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        course_map = (ROOT / "content" / "course-map.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("第五部：积分、累积与数值求积", config)
        self.assertIn("本章学时：8 小时（理论 4.5，应用 3.5）。", course_map)
        self.assertIn("第六部第 25 章，共 113 个学习单元", readme)
        navigation_positions = []
        map_positions = []
        for unit_id, title, _theory, _applied, suffix in EXPECTED_UNITS:
            path = f"chapters/chapter-18/{unit_id}-{suffix}.md"
            self.assertEqual(1, config.count(f"{title}: {path}"))
            self.assertEqual(1, course_map.count(f"[{title}]({path})"))
            navigation_positions.append(config.index(path))
            map_positions.append(course_map.index(path))
        self.assertEqual(sorted(navigation_positions), navigation_positions)
        self.assertEqual(sorted(map_positions), map_positions)


if __name__ == "__main__":
    unittest.main()
