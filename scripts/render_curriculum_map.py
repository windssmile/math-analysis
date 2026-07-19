"""Render the curriculum map from the machine-readable course outline."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "curriculum" / "outline.toml"
TARGET = ROOT / "book" / "curriculum-map.qmd"
CHINESE_NUMBERS = ("一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二")


def render_map(data: Mapping[str, object]) -> str:
    """Return a deterministic Quarto curriculum map for an outline mapping."""
    book = data["book"]
    parts = data["parts"]
    assert isinstance(book, Mapping)
    assert isinstance(parts, list)

    lines = [
        "# 全书课程地图 {#sec-curriculum-map}",
        "",
        (
            "**学时：** "
            f"理论 {book['theory_hours']} + 应用 {book['applied_hours']} "
            f"= {book['total_hours']}"
        ),
        "",
        "本页由 `curriculum/outline.toml` 自动生成。请勿直接编辑。",
    ]
    for part in parts:
        assert isinstance(part, Mapping)
        part_number = part["number"]
        assert isinstance(part_number, int)
        lines.extend(
            (
                "",
                f"## 第{CHINESE_NUMBERS[part_number - 1]}部：{part['title']}",
                f"**问题弧：** {part['question']}",
                "",
                (
                    "**学时：** "
                    f"理论 {part['theory_hours']} + 应用 {part['applied_hours']} "
                    f"= {part['theory_hours'] + part['applied_hours']}"
                ),
                "",
            )
        )
        chapters = part["chapters"]
        assert isinstance(chapters, list)
        for chapter in chapters:
            assert isinstance(chapter, Mapping)
            chapter_id = chapter["id"]
            assert isinstance(chapter_id, str)
            lines.append(
                f"{chapter['number']}. [{chapter['title']}]{{#{chapter_id}}}"
            )

    return "\n".join(lines) + "\n"


def main() -> None:
    """Load the source outline and write its generated map."""
    with SOURCE.open("rb") as handle:
        data = tomllib.load(handle)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(render_map(data), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
