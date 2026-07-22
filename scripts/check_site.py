from html.parser import HTMLParser
from pathlib import Path
import tomllib
from urllib.parse import unquote, urlsplit
import sys

if __package__:
    from .fix_page_titles import configured_page_titles
else:
    from fix_page_titles import configured_page_titles


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
    "book/part-02/chapter-08/u-02-08-03-cauchy-criterion.html": [
        "thm-u-02-08-03-criterion",
    ],
    "book/part-02/chapter-08/u-02-08-04-contraction-mapping.html": [
        "thm-u-02-08-04-contraction",
    ],
    "book/part-02/chapter-08/u-02-08-05-limsup-liminf.html": [
        "def-u-02-08-05-tail-bounds",
    ],
    "book/part-02/chapter-08/u-02-08-08-limsup-subsequences.html": [
        "thm-u-02-08-08-convergence",
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

REQUIRED_NAVIGATION_MARKERS = {
    "book/part-01/chapter-01/u-01-01-01-sets.html": [
        "第一部：实数、函数与分析语言",
        "第 1 章：函数、集合与数学陈述",
        "1.1 集合怎样组织数学对象？",
        "sidebar-section depth2",
    ],
    "book/part-02/chapter-05/u-02-05-01-sequences.html": [
        "第二部：数列极限与无限过程",
        "第 5 章：数列极限与量词结构",
        "5.1 数列怎样记录无限过程？",
        "5.5 迭代数据何时值得相信？",
        "sidebar-section depth2",
    ],
    "book/part-03/chapter-12/u-03-12-03-fixed-points-and-iteration.html": [
        "第三部：函数极限、连续性与方程",
        "第 12 章：零点、不动点与迭代求解",
        "12.3 有固定点是否意味着简单迭代会收敛？",
        "sidebar-section depth2",
    ],
    "book/bridges/python/functions-loops.html": [
        "附录",
        "Python 知识桥：函数、循环与异常",
    ],
}


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.title_parts: list[str] = []
        self._inside_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "title":
            self._inside_title = True
        if tag != "a":
            return
        attributes = dict(attrs)
        if attributes.get("href"):
            self.links.append(attributes["href"])

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._inside_title = False

    def handle_data(self, data: str) -> None:
        if self._inside_title:
            self.title_parts.append(data)

    @property
    def title(self) -> str:
        return "".join(self.title_parts).strip()


def validate_site(
    site: Path,
    expected_pages: list[str] | None = None,
    expected_anchors: dict[str, list[str]] | None = None,
    expected_navigation: dict[str, list[str]] | None = None,
    expected_titles: dict[str, str] | None = None,
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
        page = site / expected_page
        if not page.is_file():
            errors.append(f"rendered site is missing registered unit page: {expected_page}")
            continue
        rendered = page.read_text(encoding="utf-8")
        if 'class="chapter-number"' in rendered:
            errors.append(
                f"rendered unit page {expected_page} contains automatic chapter numbering"
            )
        if 'class="header-section-number"' in rendered:
            errors.append(
                f"rendered unit page {expected_page} contains automatic heading numbering"
            )
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
    for expected_page, markers in (expected_navigation or {}).items():
        page = site / expected_page
        if not page.is_file():
            continue
        rendered = page.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in rendered:
                errors.append(
                    f"rendered site page {expected_page} is missing navigation marker: "
                    f"{marker}"
                )
    for expected_page, expected_title in (expected_titles or {}).items():
        page = site / expected_page
        if not page.is_file():
            continue
        parser = LinkParser()
        parser.feed(page.read_text(encoding="utf-8"))
        title_is_exact = parser.title == expected_title
        title_has_site_suffix = parser.title.startswith(f"{expected_title} – ")
        if not (title_is_exact or title_has_site_suffix):
            errors.append(
                f"rendered site page {expected_page} has the wrong page title: "
                f"expected {expected_title}"
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
        expected_navigation=REQUIRED_NAVIGATION_MARKERS,
        expected_titles=configured_page_titles(),
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
