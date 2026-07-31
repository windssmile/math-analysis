from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-08-dependencies.md"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

PART_08_UNITS = [
    ("u-08-33-01", 1.50, 0.25),
    ("u-08-33-02", 1.75, 0.00),
    ("u-08-33-03", 1.50, 0.25),
    ("u-08-33-04", 1.50, 0.25),
    ("u-08-34-01", 1.50, 0.25),
    ("u-08-34-02", 1.25, 0.50),
    ("u-08-34-03", 1.00, 0.75),
    ("u-08-34-04", 1.25, 0.50),
    ("u-08-34-05", 1.00, 1.00),
    ("u-08-35-01", 1.50, 0.25),
    ("u-08-35-02", 1.50, 0.25),
    ("u-08-35-03", 1.50, 0.25),
    ("u-08-35-04", 1.50, 0.25),
    ("u-08-36-01", 1.50, 0.25),
    ("u-08-36-02", 1.50, 0.25),
    ("u-08-36-03", 1.00, 0.75),
    ("u-08-36-04", 0.75, 1.00),
    ("u-08-36-05", 1.00, 1.00),
]


class PartEightConsistencyTests(unittest.TestCase):
    def required_text(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"missing {path}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def test_locked_part_totals(self) -> None:
        theory = sum(unit[1] for unit in PART_08_UNITS)
        applied = sum(unit[2] for unit in PART_08_UNITS)
        self.assertEqual(
            (18, 24.0, 8.0, 32.0),
            (len(PART_08_UNITS), theory, applied, theory + applied),
        )

    def test_blueprint_tracks_current_release_boundary(self) -> None:
        text = self.required_text(DEPENDENCIES)
        self.assertIn("当前发布边界：第 35 章", text)
        self.assertIn("18 个核心单元、32 学时", text)
        self.assertIn("chapters/chapter-33/", NAVIGATION)
        self.assertIn("chapters/chapter-34/", NAVIGATION)
        self.assertIn("chapters/chapter-35/", NAVIGATION)
        self.assertNotIn("chapters/chapter-36/", NAVIGATION)

    def test_dependency_map_covers_every_locked_unit(self) -> None:
        text = self.required_text(DEPENDENCIES)
        for unit_id, _theory, _applied in PART_08_UNITS:
            rows = [
                line
                for line in text.splitlines()
                if line.startswith(f"| `{unit_id}` |")
            ]
            with self.subTest(unit=unit_id):
                self.assertEqual(1, len(rows))

    def test_appendix_is_not_a_core_prerequisite(self) -> None:
        text = self.required_text(DEPENDENCIES)
        self.assertIn("选读附录不计入核心学时", text)
        for line in text.splitlines():
            if line.startswith("| `u-08-"):
                self.assertNotIn("Jordan", line)

    def test_course_map_records_planned_part(self) -> None:
        text = (ROOT / "content" / "course-map.md").read_text(encoding="utf-8")
        self.assertIn("第八部：重积分与空间测量", text)
        self.assertIn("18 个核心单元", text)
        self.assertIn("32 学时", text)
        for chapter in range(33, 37):
            self.assertIn(f"第 {chapter} 章", text)


if __name__ == "__main__":
    unittest.main()
