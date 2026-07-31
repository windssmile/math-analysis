from pathlib import Path
import unittest
import yaml


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCIES = ROOT / "docs" / "curriculum" / "part-08-dependencies.md"
APPENDIX = ROOT / "content" / "appendices" / "part-08-jordan-content.md"
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
        self.assertIn("当前发布边界：第 36 章", text)
        self.assertIn("18 个核心单元、32 学时", text)
        self.assertIn("chapters/chapter-33/", NAVIGATION)
        self.assertIn("chapters/chapter-34/", NAVIGATION)
        self.assertIn("chapters/chapter-35/", NAVIGATION)
        self.assertIn("chapters/chapter-36/", NAVIGATION)
        self.assertNotIn("chapters/chapter-37/", NAVIGATION)

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

    def test_optional_jordan_appendix_contract(self) -> None:
        text = self.required_text(APPENDIX)
        self.assertIn("选读，不计入第八部核心学时", text)
        for marker in (
            "有限个矩形的并",
            "Jordan 内含量",
            "Jordan 外含量",
            "Jordan 可测",
            "边界",
            "Lebesgue 测度",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("unit_id: u-08-", text)
        self.assertNotIn("hours:", text)
        self.assertEqual(1, NAVIGATION.count("appendices/part-08-jordan-content.md"))

    def test_course_map_records_planned_part(self) -> None:
        text = (ROOT / "content" / "course-map.md").read_text(encoding="utf-8")
        self.assertIn("第八部：重积分与空间测量", text)
        self.assertIn("18 个核心单元", text)
        self.assertIn("32 学时", text)
        for chapter in range(33, 37):
            self.assertIn(f"第 {chapter} 章", text)

    def test_published_core_inventory_and_totals(self) -> None:
        files = sorted(
            path
            for chapter in range(33, 37)
            for path in (ROOT / "content" / "chapters" / f"chapter-{chapter:02d}").glob("u-08-*.md")
        )
        self.assertEqual(18, len(files))
        ids = []
        theory = applied = 0.0
        exercises = answers = 0
        for path in files:
            text = path.read_text(encoding="utf-8")
            meta = yaml.safe_load(text.split("---\n", 2)[1])
            ids.append(meta["unit_id"])
            theory += meta["hours"]["theory"]
            applied += meta["hours"]["applied"]
            exercises += text.count("{#pr-u-08-")
            answers += text.count('??? note "答案"')
            relative = path.relative_to(ROOT / "content").as_posix()
            self.assertEqual(1, NAVIGATION.count(relative))
        self.assertEqual([unit[0] for unit in PART_08_UNITS], ids)
        self.assertEqual((24.0, 8.0, 32.0), (theory, applied, theory + applied))
        self.assertEqual((175, 213), (exercises, answers))

    def test_publication_surfaces_and_algorithm_ownership(self) -> None:
        readme = self.required_text(ROOT / "README.md")
        dependencies = self.required_text(DEPENDENCIES)
        self.assertIn("第八部已发布\n第 33–36 章", readme)
        self.assertIn("18 个核心单元、32 学时", readme)
        self.assertIn("当前发布边界：第 36 章", dependencies)
        self.assertNotIn("chapters/chapter-37/", NAVIGATION)

        mentions = []
        copied_definitions = []
        for chapter in range(33, 37):
            for path in (ROOT / "content" / "chapters" / f"chapter-{chapter:02d}").glob("*.md"):
                text = path.read_text(encoding="utf-8")
                if "tensor_midpoint_2d" in text:
                    mentions.append(path.name)
                if "def tensor_midpoint" in text:
                    copied_definitions.append(path.name)
        self.assertEqual(["u-08-34-05-tensor-midpoint.md"], mentions)
        self.assertEqual([], copied_definitions)


if __name__ == "__main__":
    unittest.main()
