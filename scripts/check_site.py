from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"


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


def validate_site(site: Path) -> list[str]:
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
    return errors


def main() -> int:
    errors = validate_site(SITE)
    pilot_pages = list(SITE.rglob("*u-03-12-01-ivt-bisection*.html"))
    if not pilot_pages:
        errors.append("rendered site is missing the pilot unit page")
    else:
        pilot = pilot_pages[0].read_text(encoding="utf-8")
        for required in ["u-03-12-01", "介值定理", "二分法", "习题与答案"]:
            if required not in pilot:
                errors.append(f"pilot unit page is missing {required}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("site valid: internal links and pilot markers present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
