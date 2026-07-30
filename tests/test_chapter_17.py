from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-17"

EXPECTED_UNITS = [
    (
        "u-04-17-01",
        "导数怎样还原函数的增减、极值与弯曲形态？",
        1.50,
        0.50,
        "function-shape",
    ),
    (
        "u-04-17-02",
        "凸性为何能把局部极小升级为整体极小？",
        1.50,
        0.50,
        "convexity-optimization",
    ),
    (
        "u-04-17-03",
        "Newton 迭代为什么可能快速收敛，也可能失败？",
        1.25,
        0.75,
        "newton-convergence-failure",
    ),
    (
        "u-04-17-04",
        "怎样实现具有保护机制和停止证书的 Newton 算法？",
        0.25,
        1.75,
        "safeguarded-newton",
    ),
]

REQUIRED_ANCHORS = {
    "u-04-17-01": (
        "thm-u-04-17-01-first-derivative-test",
        "thm-u-04-17-01-second-derivative-test",
        "def-u-04-17-01-inflection",
    ),
    "u-04-17-02": (
        "def-u-04-17-02-convex",
        "thm-u-04-17-02-supporting-line",
        "thm-u-04-17-02-derivative-monotone",
        "thm-u-04-17-02-strict-minimizer",
    ),
    "u-04-17-03": (
        "thm-u-04-17-03-interval-newton",
        "thm-u-04-17-03-quadratic-convergence",
        "thm-u-04-17-03-multiple-root",
        "ex-u-04-17-03-two-cycle",
    ),
    "u-04-17-04": (
        "alg-u-04-17-04-safeguarded-newton",
        "thm-u-04-17-04-bracket-contraction",
        "def-u-04-17-04-verifiable-certificate",
        "tbl-u-04-17-04-certificate-comparison",
    ),
}

FORBIDDEN_CORE_TERMS = (
    "Riemann 积分",
    "积分型 Taylor 余项",
    "幂级数展开",
    "多元 Newton",
    "Fréchet",
)


def unit_path(unit: tuple[str, str, float, float, str]) -> Path:
    unit_id, _title, _theory, _applied, suffix = unit
    return CHAPTER / f"{unit_id}-{suffix}.md"


def read_unit(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    metadata = yaml.safe_load(text.split("---\n", 2)[1])
    return metadata, text


class ChapterSeventeenTests(unittest.TestCase):
    def required_text(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"missing {path.name}")
        return path.read_text(encoding="utf-8")

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
        self.assertIn("本章共4个核心单元，8学时（理论4.5，应用3.5）。", guide)
        self.assertIn("第 12 章", guide)
        self.assertIn("第 18 章", guide)
        self.assertIn("不引入积分型余项、无穷级数或多元方法", guide)
        for unit_id, title, _theory, _applied, suffix in EXPECTED_UNITS:
            self.assertEqual(1, guide.count(f"[{title}]({unit_id}-{suffix}.md)"))

    def test_shape_unit_keeps_candidate_and_inflection_boundaries(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[0]))
        for marker in (
            "第 15.2 单元已经证明",
            "端点、驻点和不可导点",
            "局部极值不自动是整体极值",
            r"f''(x_0)=0",
            "凹凸性发生改变",
            r"x^4",
        ):
            self.assertIn(marker, text)

    def test_convexity_unit_separates_existence_and_uniqueness(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[1]))
        for marker in (
            "弦不等式",
            "支撑线不等式",
            "当且仅当",
            "至多有一个整体极小点",
            "不保证极小点存在",
            r"e^x-x",
        ):
            self.assertIn(marker, text)

    def test_newton_unit_keeps_local_and_global_assumptions(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[2]))
        for marker in (
            r"f(a)f(b)<0",
            r"f(x_0)f''(x_0)>0",
            r"|f'(x)|\ge \mu>0",
            r"|e_{n+1}|\le \frac{M}{2\mu}|e_n|^2",
            r"1-\frac1m",
            r"x^3-x-1",
            r"x^3-2x+2",
            r"(x-1)^2",
            "局部结论",
        ):
            self.assertIn(marker, text)

    def test_algorithm_unit_distinguishes_stop_signal_and_certificate(self) -> None:
        text = self.required_text(unit_path(EXPECTED_UNITS[3]))
        for marker in (
            "可验证误差证书",
            "连续性由调用者证明",
            "程序能够检查",
            r"[a+w/4,b-w/4]",
            r"\left(\frac34\right)^n",
            "converged",
            "certified",
            "step_types",
            "src/mathbook_examples/newton.py",
            "safeguarded_newton",
        ):
            self.assertIn(marker, text)

    def test_publication_uses_final_order_hours_and_release_scope(self) -> None:
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        course_map = (ROOT / "content" / "course-map.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        part_design = (
            ROOT
            / "docs"
            / "superpowers"
            / "specs"
            / "2026-07-25-part-04-differentiation-design.md"
        ).read_text(encoding="utf-8")
        master_design = (
            ROOT
            / "docs"
            / "superpowers"
            / "specs"
            / "2026-07-18-mathematical-analysis-textbook-design.md"
        ).read_text(encoding="utf-8")

        self.assertIn("第五部第 22 章，共 98 个学习单元", readme)
        self.assertIn("本章学时：8 小时（理论 4.5，应用 3.5）。", course_map)
        self.assertIn("| 第 17 章 | 4.5 | 3.5 | 8 |", part_design)
        self.assertIn("| **第四部** | **26** | **12.5** | **38.5** |", part_design)
        self.assertNotIn(r"第四部学时 \(24+10=34\)", part_design)
        self.assertNotIn("学时闭合为理论 24、应用 10", part_design)
        self.assertIn(
            "| IV | 微分与局部线性化 | 26 | 12.5 | 38.5 |",
            master_design,
        )
        self.assertIn(
            "| **当前总计** |  | **292.75** | **101.25** | **394** |",
            master_design,
        )
        self.assertIn("由 392 增至 394", master_design)

        navigation_positions = []
        map_positions = []
        for unit_id, title, _theory, _applied, suffix in EXPECTED_UNITS:
            path = f"chapters/chapter-17/{unit_id}-{suffix}.md"
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
            core = path.read_text(encoding="utf-8").split(
                "## 常见误区与后续", 1
            )[0]
            with self.subTest(unit=unit[0]):
                for term in FORBIDDEN_CORE_TERMS:
                    self.assertNotIn(term, core)


if __name__ == "__main__":
    unittest.main()
