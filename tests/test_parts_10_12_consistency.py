from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
COURSE_MAP = ROOT / "content/course-map.md"
README = ROOT / "README.md"
FINAL_REVIEW = ROOT / "docs/reviews/2026-08-01-parts-10-12-consistency-review.md"

class PartsTenToTwelveConsistencyTests(unittest.TestCase):
    def text(self, path):
        self.assertTrue(path.is_file(), f"missing {path.relative_to(ROOT)}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def test_physical_inventory_and_hours_close(self):
        expected = {10: (range(42, 46), 20, 30.0), 11: (range(46, 51), 25, 38.0), 12: (range(51, 55), 21, 33.0)}
        grand_units = 0; grand_hours = 0.0
        for part, (chapters, units, hours) in expected.items():
            pages = []
            for chapter in chapters:
                pages.extend(sorted((ROOT / f"content/chapters/chapter-{chapter:02d}").glob("u-*.md")))
            actual_hours = 0.0
            for page in pages:
                meta = yaml.safe_load(page.read_text(encoding="utf-8").split("---\n", 2)[1])
                actual_hours += float(meta["hours"]["theory"]) + float(meta["hours"]["applied"])
            self.assertEqual((units, hours), (len(pages), actual_hours), f"part {part}")
            grand_units += len(pages); grand_hours += actual_hours
        self.assertEqual((66, 101.0), (grand_units, grand_hours))

    def test_publication_surfaces_are_current(self):
        joined = self.text(README) + self.text(COURSE_MAP)
        for marker in ("第十二部第 54 章", "255 个学习单元", "438 学时", "第 42–45 章已完整发布", "第 46–50 章已完整发布", "第 51–54 章已完整发布"):
            self.assertIn(marker, joined)
        for stale in ("当前已发布至第十部第 45 章", "第 49–50 章尚未创建", "第 53–54 章仍为规划"):
            self.assertNotIn(stale, joined)

    def test_cross_part_handoffs_name_published_consumers(self):
        p10 = self.text(ROOT / "docs/curriculum/part-10-dependencies.md")
        p11 = self.text(ROOT / "docs/curriculum/part-11-dependencies.md")
        p12 = self.text(ROOT / "docs/curriculum/part-12-dependencies.md")
        for marker in ("u-12-52-05", "u-12-53-03", "u-12-54-03"):
            self.assertIn(marker, p10 + p11 + p12)
        self.assertIn("第十二部已建立", p11)
        self.assertNotIn("第十二部自行建立", p11)

    def test_review_records_math_and_release_audit(self):
        review = self.text(FINAL_REVIEW)
        for marker in ("第十部", "第十一部", "第十二部", "66 个单元", "101 学时", "Dirichlet 核", "Parseval", "Gibbs", "Fejér", "255", "438", "make verify"):
            self.assertIn(marker, review)

if __name__ == "__main__": unittest.main()
