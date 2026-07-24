"""Convert the supported Quarto Markdown surface to Material Markdown."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import tomllib

import yaml


HEADING_ATTRIBUTES = re.compile(r"^(#{1,6}\s+.+?)\s+\{([^}]*)\}\s*$")
QMD_LINK = re.compile(r"(\]\([^\s)#]+)\.qmd(?=[)#])")


def _convert_heading(line: str) -> str:
    match = HEADING_ATTRIBUTES.match(line)
    if not match:
        return line
    heading, attributes = match.groups()
    anchor = re.search(r"#([A-Za-z0-9_-]+)", attributes)
    if anchor:
        return f"{heading} {{#{anchor.group(1)}}}"
    return heading


def metadata_from_unit(unit: dict[str, object]) -> dict[str, object]:
    """Translate one legacy unit record into page-local MkDocs metadata."""
    return {
        "title": unit["title"],
        "unit_id": unit["id"],
        "hours": {
            "theory": unit["theory_hours"],
            "applied": unit["applied_hours"],
        },
        "difficulty": unit["difficulty"],
        "prerequisites": {
            "book": unit["book_prerequisites"],
            "higher_algebra": unit["higher_algebra_prerequisites"],
            "analytic_geometry": unit["analytic_geometry_prerequisites"],
            "python": unit["python_prerequisites"],
        },
        "capabilities": unit["capabilities"],
        "learning_goals": unit["learning_goals"],
        "content_standard": unit.get("content_standard", 1),
    }


def with_front_matter(content: str, metadata: dict[str, object]) -> str:
    front_matter = yaml.safe_dump(
        metadata,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    )
    return f"---\n{front_matter}---\n\n{content}"


def convert_markdown(source: str) -> str:
    """Convert stable anchors, links and supported Quarto callout fences."""
    converted: list[str] = []
    callout: str | None = None
    for raw_line in source.splitlines():
        stripped = raw_line.strip()
        if stripped == "::: {.unit-meta}":
            callout = "unit-meta"
            continue
        if stripped == '::: {.callout-note collapse="true"}':
            callout = "answer"
            converted.append('??? note "答案"')
            continue
        if stripped == "::: {.callout-note}":
            callout = "note"
            converted.append("!!! note")
            continue
        if stripped == ":::" and callout:
            callout = None
            continue
        if callout:
            if callout == "unit-meta":
                continue
            if callout == "answer" and stripped == "## 答案":
                continue
            converted.append("    " + raw_line if raw_line else "")
            continue
        line = QMD_LINK.sub(r"\1.md", raw_line).replace(
            "curriculum-map.md", "course-map.md"
        )
        converted.append(_convert_heading(line))
    return "\n".join(converted) + "\n"


def convert_tree(
    source: Path,
    destination: Path,
    *,
    metadata_by_source: dict[str, dict[str, object]] | None = None,
    repository_root: Path | None = None,
) -> dict[str, list[str]]:
    """Convert a directory tree without overwriting existing destination pages."""
    report: dict[str, list[str]] = {"converted": [], "skipped": []}
    for page in sorted(source.rglob("*.qmd")):
        target = destination / page.relative_to(source).with_suffix(".md")
        if target.exists():
            report["skipped"].append(f"{page}: destination exists")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        converted = convert_markdown(page.read_text(encoding="utf-8"))
        if metadata_by_source and repository_root:
            source_key = page.resolve().relative_to(repository_root.resolve()).as_posix()
            unit = metadata_by_source.get(source_key)
            if unit:
                converted = with_front_matter(converted, metadata_from_unit(unit))
        target.write_text(converted, encoding="utf-8")
        report["converted"].append(str(page))
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--registry", type=Path)
    args = parser.parse_args()
    if not args.source.is_dir():
        parser.error(f"source directory does not exist: {args.source}")
    metadata_by_source = None
    repository_root = None
    if args.registry:
        with args.registry.open("rb") as handle:
            registry = tomllib.load(handle)
        units = registry.get("units", [])
        if not isinstance(units, list):
            parser.error(f"registry has no units list: {args.registry}")
        metadata_by_source = {
            unit["path"]: unit
            for unit in units
            if isinstance(unit, dict) and isinstance(unit.get("path"), str)
        }
        repository_root = args.registry.resolve().parents[1]
    report = convert_tree(
        args.source,
        args.destination,
        metadata_by_source=metadata_by_source,
        repository_root=repository_root,
    )
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return int(bool(report["skipped"]))


if __name__ == "__main__":
    raise SystemExit(main())
