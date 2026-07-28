from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-14"

EXPECTED_UNITS = [
    (
        "u-04-14-01",
        "局部线性模型怎样通过和、积、商传递？",
        1.25,
        0.25,
        "algebraic-derivative-rules",
    ),
    (
        "u-04-14-02",
        "复合函数的局部误差怎样层层传递？",
        1.25,
        0.25,
        "chain-rule",
    ),
    (
        "u-04-14-03",
        "反函数的变化率为何是原导数的倒数？",
        1.00,
        0.50,
        "inverse-elementary-derivatives",
    ),
    (
        "u-04-14-04",
        "隐式关系与高阶导数怎样记录复杂变化？",
        1.00,
        0.50,
        "implicit-higher-derivatives",
    ),
    (
        "u-04-14-05",
        "怎样为原函数计算准备可靠的求导能力？",
        0.50,
        1.50,
        "derivative-fluency-for-antiderivatives",
    ),
]

REQUIRED_ANCHORS = {
    "u-04-14-01": (
        "thm-u-04-14-01-sum-product",
        "thm-u-04-14-01-reciprocal-quotient",
    ),
    "u-04-14-02": (
        "thm-u-04-14-02-chain-rule",
        "ex-u-04-14-02-zero-inner-increment",
    ),
    "u-04-14-03": (
        "thm-u-04-14-03-inverse-derivative",
        "thm-u-04-14-03-elementary-derivatives",
    ),
    "u-04-14-04": (
        "def-u-04-14-04-higher-derivatives",
        "thm-u-04-14-04-implicit-conditional",
    ),
    "u-04-14-05": (
        "tbl-u-04-14-05-structure-signals",
        "ex-u-04-14-05-nested-chain",
        "ex-u-04-14-05-error-diagnosis",
    ),
}

FORBIDDEN_CORE_TERMS = (
    "中值定理",
    "L’Hôpital",
    "Taylor",
    "Newton",
    "Riemann 积分",
    "无穷级数",
)


def unit_path(unit: tuple[str, str, float, float, str]) -> Path:
    unit_id, _title, _theory, _applied, suffix = unit
    return CHAPTER / f"{unit_id}-{suffix}.md"


def read_unit(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    metadata = yaml.safe_load(text.split("---\n", 2)[1])
    return metadata, text


class ChapterFourteenTests(unittest.TestCase):
    def test_units_have_final_metadata_hours_and_anchors(self) -> None:
        theory = 0.0
        applied = 0.0
        for unit in EXPECTED_UNITS:
            unit_id, title, theory_hours, applied_hours, _suffix = unit
            path = unit_path(unit)
            with self.subTest(unit=unit_id):
                self.assertTrue(path.is_file(), f"missing {path.name}")
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
        self.assertEqual(5.0, theory)
        self.assertEqual(3.0, applied)

    def test_chapter_guide_lists_units_hours_and_boundaries(self) -> None:
        guide_path = CHAPTER / "index.md"
        self.assertTrue(guide_path.is_file(), "missing chapter guide")
        guide = guide_path.read_text(encoding="utf-8")
        self.assertIn("本章共5个核心单元，8学时（理论5，应用3）。", guide)
        self.assertIn("第 15–17 章", guide)
        self.assertIn("第 18 章", guide)
        for unit in EXPECTED_UNITS:
            _unit_id, title, _theory, _applied, suffix = unit
            self.assertEqual(1, guide.count(f"[{title}]({unit[0]}-{suffix}.md)"))

    def test_navigation_and_course_map_use_final_order(self) -> None:
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        course_map = (ROOT / "content" / "course-map.md").read_text(encoding="utf-8")
        self.assertIn("本章学时：8 小时（理论 5，应用 3）。", course_map)
        navigation_positions = []
        map_positions = []
        for unit in EXPECTED_UNITS:
            unit_id, title, _theory, _applied, suffix = unit
            path = f"chapters/chapter-14/{unit_id}-{suffix}.md"
            self.assertEqual(1, config.count(f"{title}: {path}"))
            self.assertEqual(1, course_map.count(f"[{title}]({path})"))
            navigation_positions.append(config.index(path))
            map_positions.append(course_map.index(path))
        self.assertEqual(sorted(navigation_positions), navigation_positions)
        self.assertEqual(sorted(map_positions), map_positions)

    def test_core_proofs_do_not_use_later_calculus(self) -> None:
        for unit in EXPECTED_UNITS:
            path = unit_path(unit)
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            core = text.split("## 常见误区与后续", 1)[0]
            with self.subTest(unit=unit[0]):
                for term in FORBIDDEN_CORE_TERMS:
                    self.assertNotIn(term, core)

    def test_chain_rule_handles_zero_inner_increment(self) -> None:
        path = unit_path(EXPECTED_UNITS[1])
        self.assertTrue(path.is_file(), "missing chain-rule unit")
        text = path.read_text(encoding="utf-8")
        self.assertIn(r"即使 \(g(a+h)=g(a)\)", text)

    def test_inverse_theorem_states_its_limit_contract(self) -> None:
        path = unit_path(EXPECTED_UNITS[2])
        self.assertTrue(path.is_file(), "missing inverse-function unit")
        text = path.read_text(encoding="utf-8")
        for marker in (r"反函数 \(g=f^{-1}\) 在 \(b\) 连续", r"f'(a)\ne0", r"y\to b"):
            self.assertIn(marker, text)

    def test_interval_inverse_continuity_is_proved_locally(self) -> None:
        path = unit_path(EXPECTED_UNITS[2])
        self.assertTrue(path.is_file(), "missing inverse-function unit")
        text = path.read_text(encoding="utf-8")
        self.assertIn("### 引理：区间反函数连续", text)
        self.assertIn(r"f(a-\varepsilon)<y<f(a+\varepsilon)", text)
        self.assertNotIn("可以由第 10 章的连续性与区间", text)

    def test_zero_original_derivative_rules_out_a_finite_inverse_derivative(self) -> None:
        path = unit_path(EXPECTED_UNITS[2])
        self.assertTrue(path.is_file(), "missing inverse-function unit")
        text = path.read_text(encoding="utf-8")
        self.assertIn(
            r"反函数 \(g\) 不可能在 \(b\) 处有有限导数",
            text,
        )
        self.assertNotIn("原导数为零时反函数一定不可导", text)

    def test_inverse_theorem_applications_verify_inverse_continuity(self) -> None:
        path = unit_path(EXPECTED_UNITS[2])
        self.assertTrue(path.is_file(), "missing inverse-function unit")
        text = path.read_text(encoding="utf-8")
        self.assertIn(
            r"\(G(x)=x^{1/q}\) 在 \((0,\infty)\) 上连续",
            text,
        )
        self.assertIn(
            r"\(\ln x\) 在 \((0,\infty)\) 上连续",
            text,
        )

    def test_trigonometric_basic_limit_does_not_assume_cosine_continuity(self) -> None:
        path = unit_path(EXPECTED_UNITS[2])
        self.assertTrue(path.is_file(), "missing inverse-function unit")
        text = path.read_text(encoding="utf-8")
        self.assertIn(r"0\le1-\cos h", text)
        self.assertIn(r"\le\frac{h^2}{2}", text)
        self.assertNotIn("余弦连续性给出", text)

    def test_implicit_differentiation_is_conditional(self) -> None:
        path = unit_path(EXPECTED_UNITS[3])
        self.assertTrue(path.is_file(), "missing implicit-differentiation unit")
        text = path.read_text(encoding="utf-8")
        self.assertIn(r"先已知 \(y\) 在该点可导", text)
        self.assertNotIn("隐函数定理保证", text)

    def test_second_derivative_counterexample_orders_one_sided_limits(self) -> None:
        path = unit_path(EXPECTED_UNITS[3])
        self.assertTrue(path.is_file(), "missing higher-derivative unit")
        text = path.read_text(encoding="utf-8")
        self.assertIn(
            r"左极限为 \(-2\)，右极限为 \(2\)",
            text,
        )

    def test_derivative_fluency_unit_prepares_integration_without_teaching_it(self) -> None:
        path = unit_path(EXPECTED_UNITS[4])
        self.assertTrue(path.is_file(), "missing derivative-fluency unit")
        if not path.is_file():
            return
        text = path.read_text(encoding="utf-8")
        self.assertGreaterEqual(text.count("{#pr-u-04-14-05-"), 12)
        self.assertGreaterEqual(text.count('??? note "答案"'), 14)
        for marker in (
            "结构识别",
            "错误诊断",
            "定义域",
            "第 18 章",
            "求导回验",
        ):
            self.assertIn(marker, text)
        core = text.split("## 常见误区与后续", 1)[0]
        for forbidden in ("换元积分公式", "分部积分公式", "Riemann 积分", "微积分基本定理"):
            self.assertNotIn(forbidden, core)


if __name__ == "__main__":
    unittest.main()
