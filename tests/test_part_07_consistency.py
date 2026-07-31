from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-07-dependencies.md"
README = (ROOT / "README.md").read_text(encoding="utf-8")
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

PART_07_UNITS = [
    ("u-07-28-01", 1.25, 0.50),
    ("u-07-28-02", 1.50, 0.25),
    ("u-07-28-03", 1.50, 0.25),
    ("u-07-28-04", 1.50, 0.25),
    ("u-07-28-05", 1.50, 0.50),
    ("u-07-29-01", 1.25, 0.25),
    ("u-07-29-02", 1.50, 0.25),
    ("u-07-29-03", 1.50, 0.25),
    ("u-07-29-04", 1.50, 0.25),
    ("u-07-29-05", 1.25, 0.50),
    ("u-07-29-06", 0.75, 0.75),
    ("u-07-30-01", 1.50, 0.25),
    ("u-07-30-02", 1.25, 0.25),
    ("u-07-30-03", 1.50, 0.25),
    ("u-07-30-04", 1.25, 0.75),
    ("u-07-31-01", 1.50, 0.25),
    ("u-07-31-02", 1.50, 0.25),
    ("u-07-31-03", 1.25, 0.50),
    ("u-07-31-04", 1.00, 0.75),
    ("u-07-32-01", 1.25, 0.25),
    ("u-07-32-02", 1.50, 0.25),
    ("u-07-32-03", 1.50, 0.25),
    ("u-07-32-04", 1.50, 0.50),
    ("u-07-32-05", 1.25, 0.50),
    ("u-07-32-06", 1.00, 1.25),
]


class PartSevenConsistencyTests(unittest.TestCase):
    def required_text(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"missing {path}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def test_locked_part_totals(self) -> None:
        theory = sum(unit[1] for unit in PART_07_UNITS)
        applied = sum(unit[2] for unit in PART_07_UNITS)

        self.assertEqual(
            (25, 33.75, 10.25, 44.0),
            (len(PART_07_UNITS), theory, applied, theory + applied),
        )

    def test_blueprint_records_completed_part_seven(self) -> None:
        text = self.required_text(DEPENDENCIES)
        self.assertIn("当前发布边界：第 32 章", text)
        self.assertIn("25 个核心单元、44 学时", text)

    def test_dependency_map_covers_every_locked_unit(self) -> None:
        text = self.required_text(DEPENDENCIES)

        for unit_id, _theory, _applied in PART_07_UNITS:
            with self.subTest(unit=unit_id):
                rows = [
                    line
                    for line in text.splitlines()
                    if line.startswith(f"| `{unit_id}` |")
                ]
                self.assertEqual(1, len(rows))

    def test_course_map_records_the_planned_part(self) -> None:
        text = (ROOT / "content" / "course-map.md").read_text(encoding="utf-8")

        self.assertIn("第七部：Euclid 空间、多元微分与优化", text)
        self.assertIn("25 个核心单元", text)
        self.assertIn("44 学时", text)
        for chapter in range(28, 33):
            with self.subTest(chapter=chapter):
                self.assertIn(f"第 {chapter} 章", text)
        self.assertIn("chapters/chapter-32/", (ROOT / "mkdocs.yml").read_text(encoding="utf-8"))

    def test_final_release_has_exact_units_metadata_and_navigation(self) -> None:
        paths = list((ROOT / "content" / "chapters").glob("chapter-2[89]/u-07-*.md"))
        paths += list((ROOT / "content" / "chapters").glob("chapter-3[0-2]/u-07-*.md"))
        self.assertEqual(25, len(paths))
        self.assertIn("第七部（第 28–32 章）已经完整发布", README)
        self.assertIn("147 个学习单元", README)
        theory = applied = 0.0
        by_id = {}
        for path in paths:
            text = path.read_text(encoding="utf-8")
            metadata = yaml.safe_load(text.split("---\n", 2)[1])
            by_id[metadata["unit_id"]] = path
            theory += float(metadata["hours"]["theory"])
            applied += float(metadata["hours"]["applied"])
            self.assertEqual(1, NAVIGATION.count(f"chapters/{path.parent.name}/{path.name}"))
        self.assertEqual((33.75, 10.25, 44.0), (theory, applied, theory + applied))
        self.assertEqual({unit[0] for unit in PART_07_UNITS}, set(by_id))

    def test_algorithm_pages_reuse_one_unique_source_each(self) -> None:
        contracts = [
            ("chapter-29/u-07-29-06-linearization-check.md", "mathbook_examples.multivariate", "def check_jacobian("),
            ("chapter-31/u-07-31-04-newton-systems.md", "mathbook_examples.nonlinear", "def newton_system("),
            ("chapter-32/u-07-32-06-optimization-check.md", "mathbook_examples.optimization", "def gradient_descent("),
        ]
        for relative, module, copied_definition in contracts:
            text = self.required_text(ROOT / "content" / "chapters" / relative)
            with self.subTest(page=relative):
                self.assertIn(module, text)
                self.assertNotIn(copied_definition, text)

    def test_scope_boundaries_and_final_review_are_recorded(self) -> None:
        units = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (ROOT / "content" / "chapters").glob("chapter-3[0-2]/u-07-*.md")
        )
        self.assertIn("不覆盖不等式约束", units)
        self.assertIn("不建立一般 KKT 理论", units)
        self.assertNotIn("KKT 条件给出", units)
        report = self.required_text(
            ROOT / "docs" / "reviews" / "2026-07-31-part-07-consistency-review.md"
        )
        for marker in ("25 个核心单元", "44 学时", "239", "293", "chapter-32", "29.6", "31.4", "32.6"):
            self.assertIn(marker, report)


if __name__ == "__main__":
    unittest.main()
