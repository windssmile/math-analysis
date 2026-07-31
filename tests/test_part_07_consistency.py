from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-07-dependencies.md"

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

    def test_blueprint_stops_before_part_eight(self) -> None:
        text = self.required_text(DEPENDENCIES)
        self.assertIn("当前发布边界：第 ", text)
        self.assertIn("25 个核心单元、44 学时", text)
        self.assertNotIn(
            "chapter-33",
            (ROOT / "mkdocs.yml").read_text(encoding="utf-8"),
        )

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
        self.assertNotIn("chapters/chapter-33/", (ROOT / "mkdocs.yml").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
