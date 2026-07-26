from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-15"

EXPECTED_UNITS = [
    (
        "u-04-15-01",
        "两个端点的信息怎样迫使中间出现特殊切线？",
        1.75,
        0.25,
        "fermat-rolle-lagrange",
    ),
    (
        "u-04-15-02",
        "导数符号能推出哪些整体性质？",
        1.75,
        0.50,
        "monotonicity-darboux",
    ),
    (
        "u-04-15-03",
        "两个函数的变化率怎样进行严格比较？",
        1.50,
        0.50,
        "cauchy-mean-value",
    ),
    (
        "u-04-15-04",
        "L’Hôpital 法则何时能判定未定式极限？",
        1.50,
        0.75,
        "lhopital-rule",
    ),
]

REQUIRED_ANCHORS = {
    "u-04-15-01": (
        "thm-u-04-15-01-fermat",
        "thm-u-04-15-01-rolle",
        "thm-u-04-15-01-lagrange",
    ),
    "u-04-15-02": (
        "thm-u-04-15-02-monotonicity",
        "thm-u-04-15-02-darboux",
        "ex-u-04-15-02-discontinuous-derivative",
    ),
    "u-04-15-03": (
        "thm-u-04-15-03-cauchy-cross",
        "cor-u-04-15-03-cauchy-ratio",
    ),
    "u-04-15-04": (
        "thm-u-04-15-04-lhopital-zero-zero",
        "thm-u-04-15-04-lhopital-infinity-infinity",
        "ex-u-04-15-04-power-forms",
    ),
}

FORBIDDEN_CORE_TERMS = (
    "Taylor",
    "Newton",
    "Riemann 积分",
    "无穷级数",
    "凸函数",
)


def unit_path(unit: tuple[str, str, float, float, str]) -> Path:
    unit_id, _title, _theory, _applied, suffix = unit
    return CHAPTER / f"{unit_id}-{suffix}.md"


def read_unit(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    metadata = yaml.safe_load(text.split("---\n", 2)[1])
    return metadata, text


class ChapterFifteenTests(unittest.TestCase):
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
        self.assertEqual(6.5, theory)
        self.assertEqual(2.0, applied)

    def test_chapter_guide_lists_units_hours_and_boundaries(self) -> None:
        guide_path = CHAPTER / "index.md"
        self.assertTrue(guide_path.is_file(), "missing chapter guide")
        if not guide_path.is_file():
            return
        guide = guide_path.read_text(encoding="utf-8")
        self.assertIn("本章共4个核心单元，8.5学时（理论6.5，应用2.0）。", guide)
        self.assertIn("第 16–17 章", guide)
        for unit_id, title, _theory, _applied, suffix in EXPECTED_UNITS:
            self.assertEqual(1, guide.count(f"[{title}]({unit_id}-{suffix}.md)"))

    def test_navigation_course_map_and_part_design_use_final_order(self) -> None:
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
        self.assertIn("本章学时：8.5 小时（理论 6.5，应用 2.0）。", course_map)
        self.assertIn("第四部第 16 章，共 68 个学习单元", readme)
        self.assertIn("| 第 15 章 | 6.5 | 2.0 | 8.5 |", part_design)
        self.assertIn("| **第四部** | **25** | **10.5** | **35.5** |", part_design)
        navigation_positions = []
        map_positions = []
        for unit_id, title, _theory, _applied, suffix in EXPECTED_UNITS:
            path = f"chapters/chapter-15/{unit_id}-{suffix}.md"
            self.assertEqual(1, config.count(f"{title}: {path}"))
            self.assertEqual(1, course_map.count(f"[{title}]({path})"))
            if path in config:
                navigation_positions.append(config.index(path))
            if path in course_map:
                map_positions.append(course_map.index(path))
        self.assertEqual(sorted(navigation_positions), navigation_positions)
        self.assertEqual(sorted(map_positions), map_positions)

    def test_core_proofs_do_not_use_later_calculus(self) -> None:
        for unit in EXPECTED_UNITS:
            path = unit_path(unit)
            if not path.is_file():
                continue
            core = path.read_text(encoding="utf-8").split("## 常见误区与后续", 1)[0]
            with self.subTest(unit=unit[0]):
                for term in FORBIDDEN_CORE_TERMS:
                    self.assertNotIn(term, core)

    def test_darboux_does_not_assume_derivative_continuity(self) -> None:
        path = unit_path(EXPECTED_UNITS[1])
        self.assertTrue(path.is_file(), "missing monotonicity-darboux unit")
        if not path.is_file():
            return
        text = path.read_text(encoding="utf-8")
        self.assertIn(r"\(a,b\) 都是导数定义区间的内部点", text)
        self.assertIn(r"证明没有假设 \(f'\) 连续", text)
        self.assertNotIn("因为导函数连续", text)

    def test_cauchy_cross_product_precedes_ratio_form(self) -> None:
        path = unit_path(EXPECTED_UNITS[2])
        self.assertTrue(path.is_file(), "missing Cauchy unit")
        if not path.is_file():
            return
        text = path.read_text(encoding="utf-8")
        cross = text.index("{#thm-u-04-15-03-cauchy-cross}")
        ratio = text.index("{#cor-u-04-15-03-cauchy-ratio}")
        self.assertLess(cross, ratio)
        self.assertIn(r"g'(x)\ne0\qquad(x\in(a,b))", text)
        self.assertIn("不能对定理给出的未知点追加条件", text)

    def test_lhopital_separates_forms_and_rechecks_conditions(self) -> None:
        path = unit_path(EXPECTED_UNITS[3])
        self.assertTrue(path.is_file(), "missing L'Hopital unit")
        if not path.is_file():
            return
        text = path.read_text(encoding="utf-8")
        self.assertLess(
            text.index("{#thm-u-04-15-04-lhopital-zero-zero}"),
            text.index("{#thm-u-04-15-04-lhopital-infinity-infinity}"),
        )
        for marker in (
            r"0\cdot\infty",
            r"\infty-\infty",
            r"1^\infty",
            r"0^0",
            r"\infty^0",
            "每一轮都重新核验",
            "去心邻域内为正",
        ):
            self.assertIn(marker, text)

    def test_lhopital_includes_one_sided_infinite_and_failure_cases(self) -> None:
        path = unit_path(EXPECTED_UNITS[3])
        self.assertTrue(path.is_file(), "missing L'Hopital unit")
        if not path.is_file():
            return
        text = path.read_text(encoding="utf-8")
        for marker in (
            r"x\to a^+",
            r"x\to a^-",
            r"x\to+\infty",
            r"x\to-\infty",
            "导数之比没有极限",
            "非未定式",
        ):
            self.assertIn(marker, text)

    def test_infinity_over_infinity_extended_limit_uses_target_threshold(self) -> None:
        path = unit_path(EXPECTED_UNITS[3])
        self.assertTrue(path.is_file(), "missing L'Hopital unit")
        if not path.is_file():
            return
        text = path.read_text(encoding="utf-8")
        self.assertIn(r"先令增量比大于 \(3K\)", text)
        self.assertIn(r"原商最终大于 \(K\)", text)


if __name__ == "__main__":
    unittest.main()
