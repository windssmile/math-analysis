from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content" / "chapters" / "chapter-10"

EXPECTED_UNITS = [
    (
        "u-03-10-01",
        "连续性怎样把极限与函数值接起来？",
        1.75,
        0.25,
        "epsilon-delta-continuity",
    ),
    (
        "u-03-10-02",
        "连续性怎样经过运算和复合传递？",
        1.75,
        0.25,
        "continuous-operations",
    ),
    (
        "u-03-10-04",
        "端点连续与连续延拓怎样统一处理？",
        1.50,
        0.50,
        "one-sided-continuity-extension",
    ),
    (
        "u-03-10-03",
        "函数会以哪些方式失去连续性？",
        1.50,
        0.50,
        "discontinuities-elementary-functions",
    ),
    (
        "u-03-10-05",
        "常见初等函数的连续性从哪里来？",
        1.50,
        0.50,
        "elementary-continuity-bridge",
    ),
]

REQUIRED_ANCHORS = {
    "u-03-10-01": (
        "def-u-03-10-01-continuity",
        "thm-u-03-10-01-sequential-continuity",
    ),
    "u-03-10-02": (
        "thm-u-03-10-02-continuous-operations",
        "thm-u-03-10-02-composition",
    ),
    "u-03-10-04": (
        "def-u-03-10-04-one-sided-continuity",
        "thm-u-03-10-04-continuous-extension",
    ),
    "u-03-10-03": (
        "def-u-03-10-03-discontinuity-types",
        "ex-u-03-10-03-oscillation",
    ),
    "u-03-10-05": (
        "thm-u-03-10-05-algebraic-continuity",
        "thm-u-03-10-05-root-continuity",
    ),
}


def read_unit(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    metadata = yaml.safe_load(text.split("---\n", 2)[1])
    return metadata, text


class ChapterTenTests(unittest.TestCase):
    def test_units_have_the_final_order_metadata_hours_and_anchors(self) -> None:
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
        self.assertEqual(8.0, theory)
        self.assertEqual(2.0, applied)

    def test_navigation_uses_the_final_reading_order(self) -> None:
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        positions = []
        for unit_id, title, _theory, _applied, suffix in EXPECTED_UNITS:
            marker = f"{title}: chapters/chapter-10/{unit_id}-{suffix}.md"
            self.assertEqual(1, config.count(marker))
            positions.append(config.index(marker))
        self.assertEqual(sorted(positions), positions)

    def test_course_map_lists_all_five_units_and_chapter_hours(self) -> None:
        course_map = (ROOT / "content" / "course-map.md").read_text(encoding="utf-8")
        chapter_start = course_map.index("### [第 10 章")
        chapter_end = course_map.index("### [第 11 章")
        chapter = course_map[chapter_start:chapter_end]
        self.assertIn("本章学时：10 小时（理论 8，应用 2）。", chapter)
        positions = []
        for unit_id, title, _theory, _applied, suffix in EXPECTED_UNITS:
            marker = (
                f"[{title}](chapters/chapter-10/{unit_id}-{suffix}.md)"
            )
            self.assertEqual(1, chapter.count(marker))
            positions.append(chapter.index(marker))
        self.assertEqual(sorted(positions), positions)

    def test_proof_core_does_not_depend_on_later_calculus(self) -> None:
        forbidden = (
            "导数",
            "中值定理",
            "Taylor",
            "洛必达",
            "Newton",
            "Riemann 积分",
        )
        for unit_id, _title, _theory, _applied, suffix in EXPECTED_UNITS:
            path = CHAPTER / f"{unit_id}-{suffix}.md"
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            proof_core = text.split("## 常见误区与后续", 1)[0]
            with self.subTest(unit=unit_id):
                for term in forbidden:
                    self.assertNotIn(term, proof_core)


if __name__ == "__main__":
    unittest.main()
