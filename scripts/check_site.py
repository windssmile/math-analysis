from html.parser import HTMLParser
from pathlib import Path
import tomllib
from urllib.parse import unquote, urlsplit
import sys


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
UNITS = ROOT / "curriculum" / "units.toml"

REQUIRED_RENDERED_ANCHORS = {
    "book/part-01/chapter-02/u-01-02-02-dedekind-cuts.html": [
        "def-u-01-02-02-dedekind-cut",
        "ex-u-01-02-02-sqrt2-cut",
    ],
    "book/part-01/chapter-02/u-01-02-03-cut-order-operations.html": [
        "def-u-01-02-03-cut-order",
        "thm-u-01-02-03-union-supremum",
    ],
    "book/part-01/chapter-04/u-01-04-01-recurrence.html": [
        "def-u-01-04-01-babylonian-recurrence",
        "ex-u-01-04-01-sqrt2-table",
    ],
    "book/part-01/chapter-04/u-01-04-02-interval-bisection.html": [
        "def-u-01-04-02-interval-bisection",
        "ex-u-01-04-02-sqrt2-certificate",
    ],
    "book/part-01/chapter-04/u-01-04-03-approximation-error.html": [
        "def-u-01-04-03-error-guarantee",
        "thm-u-01-04-03-bisection-step-count",
        "ex-u-01-04-03-bisection-step-count",
    ],
    "book/part-01/chapter-04/u-01-04-04-failure-of-infinite-approximation.html": [
        "def-u-01-04-04-uncertified-approximation",
        "ex-u-01-04-04-small-residual",
        "ex-u-01-04-04-false-bisection",
    ],
    "book/part-03/chapter-09/u-03-09-02-epsilon-delta-limit.html": [
        "def-u-03-09-02-function-limit",
    ],
    "book/part-03/chapter-09/u-03-09-04-sequential-function-limits.html": [
        "thm-u-03-09-04-sequential-criterion",
    ],
    "book/part-03/chapter-11/u-03-11-01-compact-intervals.html": [
        "def-u-03-11-01-compactness",
        "thm-u-03-11-01-heine-borel",
    ],
    "book/part-03/chapter-11/u-03-11-03-uniform-continuity.html": [
        "thm-u-03-11-03-uniform-continuity",
    ],
    "book/part-03/chapter-12/u-03-12-02-certified-bisection.html": [
        "alg-u-03-12-02-bisection",
        "thm-u-03-12-02-bisection-error",
    ],
}


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attributes = dict(attrs)
        if attributes.get("href"):
            self.links.append(attributes["href"])


def validate_site(
    site: Path,
    expected_pages: list[str] | None = None,
    expected_anchors: dict[str, list[str]] | None = None,
) -> list[str]:
    errors: list[str] = []
    if not (site / "index.html").is_file():
        return ["site is missing index.html"]

    for html_file in sorted(site.rglob("*.html")):
        parser = LinkParser()
        parser.feed(html_file.read_text(encoding="utf-8"))
        for link in parser.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or link.startswith("mailto:") or not parsed.path:
                continue
            relative_target = unquote(parsed.path)
            if relative_target.startswith("/"):
                target = site / relative_target.lstrip("/")
            else:
                target = html_file.parent / relative_target
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                errors.append(f"{html_file.relative_to(site)} links to missing {relative_target}")
    for expected_page in expected_pages or []:
        if not (site / expected_page).is_file():
            errors.append(f"rendered site is missing registered unit page: {expected_page}")
    for expected_page, anchors in (expected_anchors or {}).items():
        page = site / expected_page
        if not page.is_file():
            continue
        rendered = page.read_text(encoding="utf-8")
        for anchor in anchors:
            if f'id="{anchor}"' not in rendered:
                errors.append(
                    f"rendered site page {expected_page} is missing required anchor: "
                    f"{anchor}"
                )
    return errors


def registered_unit_pages() -> list[str]:
    with UNITS.open("rb") as handle:
        registry = tomllib.load(handle)
    return [
        str(Path(unit["path"]).with_suffix(".html"))
        for unit in registry["units"]
    ]


def main() -> int:
    errors = validate_site(
        SITE,
        expected_pages=registered_unit_pages(),
        expected_anchors=REQUIRED_RENDERED_ANCHORS,
    )
    for marker_page, markers in {
        "book/part-03/chapter-09/u-03-09-02-epsilon-delta-limit.html": ["u-03-09-02", "函数极限"],
        "book/part-03/chapter-11/u-03-11-01-compact-intervals.html": ["u-03-11-01", "紧致"],
        "book/part-03/chapter-12/u-03-12-02-certified-bisection.html": ["u-03-12-02", "二分法"],
    }.items():
        page = SITE / marker_page
        if not page.is_file():
            errors.append(f"rendered site is missing Part III marker page: {marker_page}")
            continue
        rendered = page.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in rendered:
                errors.append(f"Part III marker page {marker_page} is missing {marker}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("site valid: internal links and Part III markers present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
