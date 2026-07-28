from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-16"

EXPECTED_UNITS = [
    (
        "u-04-16-01",
        "高阶局部信息怎样形成 Peano 展开？",
        1.25,
        0.50,
        "peano-expansion",
    ),
    (
        "u-04-16-02",
        "Lagrange 余项怎样给出可计算误差界？",
        1.50,
        0.25,
        "lagrange-remainder",
    ),
    (
        "u-04-16-03",
        "Cauchy 余项揭示了怎样的证明结构？",
        1.50,
        0.25,
        "cauchy-remainder",
    ),
    (
        "u-04-16-04",
        "怎样把 Taylor 多项式变成可信的近似工具？",
        0.25,
        1.50,
        "trusted-approximation",
    ),
]

REQUIRED_ANCHORS = {
    "u-04-16-01": (
        "def-u-04-16-01-taylor-polynomial",
        "thm-u-04-16-01-peano",
        "thm-u-04-16-01-uniqueness",
    ),
    "u-04-16-02": (
        "thm-u-04-16-02-lagrange-remainder",
        "cor-u-04-16-02-error-bound",
        "ex-u-04-16-02-order-budget",
    ),
    "u-04-16-03": (
        "thm-u-04-16-03-cauchy-remainder",
        "tbl-u-04-16-03-remainder-comparison",
    ),
    "u-04-16-04": (
        "alg-u-04-16-04-horner",
        "alg-u-04-16-04-centered-difference",
        "ex-u-04-16-04-step-study",
    ),
}

FORBIDDEN_CORE_TERMS = ("凸函数", "Newton 方法", "无穷 Taylor 级数", "解析函数")


def unit_path(unit: tuple[str, str, float, float, str]) -> Path:
    unit_id, _title, _theory, _applied, suffix = unit
    return CHAPTER / f"{unit_id}-{suffix}.md"


def read_unit(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    metadata = yaml.safe_load(text.split("---\n", 2)[1])
    return metadata, text


class ChapterSixteenTests(unittest.TestCase):
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
                theory += metadata["hours"]["theory"]
                applied += metadata["hours"]["applied"]
        self.assertEqual(4.5, theory)
        self.assertEqual(2.5, applied)

    def test_chapter_guide_lists_units_hours_and_boundaries(self) -> None:
        guide_path = CHAPTER / "index.md"
        self.assertTrue(guide_path.is_file(), "missing chapter guide")
        if not guide_path.is_file():
            return
        guide = guide_path.read_text(encoding="utf-8")
        self.assertIn("本章共4个核心单元，7学时（理论4.5，应用2.5）。", guide)
        self.assertIn("第 17 章", guide)
        self.assertIn("有限阶 Taylor 公式不等于无穷 Taylor 级数", guide)
        for unit_id, title, _theory, _applied, suffix in EXPECTED_UNITS:
            self.assertEqual(1, guide.count(f"[{title}]({unit_id}-{suffix}.md)"))

    def test_navigation_course_map_and_readme_use_final_order(self) -> None:
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        course_map = (ROOT / "content" / "course-map.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("本章学时：7 小时（理论 4.5，应用 2.5）。", course_map)
        self.assertIn("第四部第 17 章，共 73 个学习单元", readme)
        navigation_positions = []
        map_positions = []
        for unit_id, title, _theory, _applied, suffix in EXPECTED_UNITS:
            path = f"chapters/chapter-16/{unit_id}-{suffix}.md"
            self.assertEqual(1, config.count(f"{title}: {path}"))
            self.assertEqual(1, course_map.count(f"[{title}]({path})"))
            if path in config:
                navigation_positions.append(config.index(path))
            if path in course_map:
                map_positions.append(course_map.index(path))
        self.assertEqual(sorted(navigation_positions), navigation_positions)
        self.assertEqual(sorted(map_positions), map_positions)

    def test_core_does_not_use_later_topics(self) -> None:
        for unit in EXPECTED_UNITS:
            path = unit_path(unit)
            if not path.is_file():
                continue
            core = path.read_text(encoding="utf-8").split("## 常见误区与后续", 1)[0]
            with self.subTest(unit=unit[0]):
                for term in FORBIDDEN_CORE_TERMS:
                    self.assertNotIn(term, core)

    def test_peano_uses_pointwise_recursive_differentiability(self) -> None:
        path = unit_path(EXPECTED_UNITS[0])
        self.assertTrue(path.is_file(), "missing Peano unit")
        if not path.is_file():
            return
        text = path.read_text(encoding="utf-8")
        for marker in (
            "不要求最高阶导函数在展开点连续",
            r"G'(t)=o\!\left((t-a)^{n-1}\right)",
            r"|\xi-a|\le |x-a|",
            r"c_k=\frac{f^{(k)}(a)}{k!}",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("假设最高阶导函数连续", text)

    def test_lagrange_remainder_has_correct_order_and_interval_bound(self) -> None:
        path = unit_path(EXPECTED_UNITS[1])
        self.assertTrue(path.is_file(), "missing Lagrange remainder unit")
        if not path.is_file():
            return
        text = path.read_text(encoding="utf-8")
        for marker in (
            r"R_n(x)=\frac{f^{(n+1)}(\xi)}{(n+1)!}(x-a)^{n+1}",
            r"|R_n(x)|\le\frac{M}{(n+1)!}|x-a|^{n+1}",
            r"包含连接 \(a\) 与 \(x\) 的闭线段",
            "不要求最高阶导函数连续",
            "最低阶数",
        ):
            self.assertIn(marker, text)

    def test_order_budget_proves_all_lower_orders_fail(self) -> None:
        path = unit_path(EXPECTED_UNITS[1])
        self.assertTrue(path.is_file(), "missing Lagrange remainder unit")
        if not path.is_file():
            return
        text = path.read_text(encoding="utf-8")
        self.assertIn(r"相邻上界的比值为 \(0.5/(n+2)<1\)", text)
        self.assertIn("所有低于四阶的上界更大", text)

    def test_cauchy_remainder_has_correct_cancellation_and_factorial(self) -> None:
        path = unit_path(EXPECTED_UNITS[2])
        self.assertTrue(path.is_file(), "missing Cauchy remainder unit")
        if not path.is_file():
            return
        text = path.read_text(encoding="utf-8")
        for marker in (
            r"\Phi'(t)=-\frac{f^{(n+1)}(t)}{n!}(x-t)^n",
            r"R_n(x)=\frac{f^{(n+1)}(\xi)}{n!}(x-\xi)^n(x-a)",
            r"分母函数的导数恒为 \(-1\)",
            "中间点一般不同",
            "不能无条件互换",
        ):
            self.assertIn(marker, text)

    def test_numerical_error_orders_keep_their_smoothness_conditions(self) -> None:
        path = unit_path(EXPECTED_UNITS[3])
        self.assertTrue(path.is_file(), "missing trusted approximation unit")
        if not path.is_file():
            return
        text = path.read_text(encoding="utf-8")
        for marker in (
            "二阶导数存在并有界",
            r"f'(x)+O(h)",
            "三阶导数存在并有界",
            r"f'(x)+O(h^2)",
            "经验步长不提供误差证书",
            "不能倒过来证明函数可导",
            "evaluate_taylor",
            "forward_difference",
            "centered_difference",
            "DifferenceEstimate",
            "src/mathbook_examples/differentiation.py",
        ):
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
