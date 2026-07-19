"""Validate the machine-readable mathematics course outline."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.9 and 3.10
    tomllib = None


ROOT = Path(__file__).resolve().parents[1]
OUTLINE = ROOT / "curriculum" / "outline.toml"


def _load_simple_toml(path: Path) -> dict:
    """Load the small TOML subset used by the curriculum outline.

    This keeps the validator dependency-free when run with Python versions
    before 3.11, which do not provide ``tomllib``.
    """
    data: dict = {}
    current: dict | None = data
    current_part: dict | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line == "[book]":
            current = data.setdefault("book", {})
            continue
        if line == "[[parts]]":
            current_part = {}
            data.setdefault("parts", []).append(current_part)
            current = current_part
            continue
        if line == "[[parts.chapters]]":
            if current_part is None:
                raise ValueError("chapter declared before its part")
            current = {}
            current_part.setdefault("chapters", []).append(current)
            continue
        key, separator, value = line.partition("=")
        if not separator or current is None:
            raise ValueError(f"unsupported TOML line: {raw_line}")
        value = value.strip()
        if value.startswith('"'):
            current[key.strip()] = json.loads(value)
        else:
            current[key.strip()] = int(value)
    return data


def load_outline(path: Path = OUTLINE) -> dict:
    """Load an outline TOML file using only the Python standard library."""
    if tomllib is not None:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    return _load_simple_toml(path)


def _hour_total(parts: list[dict], key: str) -> int:
    return sum(part.get(key, 0) for part in parts)


def validate_outline(data: dict) -> list[str]:
    """Return all contract violations found in an outline data structure."""
    errors: list[str] = []
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")

    parts = data.get("parts", [])
    if not isinstance(parts, list) or len(parts) != 12:
        errors.append("outline must contain exactly 12 parts")
        parts = [] if not isinstance(parts, list) else parts

    if [part.get("number") for part in parts] != list(range(1, 13)):
        errors.append("part numbers must be exactly 1..12")

    theory_hours = _hour_total(parts, "theory_hours")
    applied_hours = _hour_total(parts, "applied_hours")
    if theory_hours != 270:
        errors.append(f"theory hours must total 270, got {theory_hours}")
    if applied_hours != 90:
        errors.append(f"applied hours must total 90, got {applied_hours}")

    chapters: list[dict] = []
    for part in parts:
        part_id = part.get("id", "part-?")
        if not isinstance(part.get("question"), str) or not part["question"].strip():
            errors.append(f"{part_id} must have a guiding question")
        part_chapters = part.get("chapters", [])
        if isinstance(part_chapters, list):
            chapters.extend(part_chapters)

    if [chapter.get("number") for chapter in chapters] != list(range(1, 55)):
        errors.append("chapter numbers must be exactly 1..54")
    chapter_ids = [chapter.get("id") for chapter in chapters]
    if len(chapter_ids) != len(set(chapter_ids)):
        errors.append("chapter IDs must be unique")
    for chapter in chapters:
        if not isinstance(chapter.get("title"), str) or not chapter["title"].strip():
            errors.append(f"{chapter.get('id', 'chapter-?')} must have a nonblank title")

    book = data.get("book", {})
    if book.get("theory_hours") != theory_hours:
        errors.append(
            "book.theory_hours must match summed theory hours "
            f"{theory_hours}, got {book.get('theory_hours')}"
        )
    if book.get("applied_hours") != applied_hours:
        errors.append(
            "book.applied_hours must match summed applied hours "
            f"{applied_hours}, got {book.get('applied_hours')}"
        )
    total_hours = theory_hours + applied_hours
    if book.get("total_hours") != total_hours:
        errors.append(
            "book.total_hours must match summed hours "
            f"{total_hours}, got {book.get('total_hours')}"
        )
    return errors


def main() -> int:
    errors = validate_outline(load_outline())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("outline valid: 12 parts, 54 chapters, 270+90=360 hours")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
