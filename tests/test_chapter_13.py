from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-13"

EXPECTED_UNITS = [
    (
        "u-04-13-01",
        "平均变化率怎样逼近瞬时变化率？",
        1.25,
        0.50,
        "average-instantaneous-rate",
    ),
    (
        "u-04-13-02",
        "差商极限何时存在，何时失败？",
        1.50,
        0.25,
        "derivative-existence-failure",
    ),
    (
        "u-04-13-03",
        "可导为什么等价于一阶局部线性化？",
        1.50,
        0.25,
        "local-linearization",
    ),
    (
        "u-04-13-04",
        "局部线性模型怎样预测增量、误差与敏感性？",
        1.25,
        0.50,
        "sensitivity-linear-model",
    ),
]

REQUIRED_ANCHORS = {
    "u-04-13-01": (
        "def-u-04-13-01-derivative",
        "thm-u-04-13-01-derivative-unique",
    ),
    "u-04-13-02": (
        "thm-u-04-13-02-one-sided-criterion",
        "ex-u-04-13-02-absolute-value",
    ),
    "u-04-13-03": (
        "thm-u-04-13-03-linearization-equivalence",
        "thm-u-04-13-03-differentiable-continuous",
    ),
    "u-04-13-04": (
        "def-u-04-13-04-relative-sensitivity",
        "thm-u-04-13-04-relative-error",
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


def read_unit(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    metadata = yaml.safe_load(text.split("---\n", 2)[1])
    return metadata, text


class ChapterThirteenTests(unittest.TestCase):
    def test_units_have_final_metadata_hours_and_anchors(self) -> None:
        theory = 0.0
        applied = 0.0
        for unit_id, title, theory_hours, applied_hours, suffix in EXPECTED_UNITS:
            path = CHAPTER / f"{unit_id}-{suffix}.md"
            with self.subTest(unit=unit_id):
                self.assertTrue(path.is_file())
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
        self.assertEqual(5.5, theory)
        self.assertEqual(1.5, applied)

    def test_navigation_and_course_map_use_final_order(self) -> None:
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        course_map = (ROOT / "content" / "course-map.md").read_text(encoding="utf-8")
        self.assertIn("本章学时：7 小时（理论 5.5，应用 1.5）。", course_map)
        navigation_positions = []
        map_positions = []
        for unit_id, title, _theory, _applied, suffix in EXPECTED_UNITS:
            path = f"chapters/chapter-13/{unit_id}-{suffix}.md"
            self.assertEqual(1, config.count(f"{title}: {path}"))
            self.assertEqual(1, course_map.count(f"[{title}]({path})"))
            navigation_positions.append(config.index(path))
            map_positions.append(course_map.index(path))
        self.assertEqual(sorted(navigation_positions), navigation_positions)
        self.assertEqual(sorted(map_positions), map_positions)

    def test_chapter_guide_lists_units_and_hours(self) -> None:
        guide_path = CHAPTER / "index.md"
        self.assertTrue(guide_path.is_file())
        guide = guide_path.read_text(encoding="utf-8")
        self.assertIn("本章共4个核心单元，7学时（理论5.5，应用1.5）。", guide)
        for unit_id, title, _theory, _applied, suffix in EXPECTED_UNITS:
            path = f"{unit_id}-{suffix}.md"
            self.assertEqual(1, guide.count(f"[{title}]({path})"))

    def test_core_does_not_use_later_calculus(self) -> None:
        for unit_id, _title, _theory, _applied, suffix in EXPECTED_UNITS:
            path = CHAPTER / f"{unit_id}-{suffix}.md"
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            core = text.split("## 常见误区与后续", 1)[0]
            with self.subTest(unit=unit_id):
                for term in FORBIDDEN_CORE_TERMS:
                    self.assertNotIn(term, core)


if __name__ == "__main__":
    unittest.main()
