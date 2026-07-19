"""Validate the machine-readable learning-unit registry."""

from __future__ import annotations

from collections.abc import Mapping
import math
from pathlib import Path, PurePosixPath
import sys
import tomllib


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"
OUTLINE = ROOT / "curriculum" / "outline.toml"

REQUIRED_LIST_FIELDS = (
    "book_prerequisites",
    "higher_algebra_prerequisites",
    "analytic_geometry_prerequisites",
    "python_prerequisites",
    "knowledge_bridges",
    "capabilities",
    "learning_goals",
)
ALLOWED_CAPABILITIES = frozenset(
    {
        "concepts",
        "proof",
        "analytic_calculation",
        "numerical_algorithm",
        "modeling",
        "mathematical_expression",
    }
)
REQUIRED_QMD_HEADINGS = (
    "## 先备知识",
    "## 学习目标",
    "## 牵引问题",
    "## 探索与猜想",
    "## 概念与理论",
    "## 例题与迁移",
    "## 即时检验与回望",
    "## 习题与答案",
)


def load_units(path: Path = UNITS) -> dict:
    """Load a unit registry using Python 3.12's standard-library TOML parser."""
    with path.open("rb") as handle:
        return tomllib.load(handle)


def load_outline(path: Path = OUTLINE) -> dict:
    """Load the course outline used to resolve chapter IDs."""
    with path.open("rb") as handle:
        return tomllib.load(handle)


def _is_number(value: object) -> bool:
    return type(value) in (int, float)


def _is_finite_number(value: int | float) -> bool:
    return type(value) is int or math.isfinite(value)


def _repository_path(
    value: str, label: str, root: Path, errors: list[str]
) -> Path | None:
    relative_path = PurePosixPath(value)
    is_normalized = (
        value == relative_path.as_posix()
        and not relative_path.is_absolute()
        and ".." not in relative_path.parts
        and "\\" not in value
    )
    if not is_normalized:
        errors.append(f"{label} must be a normalized repository-relative path")
        return None

    resolved_root = root.resolve()
    resolved_path = (resolved_root / Path(*relative_path.parts)).resolve()
    if not resolved_path.is_relative_to(resolved_root):
        errors.append(f"{label} must remain under the repository root")
        return None
    return resolved_path


def _non_fenced_lines(text: str) -> list[str]:
    lines: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    for line in text.splitlines():
        stripped = line.lstrip()
        marker_character = stripped[:1]
        marker_length = 0
        if marker_character in ("`", "~"):
            marker_length = len(stripped) - len(stripped.lstrip(marker_character))

        if fence_character is None:
            if marker_length >= 3:
                fence_character = marker_character
                fence_length = marker_length
            else:
                lines.append(line)
        elif (
            marker_character == fence_character
            and marker_length >= fence_length
            and not stripped[marker_length:].strip()
        ):
            fence_character = None
            fence_length = 0
    return lines


def _chapter_ids(outline: object, errors: list[str]) -> set[str]:
    if not isinstance(outline, Mapping):
        errors.append("outline must be a mapping")
        return set()

    parts = outline.get("parts")
    if not isinstance(parts, list):
        errors.append("outline.parts must be a list")
        return set()

    chapter_ids: set[str] = set()
    for part_index, part in enumerate(parts):
        if not isinstance(part, Mapping):
            errors.append(f"outline.parts[{part_index}] must be a mapping")
            continue
        chapters = part.get("chapters")
        if not isinstance(chapters, list):
            errors.append(f"outline.parts[{part_index}].chapters must be a list")
            continue
        for chapter_index, chapter in enumerate(chapters):
            if not isinstance(chapter, Mapping):
                errors.append(
                    f"outline.parts[{part_index}].chapters[{chapter_index}] "
                    "must be a mapping"
                )
                continue
            chapter_id = chapter.get("id")
            if isinstance(chapter_id, str) and chapter_id.strip():
                chapter_ids.add(chapter_id)
    return chapter_ids


def _validate_nonblank_string(
    unit: Mapping[str, object], field: str, label: str, errors: list[str]
) -> str | None:
    value = unit.get(field)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}.{field} must be a nonblank string")
        return None
    return value


def _validate_string_list(
    values: list[object], field: str, label: str, errors: list[str]
) -> None:
    for index, value in enumerate(values):
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{label}.{field}[{index}] must be a nonblank string")


def _validate_content_file(
    unit_id: str, relative_path: str, content_path: Path, errors: list[str]
) -> None:
    if not content_path.is_file():
        errors.append(f"{unit_id} content file does not exist: {relative_path}")
        return

    try:
        text = content_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"{unit_id} content file cannot be read: {relative_path}: {exc}")
        return

    non_fenced_lines = _non_fenced_lines(text)
    anchor = f"{{#{unit_id}}}"
    first_heading = next(
        (line for line in non_fenced_lines if line.startswith("# ")),
        None,
    )
    if first_heading is None or anchor not in first_heading:
        errors.append(
            f"{unit_id} content file first level-one heading must contain "
            f"stable anchor {anchor}"
        )

    lines = set(non_fenced_lines)
    for heading in REQUIRED_QMD_HEADINGS:
        if heading not in lines:
            errors.append(f"{unit_id} content file is missing heading: {heading}")


def validate_units(
    registry: object, outline: object, *, root: Path = ROOT
) -> list[str]:
    """Return contract violations without raising on malformed structures."""
    errors: list[str] = []
    if not isinstance(registry, Mapping):
        return ["registry must be a mapping"]

    if type(registry.get("schema_version")) is not int or registry.get(
        "schema_version"
    ) != 1:
        errors.append("schema_version must be the integer 1")

    chapter_ids = _chapter_ids(outline, errors)
    units = registry.get("units")
    if not isinstance(units, list):
        errors.append("units must be a list")
        return errors

    seen_ids: set[str] = set()
    for index, unit in enumerate(units):
        if not isinstance(unit, Mapping):
            errors.append(f"units[{index}] must be a mapping")
            continue

        raw_id = unit.get("id")
        label = raw_id if isinstance(raw_id, str) and raw_id.strip() else f"units[{index}]"
        unit_id = _validate_nonblank_string(unit, "id", label, errors)
        if unit_id is not None:
            if unit_id in seen_ids:
                errors.append(f"duplicate unit id: {unit_id}")
            seen_ids.add(unit_id)

        chapter_id = _validate_nonblank_string(
            unit, "chapter_id", label, errors
        )
        if chapter_id is not None and chapter_id not in chapter_ids:
            errors.append(f"{label} references unknown chapter {chapter_id}")

        _validate_nonblank_string(unit, "title", label, errors)
        relative_path = _validate_nonblank_string(unit, "path", label, errors)

        valid_hours: dict[str, int | float] = {}
        for field in ("theory_hours", "applied_hours"):
            value = unit.get(field)
            if not _is_number(value):
                errors.append(f"{label}.{field} must be a number")
            elif not _is_finite_number(value):
                errors.append(f"{label}.{field} must be a finite number")
            elif value < 0:
                errors.append(f"{label}.{field} must be >= 0")
            else:
                valid_hours[field] = value
        if len(valid_hours) == 2:
            theory_hours = valid_hours["theory_hours"]
            applied_hours = valid_hours["applied_hours"]
            if theory_hours > 2 or applied_hours > 2:
                errors.append(
                    f"{label} theory_hours and applied_hours must each be <= 2"
                )
            else:
                total = theory_hours + applied_hours
                if total <= 0 or total > 2.5:
                    errors.append(
                        f"{label} theory_hours + applied_hours must be > 0 and <= 2.5, "
                        f"got {total:g}"
                    )

        difficulty = unit.get("difficulty")
        if type(difficulty) is not int or difficulty <= 0:
            errors.append(f"{label}.difficulty must be a positive integer")

        valid_lists: dict[str, list[object]] = {}
        for field in REQUIRED_LIST_FIELDS:
            value = unit.get(field)
            if not isinstance(value, list):
                errors.append(f"{label}.{field} must be a list")
            else:
                valid_lists[field] = value
                _validate_string_list(value, field, label, errors)

        for prerequisite_index, prerequisite in enumerate(
            valid_lists.get("book_prerequisites", [])
        ):
            if (
                isinstance(prerequisite, str)
                and prerequisite.strip()
                and prerequisite not in chapter_ids
            ):
                errors.append(
                    f"{label}.book_prerequisites[{prerequisite_index}] "
                    f"references unknown chapter {prerequisite}"
                )

        capabilities = valid_lists.get("capabilities", [])
        for capability in capabilities:
            if isinstance(capability, str) and capability not in ALLOWED_CAPABILITIES:
                errors.append(
                    f"{label}.capabilities contains unsupported capability {capability}"
                )

        learning_goals = valid_lists.get("learning_goals")
        if learning_goals is not None and not learning_goals:
            errors.append(f"{label}.learning_goals must not be empty")

        for bridge_index, bridge in enumerate(
            valid_lists.get("knowledge_bridges", [])
        ):
            if isinstance(bridge, str) and bridge.strip():
                bridge_path = _repository_path(
                    bridge,
                    f"{label}.knowledge_bridges[{bridge_index}]",
                    root,
                    errors,
                )
                if bridge_path is not None and not bridge_path.is_file():
                    errors.append(f"{label} knowledge bridge does not exist: {bridge}")

        if unit_id is not None and relative_path is not None:
            content_path = _repository_path(
                relative_path, f"{label}.path", root, errors
            )
            if content_path is not None:
                _validate_content_file(unit_id, relative_path, content_path, errors)

    return errors


def main() -> int:
    try:
        registry = load_units()
    except (OSError, tomllib.TOMLDecodeError) as exc:
        print(f"ERROR: failed to load {UNITS.relative_to(ROOT)}: {exc}")
        return 1

    try:
        outline = load_outline()
    except (OSError, tomllib.TOMLDecodeError) as exc:
        print(f"ERROR: failed to load {OUTLINE.relative_to(ROOT)}: {exc}")
        return 1

    errors = validate_units(registry, outline)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    units = registry.get("units", [])
    print(f"unit registry valid: {len(units)} unit(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
