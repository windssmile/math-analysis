"""Validate the rendered Zensical site and its stable teaching anchors."""

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
    "chapters/chapter-10/u-03-10-04-one-sided-continuity-extension/index.html": [
        "thm-u-03-10-04-continuous-extension",
    ],
    "chapters/chapter-10/u-03-10-05-elementary-continuity-bridge/index.html": [
        "thm-u-03-10-05-algebraic-continuity",
    ],
    "chapters/chapter-11/u-03-11-01-compact-intervals/index.html": [
        "def-u-03-11-01-sequential-compactness",
        "thm-u-03-11-01-closed-interval-sequentially-compact",
    ],
    "chapters/chapter-12/u-03-12-02-certified-bisection/index.html": [
        "alg-u-03-12-02-bisection",
        "thm-u-03-12-02-bisection-error",
    ],
    "chapters/chapter-12/u-03-12-04-certificate-comparison/index.html": [
        "thm-u-03-12-04-certificate-boundary",
    ],
    "chapters/chapter-13/u-04-13-03-local-linearization/index.html": [
        "thm-u-04-13-03-linearization-equivalence",
        "thm-u-04-13-03-differentiable-continuous",
    ],
    "chapters/chapter-14/u-04-14-02-chain-rule/index.html": [
        "thm-u-04-14-02-chain-rule",
        "ex-u-04-14-02-zero-inner-increment",
    ],
    "chapters/chapter-14/u-04-14-05-derivative-fluency-for-antiderivatives/index.html": [
        "tbl-u-04-14-05-structure-signals",
        "ex-u-04-14-05-nested-chain",
        "ex-u-04-14-05-error-diagnosis",
    ],
    "chapters/chapter-15/u-04-15-03-cauchy-mean-value/index.html": [
        "thm-u-04-15-03-cauchy-cross",
        "cor-u-04-15-03-cauchy-ratio",
    ],
    "chapters/chapter-16/u-04-16-04-trusted-approximation/index.html": [
        "alg-u-04-16-04-horner",
        "alg-u-04-16-04-centered-difference",
    ],
    "chapters/chapter-17/u-04-17-04-safeguarded-newton/index.html": [
        "alg-u-04-17-04-safeguarded-newton",
        "thm-u-04-17-04-bracket-contraction",
        "def-u-04-17-04-verifiable-certificate",
        "tbl-u-04-17-04-certificate-comparison",
    ],
    "chapters/chapter-18/u-05-18-01-antiderivatives/index.html": [
        "def-u-05-18-01-antiderivative",
        "thm-u-05-18-01-constant-difference",
        "ex-u-05-18-01-darboux-obstruction",
    ],
    "chapters/chapter-18/u-05-18-05-method-selection/index.html": [
        "alg-u-05-18-05-method-selection",
        "tbl-u-05-18-05-verification",
    ],
    "chapters/chapter-19/u-05-19-02-riemann-darboux-equivalence/index.html": [
        "thm-u-05-19-02-darboux-criterion",
        "lem-u-05-19-02-common-refinement-control",
        "thm-u-05-19-02-riemann-darboux-equivalence",
    ],
    "chapters/chapter-19/u-05-19-04-integral-properties/index.html": [
        "thm-u-05-19-04-algebra-closure",
        "thm-u-05-19-04-order-bounds",
        "thm-u-05-19-04-interval-additivity",
    ],
    "chapters/chapter-20/u-05-20-02-fundamental-theorem-part-one/index.html": [
        "lem-u-05-20-02-local-average-control",
        "thm-u-05-20-02-ftc-part-one-pointwise",
    ],
    "chapters/chapter-20/u-05-20-03-newton-leibniz/index.html": [
        "thm-u-05-20-03-newton-leibniz-continuous",
        "thm-u-05-20-03-newton-leibniz-integrable-derivative",
    ],
    "chapters/chapter-20/u-05-20-05-definite-integral-practice/index.html": [
        "tbl-u-05-20-05-method-selection",
        "thm-u-05-20-05-reflection-symmetry",
    ],
    "chapters/chapter-21/u-05-21-02-volume-models/index.html": [
        "lem-u-05-21-02-shell-remainder",
        "thm-u-05-21-02-shell-volume",
    ],
    "chapters/chapter-21/u-05-21-03-arc-length/index.html": [
        "def-u-05-21-03-graph-arc-length",
        "thm-u-05-21-03-c1-graph-arc-length",
    ],
    "chapters/chapter-21/u-05-21-05-modeling-practice/index.html": [
        "alg-u-05-21-05-modeling-workflow",
        "tbl-u-05-21-05-model-selection",
    ],
    "chapters/chapter-22/u-05-22-01-improper-definition/index.html": [
        "def-u-05-22-01-infinite-interval-improper-integral",
        "thm-u-05-22-01-cauchy-tail-criterion",
    ],
    "chapters/chapter-22/u-05-22-03-absolute-conditional-oscillation/index.html": [
        "thm-u-05-22-03-dirichlet-test",
    ],
    "chapters/chapter-22/u-05-22-05-simpson-certificates/index.html": [
        "thm-u-05-22-05-simpson-error",
        "alg-u-05-22-05-certified-simpson-budget",
    ],
    "chapters/chapter-22/u-05-22-06-certified-improper-quadrature/index.html": [
        "alg-u-05-22-06-total-error-workflow",
        "thm-u-05-22-06-total-error-certificate",
    ],
    "chapters/chapter-23/u-06-23-02-cauchy-tail/index.html": [
        "thm-u-06-23-02-cauchy-tail",
        "tbl-u-06-23-02-evidence-boundary",
    ],
    "chapters/chapter-23/u-06-23-05-integral-condensation/index.html": [
        "thm-u-06-23-05-integral-test",
        "thm-u-06-23-05-cauchy-condensation",
        "alg-u-06-23-05-certified-truncation",
    ],
    "chapters/chapter-24/u-06-24-02-leibniz-dirichlet-abel/index.html": [
        "thm-u-06-24-02-leibniz",
        "thm-u-06-24-02-dirichlet",
    ],
    "chapters/chapter-24/u-06-24-03-rearrangements/index.html": [
        "thm-u-06-24-03-absolute-rearrangement",
        "thm-u-06-24-03-riemann-rearrangement",
    ],
    "chapters/chapter-24/u-06-24-04-cauchy-products/index.html": [
        "def-u-06-24-04-cauchy-product",
        "thm-u-06-24-04-mertens",
    ],
    "chapters/chapter-25/u-06-25-01-pointwise-uniform/index.html": [
        "def-u-06-25-01-pointwise",
        "def-u-06-25-01-uniform",
    ],
    "chapters/chapter-25/u-06-25-03-uniform-series-tests/index.html": [
        "thm-u-06-25-03-m-test",
        "thm-u-06-25-03-uniform-dirichlet",
    ],
    "chapters/chapter-25/u-06-25-05-differentiation/index.html": [
        "thm-u-06-25-05-derivative-interchange",
        "tbl-u-06-25-05-exchange-conditions",
    ],
    "chapters/chapter-26/u-06-26-01-radius/index.html": [
        "thm-u-06-26-01-radius-dichotomy",
        "thm-u-06-26-01-cauchy-hadamard",
    ],
    "chapters/chapter-26/u-06-26-03-termwise-operations/index.html": [
        "thm-u-06-26-03-termwise-operations",
        "thm-u-06-26-03-coefficient-uniqueness",
    ],
    "chapters/chapter-26/u-06-26-04-taylor-analytic/index.html": [
        "thm-u-06-26-04-remainder-criterion",
        "ex-u-06-26-04-smooth-not-analytic",
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
    "chapters/chapter-13/u-04-13-03-local-linearization/index.html": [
        "md-sidebar",
        "第四部：微分与局部线性化",
        "第 13 章：导数、微分与局部线性模型",
    ],
    "chapters/chapter-14/u-04-14-02-chain-rule/index.html": [
        "md-sidebar",
        "第四部：微分与局部线性化",
        "第 14 章：求导法则、反函数与高阶导数",
    ],
    "chapters/chapter-14/u-04-14-05-derivative-fluency-for-antiderivatives/index.html": [
        "md-sidebar",
        "第四部：微分与局部线性化",
        "第 14 章：求导法则、反函数与高阶导数",
    ],
    "chapters/chapter-15/u-04-15-03-cauchy-mean-value/index.html": [
        "md-sidebar",
        "第四部：微分与局部线性化",
        "第 15 章：微分中值定理",
    ],
    "chapters/chapter-16/u-04-16-04-trusted-approximation/index.html": [
        "md-sidebar",
        "第四部：微分与局部线性化",
        "第 16 章：Taylor 公式与余项",
    ],
    "chapters/chapter-17/u-04-17-04-safeguarded-newton/index.html": [
        "md-sidebar",
        "第四部：微分与局部线性化",
        "第 17 章：凸性、优化、函数形态与 Newton 方法",
    ],
    "chapters/chapter-18/u-05-18-01-antiderivatives/index.html": [
        "md-sidebar",
        "第五部：积分、累积与数值求积",
        "第 18 章：原函数与积分方法",
    ],
    "chapters/chapter-18/u-05-18-05-method-selection/index.html": [
        "md-sidebar",
        "第五部：积分、累积与数值求积",
        "第 18 章：原函数与积分方法",
    ],
    "chapters/chapter-19/u-05-19-02-riemann-darboux-equivalence/index.html": [
        "md-sidebar",
        "第五部：积分、累积与数值求积",
        "第 19 章：Riemann 积分与可积性",
    ],
    "chapters/chapter-19/u-05-19-04-integral-properties/index.html": [
        "md-sidebar",
        "第五部：积分、累积与数值求积",
        "第 19 章：Riemann 积分与可积性",
    ],
    "chapters/chapter-20/u-05-20-02-fundamental-theorem-part-one/index.html": [
        "md-sidebar",
        "第五部：积分、累积与数值求积",
        "第 20 章：微积分基本定理",
    ],
    "chapters/chapter-20/u-05-20-03-newton-leibniz/index.html": [
        "md-sidebar",
        "第五部：积分、累积与数值求积",
        "第 20 章：微积分基本定理",
    ],
    "chapters/chapter-20/u-05-20-05-definite-integral-practice/index.html": [
        "md-sidebar",
        "第五部：积分、累积与数值求积",
        "第 20 章：微积分基本定理",
    ],
    "chapters/chapter-21/u-05-21-02-volume-models/index.html": [
        "md-sidebar",
        "第五部：积分、累积与数值求积",
        "第 21 章：积分的几何与物理模型",
    ],
    "chapters/chapter-21/u-05-21-03-arc-length/index.html": [
        "md-sidebar",
        "第五部：积分、累积与数值求积",
        "第 21 章：积分的几何与物理模型",
    ],
    "chapters/chapter-21/u-05-21-05-modeling-practice/index.html": [
        "md-sidebar",
        "第五部：积分、累积与数值求积",
        "第 21 章：积分的几何与物理模型",
    ],
    "chapters/chapter-22/u-05-22-01-improper-definition/index.html": [
        "md-sidebar",
        "第五部：积分、累积与数值求积",
        "第 22 章：反常积分与数值求积",
    ],
    "chapters/chapter-22/u-05-22-03-absolute-conditional-oscillation/index.html": [
        "md-sidebar",
        "第五部：积分、累积与数值求积",
        "第 22 章：反常积分与数值求积",
    ],
    "chapters/chapter-22/u-05-22-05-simpson-certificates/index.html": [
        "md-sidebar",
        "第五部：积分、累积与数值求积",
        "第 22 章：反常积分与数值求积",
    ],
    "chapters/chapter-22/u-05-22-06-certified-improper-quadrature/index.html": [
        "md-sidebar",
        "第五部：积分、累积与数值求积",
        "第 22 章：反常积分与数值求积",
    ],
    "chapters/chapter-23/u-06-23-02-cauchy-tail/index.html": [
        "md-sidebar",
        "第六部：无穷级数与函数逼近",
        "第 23 章：数项级数的收敛与正项判别",
    ],
    "chapters/chapter-23/u-06-23-05-integral-condensation/index.html": [
        "md-sidebar",
        "第六部：无穷级数与函数逼近",
        "第 23 章：数项级数的收敛与正项判别",
    ],
    "chapters/chapter-24/u-06-24-02-leibniz-dirichlet-abel/index.html": [
        "md-sidebar",
        "第六部：无穷级数与函数逼近",
        "第 24 章：一般项级数、重排与乘积",
    ],
    "chapters/chapter-24/u-06-24-03-rearrangements/index.html": [
        "md-sidebar",
        "第六部：无穷级数与函数逼近",
        "第 24 章：一般项级数、重排与乘积",
    ],
    "chapters/chapter-24/u-06-24-04-cauchy-products/index.html": [
        "md-sidebar",
        "第六部：无穷级数与函数逼近",
        "第 24 章：一般项级数、重排与乘积",
    ],
    "chapters/chapter-25/u-06-25-01-pointwise-uniform/index.html": [
        "md-sidebar",
        "第六部：无穷级数与函数逼近",
        "第 25 章：函数列、函数项级数与一致收敛",
    ],
    "chapters/chapter-25/u-06-25-03-uniform-series-tests/index.html": [
        "md-sidebar",
        "第六部：无穷级数与函数逼近",
        "第 25 章：函数列、函数项级数与一致收敛",
    ],
    "chapters/chapter-25/u-06-25-05-differentiation/index.html": [
        "md-sidebar",
        "第六部：无穷级数与函数逼近",
        "第 25 章：函数列、函数项级数与一致收敛",
    ],
    "chapters/chapter-26/u-06-26-01-radius/index.html": [
        "md-sidebar",
        "第六部：无穷级数与函数逼近",
        "第 26 章：幂级数与解析表示",
    ],
    "chapters/chapter-26/u-06-26-03-termwise-operations/index.html": [
        "md-sidebar",
        "第六部：无穷级数与函数逼近",
        "第 26 章：幂级数与解析表示",
    ],
    "chapters/chapter-26/u-06-26-04-taylor-analytic/index.html": [
        "md-sidebar",
        "第六部：无穷级数与函数逼近",
        "第 26 章：幂级数与解析表示",
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
    """Map published Markdown paths to directory-style HTML output paths."""
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
