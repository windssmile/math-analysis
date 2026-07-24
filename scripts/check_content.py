"""Validate published MkDocs learning-unit pages without a separate registry."""

from __future__ import annotations

import math
from pathlib import Path
import re
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

REQUIRED_HEADINGS = (
    "## 先备知识",
    "## 学习目标",
    "## 牵引问题",
    "## 探索与猜想",
    "## 概念与理论",
    "## 例题与迁移",
    "## 即时检验与回望",
    "## 习题与答案",
)
V2_REQUIRED_HEADINGS = REQUIRED_HEADINGS + ("## 常见误区与后续",)
PREREQUISITE_CATEGORIES = (
    "book",
    "higher_algebra",
    "analytic_geometry",
    "python",
)
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")


def _read_front_matter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    metadata = yaml.safe_load(text[4:end])
    return (metadata if isinstance(metadata, dict) else {}), text[end + 5 :]


def _non_fenced_lines(text: str) -> list[str]:
    lines: list[str] = []
    fenced = False
    marker = ""
    for line in text.splitlines():
        stripped = line.lstrip()
        if not fenced and stripped.startswith(("```", "~~~")):
            fenced = True
            marker = stripped[:3]
            continue
        if fenced and stripped.startswith(marker):
            fenced = False
            marker = ""
            continue
        if not fenced:
            lines.append(line)
    return lines


def _label(page: Path, root: Path) -> str:
    return page.relative_to(root).as_posix()


def _is_finite_number(value: object) -> bool:
    return type(value) in (int, float) and math.isfinite(value)


def _validate_metadata(metadata: dict[str, object], label: str, errors: list[str]) -> str | None:
    unit_id = metadata.get("unit_id")
    if not isinstance(unit_id, str) or not unit_id.strip():
        errors.append(f"{label}: unit_id must be a nonblank string")
        unit_id = None

    hours = metadata.get("hours")
    if not isinstance(hours, dict):
        errors.append(f"{label}: hours must be a mapping")
    else:
        values: dict[str, float] = {}
        for component in ("theory", "applied"):
            value = hours.get(component)
            if not _is_finite_number(value):
                errors.append(f"{label}: hours.{component} must be a finite number")
                continue
            if value < 0:
                errors.append(f"{label}: hours.{component} must be >= 0")
            if value > 2:
                errors.append(f"{label}: hours.{component} must be <= 2")
            values[component] = float(value)
        if len(values) == 2:
            total = values["theory"] + values["applied"]
            if total <= 0:
                errors.append(f"{label}: hours total must be > 0")
            if total > 2.25:
                errors.append(f"{label}: hours total must be <= 2.25, got {total:g}")

    difficulty = metadata.get("difficulty")
    if type(difficulty) is not int or difficulty < 1:
        errors.append(f"{label}: difficulty must be a positive integer")

    prerequisites = metadata.get("prerequisites")
    if not isinstance(prerequisites, dict):
        errors.append(f"{label}: prerequisites must be a mapping")
    else:
        for category in PREREQUISITE_CATEGORIES:
            values = prerequisites.get(category)
            if not isinstance(values, list) or not all(
                isinstance(value, str) and value.strip() for value in values
            ):
                errors.append(f"{label}: prerequisites.{category} must be a list of nonblank strings")

    for field in ("capabilities", "learning_goals"):
        values = metadata.get(field)
        if not isinstance(values, list) or not values or not all(
            isinstance(value, str) and value.strip() for value in values
        ):
            errors.append(f"{label}: {field} must be a nonempty list of nonblank strings")

    content_standard = metadata.get("content_standard")
    if type(content_standard) is not int or content_standard not in (1, 2):
        errors.append(f"{label}: content_standard must be 1 or 2")
    return unit_id


def _validate_links(page: Path, text: str, root: Path, label: str, errors: list[str]) -> None:
    for target in MARKDOWN_LINK.findall(text):
        if target.startswith(("#", "/", "http:", "https:", "mailto:")):
            continue
        path_part = target.split("#", 1)[0]
        if not path_part.endswith(".md"):
            continue
        resolved = (page.parent / path_part).resolve()
        if not resolved.is_file():
            errors.append(f"{label}: links to missing Markdown page: {path_part}")


def _validate_unit(page: Path, root: Path, errors: list[str]) -> None:
    label = _label(page, root)
    text = page.read_text(encoding="utf-8")
    metadata, body = _read_front_matter(text)
    unit_id = _validate_metadata(metadata, label, errors)
    lines = _non_fenced_lines(body)
    first_heading = next((line for line in lines if line.startswith("# ")), None)
    if unit_id and (first_heading is None or f"{{#{unit_id}}}" not in first_heading):
        errors.append(f"{label}: first level-one heading must contain stable anchor {{#{unit_id}}}")

    standard = metadata.get("content_standard")
    required_headings = V2_REQUIRED_HEADINGS if standard == 2 else REQUIRED_HEADINGS
    line_set = set(lines)
    for heading in required_headings:
        if heading not in line_set:
            errors.append(f"{label}: missing heading: {heading}")

    if standard == 2:
        examples = sum(line.startswith("### ") and "{#ex-" in line for line in lines)
        exercises = sum(line.startswith("### ") and "{#pr-" in line for line in lines)
        answers = sum(line.strip() == '??? note "答案"' for line in lines)
        if examples < 2:
            errors.append(f"{label}: v2 content must contain at least 2 anchored examples")
        if exercises < 5:
            errors.append(f"{label}: v2 content must contain at least 5 anchored exercises")
        if answers < 7:
            errors.append(f"{label}: v2 content must contain at least 7 collapsed answers")

    _validate_links(page, body, root, label, errors)


def validate_content(content_root: Path = CONTENT) -> list[str]:
    """Return every contract violation in published learning-unit pages."""
    errors: list[str] = []
    chapters = content_root / "chapters"
    if not chapters.is_dir():
        return errors
    for page in sorted(chapters.glob("*/*.md")):
        if page.name != "index.md":
            _validate_unit(page, content_root, errors)
    return errors


def main() -> int:
    errors = validate_content()
    for error in errors:
        print(error)
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
