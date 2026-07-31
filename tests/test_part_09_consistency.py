from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-09-dependencies.md"
COURSE_MAP = ROOT / "content" / "course-map.md"
NAVIGATION = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

PART_09_UNITS = [
    unit
    for chapter in range(37, 41)
    for unit in (
        (f"u-09-{chapter}-01", 1.50, 0.00),
        (f"u-09-{chapter}-02", 1.25, 0.25),
        (f"u-09-{chapter}-03", 1.00, 0.50),
        (f"u-09-{chapter}-04", 0.75, 0.75),
    )
] + [
    ("u-09-41-01", 1.50, 0.00),
    ("u-09-41-02", 1.25, 0.25),
    ("u-09-41-03", 1.25, 0.25),
    ("u-09-41-04", 1.00, 0.50),
    ("u-09-41-05", 1.00, 1.00),
]


class PartNineConsistencyTests(unittest.TestCase):
    def required_text(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"missing {path}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def test_locked_part_totals(self) -> None:
        theory = sum(unit[1] for unit in PART_09_UNITS)
        applied = sum(unit[2] for unit in PART_09_UNITS)
        self.assertEqual(
            (21, 24.0, 8.0, 32.0),
            (len(PART_09_UNITS), theory, applied, theory + applied),
        )

    def test_blueprint_tracks_current_release_boundary(self) -> None:
        text = self.required_text(DEPENDENCIES)
        self.assertIn("当前发布边界：第 36 章", text)
        self.assertIn("21 个核心单元、32 学时", text)
        self.assertNotIn("chapters/chapter-37/", NAVIGATION)

    def test_dependency_map_covers_every_locked_unit(self) -> None:
        text = self.required_text(DEPENDENCIES)
        for unit_id, _theory, _applied in PART_09_UNITS:
            rows = [
                line
                for line in text.splitlines()
                if line.startswith(f"| `{unit_id}` |")
            ]
            with self.subTest(unit=unit_id):
                self.assertEqual(1, len(rows))
                self.assertNotIn("微分形式", rows[0] if rows else "")

    def test_optional_appendix_is_not_core(self) -> None:
        text = self.required_text(DEPENDENCIES)
        self.assertIn("选读附录不计入核心学时", text)

    def test_course_map_records_planned_part(self) -> None:
        text = self.required_text(COURSE_MAP)
        self.assertIn("第九部：曲线、曲面与向量分析", text)
        self.assertIn("21 个核心单元", text)
        self.assertIn("32 学时", text)
        self.assertIn("规划中", text)
        for chapter in range(37, 42):
            self.assertIn(f"第 {chapter} 章", text)


if __name__ == "__main__":
    unittest.main()
