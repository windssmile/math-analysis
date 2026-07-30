from pathlib import Path
import re
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = [ROOT / "content" / "chapters" / f"chapter-{n}" for n in range(23, 28)]
FINAL_REVIEW = ROOT / "docs" / "reviews" / "2026-07-30-part-06-consistency-review.md"


class PartSixConsistencyTests(unittest.TestCase):
    def unit_pages(self):
        return [page for chapter in CHAPTERS for page in sorted(chapter.glob("u-*.md"))]

    def test_twenty_four_unique_units_close_hours_and_training(self):
        pages = self.unit_pages()
        self.assertEqual([5, 5, 5, 5, 4], [len(list(c.glob("u-*.md"))) for c in CHAPTERS])
        ids = []
        theory = applied = 0.0
        exercises = answers = 0
        for page in pages:
            text = page.read_text(encoding="utf-8")
            metadata = yaml.safe_load(text.split("---\n", 2)[1])
            ids.append(metadata["unit_id"])
            theory += metadata["hours"]["theory"]
            applied += metadata["hours"]["applied"]
            exercises += text.count("{#pr-")
            answers += text.count('??? note "答案"')
            self.assertEqual(2, metadata["content_standard"])
            self.assertIn(f'{{#{metadata["unit_id"]}}}', text)
        self.assertEqual(24, len(ids))
        self.assertEqual(24, len(set(ids)))
        self.assertEqual((30.5, 11.5, 42.0), (theory, applied, theory + applied))
        self.assertEqual((218, 271), (exercises, answers))

    def test_chapter_order_and_navigation_match_design(self):
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        expected = [
            "第 23 章：数项级数的收敛与正项判别",
            "第 24 章：一般项级数、重排与乘积",
            "第 25 章：函数列、函数项级数与一致收敛",
            "第 26 章：幂级数与解析表示",
            "第 27 章：多项式逼近与误差控制",
        ]
        positions = [config.index(title) for title in expected]
        self.assertEqual(sorted(positions), positions)
        self.assertEqual(24, len(re.findall(r"chapters/chapter-2[3-7]/u-06-", config)))

    def test_dependency_map_and_release_surfaces_close_part(self):
        dependencies = (ROOT / "docs" / "curriculum" / "part-06-dependencies.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        course_map = (ROOT / "content" / "course-map.md").read_text(encoding="utf-8")
        self.assertIn("第六部 24 个核心单元、42 学时已全部发布", dependencies)
        self.assertIn("第六部第 27 章，共 122 个学习单元", readme)
        self.assertIn("第 27 章，共 122 个学习单元", course_map)
        for unit_id in (f"u-06-{chapter:02d}-{unit:02d}" for chapter, count in ((23, 5), (24, 5), (25, 5), (26, 5), (27, 4)) for unit in range(1, count + 1)):
            self.assertEqual(1, dependencies.count(f"`{unit_id}`"))

    def test_two_algorithm_sources_are_unique_and_semantically_separated(self):
        series_source = ROOT / "src" / "mathbook_examples" / "series.py"
        approximation_source = ROOT / "src" / "mathbook_examples" / "approximation.py"
        self.assertTrue(series_source.is_file())
        self.assertTrue(approximation_source.is_file())
        approximation = approximation_source.read_text(encoding="utf-8")
        self.assertIn("theoretical_error_bound", approximation)
        self.assertIn("observed_grid_error", approximation)
        self.assertIn('"uncertified"', approximation)
        content = "\n".join(p.read_text(encoding="utf-8") for p in self.unit_pages())
        self.assertEqual(1, content.count("mathbook_examples.approximation"))
        self.assertNotIn("def bernstein_approximation(", content)

    def test_chapter_reviews_and_final_review_record_all_gates(self):
        expected_reviews = [
            "2026-07-30-chapter-23-consistency-review.md",
            "2026-07-30-chapter-24-and-number-series-review.md",
            "2026-07-30-chapter-25-consistency-review.md",
            "2026-07-30-chapter-26-consistency-review.md",
            "2026-07-30-chapter-27-consistency-review.md",
        ]
        for name in expected_reviews:
            self.assertTrue((ROOT / "docs" / "reviews" / name).is_file(), name)
        review = FINAL_REVIEW.read_text(encoding="utf-8")
        for marker in (
            "24 个核心单元",
            "42 学时",
            "数项级数阶段",
            "函数项级数阶段",
            "幂级数",
            "Bernstein",
            "218 道习题",
            "271 个折叠答案",
            "make verify",
            "Zensical",
            "站点检查",
        ):
            self.assertIn(marker, review)

