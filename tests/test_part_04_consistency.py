from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "content" / "chapters"
PART_DESIGN = ROOT / "docs" / "superpowers" / "specs" / "2026-07-25-part-04-differentiation-design.md"
MASTER_DESIGN = ROOT / "docs" / "superpowers" / "specs" / "2026-07-18-mathematical-analysis-textbook-design.md"
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-04-dependencies.md"
REVIEW = ROOT / "docs" / "reviews" / "2026-07-27-part-04-consistency-review.md"


def part_four_units() -> list[Path]:
    return [
        path
        for chapter in range(13, 18)
        for path in sorted((CHAPTERS / f"chapter-{chapter:02d}").glob("u-*.md"))
    ]


def metadata(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---\n", 2)[1])


class PartFourConsistencyTests(unittest.TestCase):
    def test_twenty_one_unique_v2_units_close_final_hours(self) -> None:
        units = part_four_units()
        self.assertEqual(21, len(units))
        records = [metadata(path) for path in units]
        unit_ids = [str(record["unit_id"]) for record in records]
        self.assertEqual(21, len(set(unit_ids)))
        self.assertTrue(all(record["content_standard"] == 2 for record in records))
        self.assertEqual(
            26.0,
            sum(float(record["hours"]["theory"]) for record in records),
        )
        self.assertEqual(
            12.5,
            sum(float(record["hours"]["applied"]) for record in records),
        )

    def test_designs_use_reconciled_current_totals(self) -> None:
        part = PART_DESIGN.read_text(encoding="utf-8")
        master = MASTER_DESIGN.read_text(encoding="utf-8")
        self.assertIn("| **第四部** | **26** | **12.5** | **38.5** |", part)
        self.assertNotIn("第四部学时 \\(24+10=34\\)", part)
        self.assertNotIn("学时闭合为理论 24、应用 10", part)
        self.assertIn("| IV | 微分与局部线性化 | 26 | 12.5 | 38.5 |", master)
        self.assertIn("| V | 积分、累积与数值求积 | 26 | 13.5 | 39.5 |", master)
        self.assertIn("| **当前总计** |  | **292.75** | **101.25** | **394** |", master)
        self.assertIn("由 392 增至 394", master)

    def test_dependency_map_covers_interfaces_and_every_unit(self) -> None:
        text = DEPENDENCIES.read_text(encoding="utf-8")
        for chapter in range(12, 19):
            self.assertIn(f"第 {chapter} 章", text)
        for path in part_four_units():
            self.assertIn(str(metadata(path)["unit_id"]), text)

    def test_algorithm_sources_are_named_once_and_not_copied(self) -> None:
        part = PART_DESIGN.read_text(encoding="utf-8")
        dependency = DEPENDENCIES.read_text(encoding="utf-8")
        self.assertEqual(1, part.count("src/mathbook_examples/differentiation.py"))
        self.assertEqual(1, part.count("src/mathbook_examples/newton.py"))
        self.assertIn("数值实验只用于提出猜想", dependency)
        self.assertTrue((ROOT / "src" / "mathbook_examples" / "differentiation.py").is_file())
        self.assertTrue((ROOT / "src" / "mathbook_examples" / "newton.py").is_file())

    def test_review_report_records_all_five_chapter_reviews(self) -> None:
        self.assertTrue(REVIEW.is_file(), f"missing review report: {REVIEW}")
        text = REVIEW.read_text(encoding="utf-8") if REVIEW.is_file() else ""
        for chapter in range(13, 18):
            self.assertIn(f"## 第 {chapter} 章审查", text)
        self.assertIn("## 第 12 与第 18 章接口", text)
        self.assertIn("## 20 单元审查矩阵", text)
        self.assertIn("## 问题与修复", text)
        self.assertIn("## 已知限制", text)
        self.assertIn("## 最终验证", text)

    def test_release_surfaces_agree_on_chapter_seventeen(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        course_map = (ROOT / "content" / "course-map.md").read_text(encoding="utf-8")
        navigation = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        site_checker = (ROOT / "scripts" / "check_site.py").read_text(encoding="utf-8")
        self.assertIn("第六部第 24 章，共 108 个学习单元", readme)
        self.assertIn("第 24 章，共 108 个学习单元", course_map)
        self.assertIn("第 17 章：凸性、优化、函数形态与 Newton 方法", navigation)
        self.assertIn(
            "chapters/chapter-17/u-04-17-04-safeguarded-newton/index.html",
            site_checker,
        )


if __name__ == "__main__":
    unittest.main()
