"""Convert the supported Quarto Markdown surface to Material Markdown."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


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


def convert_markdown(source: str) -> str:
    """Convert stable anchors, links and supported Quarto callout fences."""
    converted: list[str] = []
    callout: str | None = None
    for raw_line in source.splitlines():
        stripped = raw_line.strip()
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
            if callout == "answer" and stripped == "## 答案":
                continue
            converted.append("    " + raw_line if raw_line else "")
            continue
        line = QMD_LINK.sub(r"\1.md", raw_line)
        converted.append(_convert_heading(line))
    return "\n".join(converted) + "\n"


def convert_tree(source: Path, destination: Path) -> dict[str, list[str]]:
    """Convert a directory tree without overwriting existing destination pages."""
    report: dict[str, list[str]] = {"converted": [], "skipped": []}
    for page in sorted(source.rglob("*.qmd")):
        target = destination / page.relative_to(source).with_suffix(".md")
        if target.exists():
            report["skipped"].append(f"{page}: destination exists")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(convert_markdown(page.read_text(encoding="utf-8")), encoding="utf-8")
        report["converted"].append(str(page))
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    if not args.source.is_dir():
        parser.error(f"source directory does not exist: {args.source}")
    report = convert_tree(args.source, args.destination)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return int(bool(report["skipped"]))


if __name__ == "__main__":
    raise SystemExit(main())
