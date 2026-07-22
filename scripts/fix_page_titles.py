from html import escape
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
QUARTO = ROOT / "_quarto.yml"
TITLE_PATTERN = re.compile(r"(<title>)(.*?)(</title>)", re.DOTALL)
HEADING_PATTERN = re.compile(
    r"^#\s+(.+?)(?:\s+\{[^}]*\})?\s*$",
    re.MULTILINE,
)


def source_page_title(source: Path) -> str:
    text = source.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        closing = text.find("\n---\n", 4)
        if closing != -1:
            frontmatter = text[4:closing]
            title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', frontmatter, re.MULTILINE)
            if title_match is not None:
                return title_match.group(1)
    heading_match = HEADING_PATTERN.search(text)
    if heading_match is None:
        raise ValueError(f"source page has no title or level-one heading: {source}")
    return heading_match.group(1)


def configured_page_titles() -> dict[str, str]:
    config = QUARTO.read_text(encoding="utf-8")
    project = config.split("project:", 1)[1].split("\nwebsite:", 1)[0]
    render_match = re.search(
        r"^  render:\n((?:    - .+\n?)+)",
        project,
        re.MULTILINE,
    )
    if render_match is None:
        raise ValueError("_quarto.yml must define project.render")
    sources = [
        line.strip().removeprefix("- ")
        for line in render_match.group(1).splitlines()
        if line.strip().startswith("- ")
    ]
    return {
        str(Path(source).with_suffix(".html")): source_page_title(ROOT / source)
        for source in sources
    }


def fix_page_title(page: Path, title: str) -> None:
    rendered = page.read_text(encoding="utf-8")
    match = TITLE_PATTERN.search(rendered)
    if match is None:
        raise ValueError(f"rendered page has no title element: {page}")
    _, separator, suffix = match.group(2).partition(" – ")
    replacement = escape(title, quote=False)
    if separator:
        replacement = f"{replacement} – {suffix}"
    updated = TITLE_PATTERN.sub(
        lambda title_match: (
            f"{title_match.group(1)}{replacement}{title_match.group(3)}"
        ),
        rendered,
        count=1,
    )
    if updated != rendered:
        page.write_text(updated, encoding="utf-8")


def main() -> int:
    for relative_page, title in configured_page_titles().items():
        page = SITE / relative_page
        if page.is_file():
            fix_page_title(page, title)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
