"""Validate the rendered MkDocs site and its stable teaching anchors."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
SITE = ROOT / "site"

REQUIRED_RENDERED_ANCHORS = {
    "chapters/chapter-01/u-01-01-01-sets/index.html": ["u-01-01-01"],
    "chapters/chapter-02/u-01-02-02-dedekind-cuts/index.html": [
        "def-u-01-02-02-dedekind-cut",
        "ex-u-01-02-02-sqrt2-cut",
    ],
    "chapters/chapter-04/u-01-04-02-interval-bisection/index.html": [
        "def-u-01-04-02-interval-bisection",
        "ex-u-01-04-02-sqrt2-certificate",
    ],
    "chapters/chapter-04/u-01-04-03-approximation-error/index.html": [
        "thm-u-01-04-03-bisection-step-count",
    ],
    "chapters/chapter-08/u-02-08-04-contraction-mapping/index.html": [
        "thm-u-02-08-04-contraction",
    ],
    "chapters/chapter-08/u-02-08-05-limsup-liminf/index.html": [
        "def-u-02-08-05-tail-bounds",
    ],
    "chapters/chapter-09/u-03-09-02-epsilon-delta-limit/index.html": [
        "def-u-03-09-02-function-limit",
    ],
    "chapters/chapter-11/u-03-11-01-compact-intervals/index.html": [
        "thm-u-03-11-01-heine-borel",
    ],
    "chapters/chapter-12/u-03-12-02-certified-bisection/index.html": [
        "alg-u-03-12-02-bisection",
        "thm-u-03-12-02-bisection-error",
    ],
}

REQUIRED_NAVIGATION_MARKERS = {
    "chapters/chapter-01/u-01-01-01-sets/index.html": [
        "md-sidebar",
        "第一部：实数、函数与分析语言",
    ],
    "chapters/chapter-04/u-01-04-02-interval-bisection/index.html": [
        "md-sidebar",
        "第 4 章：递推过程与无限逼近",
    ],
    "chapters/chapter-08/u-02-08-04-contraction-mapping/index.html": [
        "md-sidebar",
        "第二部：数列极限与无限过程",
        "第 8 章：子列、Cauchy 准则与上/下极限",
    ],
    "chapters/chapter-12/u-03-12-02-certified-bisection/index.html": [
        "md-sidebar",
        "第三部：函数极限、连续性与方程",
        "第 12 章：零点、不动点与迭代求解",
    ],
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.title_parts: list[str] = []
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "title":
            self._in_title = True
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)

    @property
    def title(self) -> str:
        return "".join(self.title_parts).strip()


def published_page_paths(paths: list[Path]) -> list[str]:
    """Map MkDocs source paths to directory-style HTML output paths."""
    rendered: list[str] = []
    for path in paths:
        if path.name == "index.md":
            rendered.append(str(path.parent / "index.html"))
        else:
            rendered.append(str(path.with_suffix("") / "index.html"))
    return rendered


def _target_for_link(site: Path, html_file: Path, href: str) -> Path | None:
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc or href.startswith("mailto:") or not parsed.path:
        return None
    relative = unquote(parsed.path)
    target = site / relative.lstrip("/") if relative.startswith("/") else html_file.parent / relative
    if relative.endswith("/") or not target.suffix:
        target = target / "index.html"
    return target


def validate_site(
    site: Path,
    *,
    expected_pages: list[str] | None = None,
    expected_anchors: dict[str, list[str]] | None = None,
    expected_navigation: dict[str, list[str]] | None = None,
    expected_titles: dict[str, str] | None = None,
) -> list[str]:
    errors: list[str] = []
    if not (site / "index.html").is_file():
        return ["site is missing index.html"]

    for html_file in sorted(site.rglob("*.html")):
        parser = PageParser()
        parser.feed(html_file.read_text(encoding="utf-8"))
        for href in parser.links:
            target = _target_for_link(site, html_file, href)
            if target is not None and not target.is_file():
                errors.append(
                    f"{html_file.relative_to(site).as_posix()} links to missing {urlsplit(href).path}"
                )

    for expected_page in expected_pages or []:
        if not (site / expected_page).is_file():
            errors.append(f"rendered site is missing published page: {expected_page}")

    for expected_page, anchors in (expected_anchors or {}).items():
        page = site / expected_page
        if not page.is_file():
            continue
        rendered = page.read_text(encoding="utf-8")
        for anchor in anchors:
            if f'id="{anchor}"' not in rendered:
                errors.append(f"rendered site page {expected_page} is missing required anchor: {anchor}")

    for expected_page, markers in (expected_navigation or {}).items():
        page = site / expected_page
        if not page.is_file():
            continue
        rendered = page.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in rendered:
                errors.append(f"rendered site page {expected_page} is missing navigation marker: {marker}")

    for expected_page, title in (expected_titles or {}).items():
        page = site / expected_page
        if not page.is_file():
            continue
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        if not (parser.title == title or parser.title.startswith(f"{title} - ")):
            errors.append(f"rendered site page {expected_page} has wrong title: expected {title}")
    return errors


def _front_matter_title(page: Path) -> str | None:
    text = page.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    metadata = yaml.safe_load(text[4:end])
    return metadata.get("title") if isinstance(metadata, dict) else None


def main() -> int:
    source_pages = sorted(path.relative_to(CONTENT) for path in CONTENT.rglob("*.md"))
    titles = {
        rendered: title
        for source, rendered in zip(source_pages, published_page_paths(source_pages))
        if (title := _front_matter_title(CONTENT / source))
    }
    errors = validate_site(
        SITE,
        expected_pages=published_page_paths(source_pages),
        expected_anchors=REQUIRED_RENDERED_ANCHORS,
        expected_navigation=REQUIRED_NAVIGATION_MARKERS,
        expected_titles=titles,
    )
    for error in errors:
        print(error)
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
