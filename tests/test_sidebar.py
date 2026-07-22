from pathlib import Path
import re
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
QUARTO = ROOT / "_quarto.yml"
OUTLINE = ROOT / "curriculum" / "outline.toml"
UNITS = ROOT / "curriculum" / "units.toml"


def load_toml(path: Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def quarto_sections() -> tuple[str, str]:
    config = QUARTO.read_text(encoding="utf-8")
    chapters, remainder = config.split("  appendices:", 1)
    sidebar = remainder.split("  sidebar:", 1)[1].split("\nformat:", 1)[0]
    return chapters, sidebar


def chapter_unit_paths(chapters: str) -> list[str]:
    return [
        line.strip().removeprefix("- ")
        for line in chapters.splitlines()
        if line.strip().startswith("- book/part-")
        and line.strip().endswith(".qmd")
    ]


def sidebar_unit_items(sidebar: str) -> list[tuple[str, str]]:
    return re.findall(
        r'^\s+- text: "(.+)"\n\s+href: (book/part-.+\.qmd)$',
        sidebar,
        flags=re.MULTILINE,
    )


class SidebarNumberingTests(unittest.TestCase):
    def expected_parts_and_chapters(self) -> tuple[list[str], dict[str, dict]]:
        outline = load_toml(OUTLINE)
        parts = [part for part in outline["parts"] if part.get("show_units")]
        sections: list[str] = []
        chapters: dict[str, dict] = {}
        chinese_part_numbers = {1: "一", 2: "二", 3: "三"}
        for part in parts:
            sections.append(
                f"第{chinese_part_numbers[part['number']]}部：{part['title']}"
            )
            for chapter in part["chapters"]:
                sections.append(f"第 {chapter['number']} 章：{chapter['title']}")
                chapters[chapter["id"]] = chapter
        return sections, chapters

    def expected_unit_items(self, paths: list[str]) -> list[tuple[str, str]]:
        units = load_toml(UNITS)["units"]
        unit_by_path = {unit["path"]: unit for unit in units}
        _, chapter_by_id = self.expected_parts_and_chapters()
        chapter_positions: dict[str, int] = {}
        expected: list[tuple[str, str]] = []
        for path in paths:
            unit = unit_by_path[path]
            chapter_id = unit["chapter_id"]
            chapter_positions[chapter_id] = chapter_positions.get(chapter_id, 0) + 1
            chapter_number = chapter_by_id[chapter_id]["number"]
            label = f"{chapter_number}.{chapter_positions[chapter_id]} {unit['title']}"
            expected.append((label, path))
        return expected

    def test_html_disables_automatic_section_numbering(self) -> None:
        config = QUARTO.read_text(encoding="utf-8")
        self.assertIn("    number-sections: false", config)
        self.assertNotIn("    number-sections: true", config)

    def test_sidebar_has_exact_part_and_chapter_sections(self) -> None:
        _, sidebar = quarto_sections()
        actual = re.findall(r'^\s+- section: "(.+)"$', sidebar, re.MULTILINE)
        expected, _ = self.expected_parts_and_chapters()
        expected.append("附录")
        self.assertEqual(expected, actual)

    def test_sidebar_units_follow_book_reading_order(self) -> None:
        chapters, sidebar = quarto_sections()
        paths = chapter_unit_paths(chapters)
        self.assertEqual(
            self.expected_unit_items(paths),
            sidebar_unit_items(sidebar),
        )

    def test_sidebar_contains_every_registered_unit_once(self) -> None:
        _, sidebar = quarto_sections()
        actual_paths = [path for _, path in sidebar_unit_items(sidebar)]
        registered_paths = [
            unit["path"] for unit in load_toml(UNITS)["units"]
        ]
        self.assertEqual(len(registered_paths), len(actual_paths))
        self.assertEqual(sorted(registered_paths), sorted(actual_paths))


if __name__ == "__main__":
    unittest.main()
