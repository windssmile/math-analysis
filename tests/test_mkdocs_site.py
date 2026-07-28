from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.check_site import (
    REQUIRED_NAVIGATION_MARKERS,
    REQUIRED_RENDERED_ANCHORS,
    published_page_paths,
    validate_site,
)


class ZensicalSiteValidationTests(unittest.TestCase):
    def test_verify_target_runs_the_zensical_site_checker(self) -> None:
        makefile = (Path(__file__).resolve().parents[1] / "Makefile").read_text(
            encoding="utf-8"
        )
        self.assertIn("zensical build --strict", makefile)
        self.assertNotIn("mkdocs build", makefile)
        self.assertIn("site-check: build", makefile)
        self.assertIn("$(PYTHON) scripts/check_site.py", makefile)

    def test_converts_published_markdown_path_to_directory_url_output(self) -> None:
        self.assertEqual(
            published_page_paths(
                [
                    Path("chapters/chapter-01/u-01-01-01-sets.md"),
                    Path("chapters/chapter-01/index.md"),
                    Path("index.md"),
                ]
            ),
            [
                "chapters/chapter-01/u-01-01-01-sets/index.html",
                "chapters/chapter-01/index.html",
                "index.html",
            ],
        )

    def test_reports_broken_link_and_missing_anchor(self) -> None:
        with TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "index.html").write_text('<a href="missing/">missing</a>', encoding="utf-8")
            page = site / "unit" / "index.html"
            page.parent.mkdir()
            page.write_text('<title>单元 - 数学分析</title>', encoding="utf-8")
            errors = validate_site(
                site,
                expected_pages=["unit/index.html"],
                expected_anchors={"unit/index.html": ["def-u-01-01-01-set"]},
                expected_navigation={"unit/index.html": ["md-sidebar"]},
                expected_titles={"unit/index.html": "单元"},
            )
            self.assertIn("index.html links to missing missing/", errors)
            self.assertIn(
                "rendered site page unit/index.html is missing required anchor: def-u-01-01-01-set",
                errors,
            )
            self.assertIn(
                "rendered site page unit/index.html is missing navigation marker: md-sidebar",
                errors,
            )

    def test_checks_representative_anchors_and_navigation_for_all_three_parts(self) -> None:
        self.assertEqual(
            ["thm-u-02-08-04-contraction"],
            REQUIRED_RENDERED_ANCHORS[
                "chapters/chapter-08/u-02-08-04-contraction-mapping/index.html"
            ],
        )
        self.assertEqual(
            ["thm-u-03-10-04-continuous-extension"],
            REQUIRED_RENDERED_ANCHORS[
                "chapters/chapter-10/u-03-10-04-one-sided-continuity-extension/index.html"
            ],
        )
        self.assertEqual(
            ["thm-u-03-10-05-algebraic-continuity"],
            REQUIRED_RENDERED_ANCHORS[
                "chapters/chapter-10/u-03-10-05-elementary-continuity-bridge/index.html"
            ],
        )
        self.assertEqual(
            [
                "def-u-03-11-01-sequential-compactness",
                "thm-u-03-11-01-closed-interval-sequentially-compact",
            ],
            REQUIRED_RENDERED_ANCHORS[
                "chapters/chapter-11/u-03-11-01-compact-intervals/index.html"
            ],
        )
        self.assertEqual(
            ["alg-u-03-12-02-bisection", "thm-u-03-12-02-bisection-error"],
            REQUIRED_RENDERED_ANCHORS[
                "chapters/chapter-12/u-03-12-02-certified-bisection/index.html"
            ],
        )
        self.assertIn(
            "第二部：数列极限与无限过程",
            REQUIRED_NAVIGATION_MARKERS[
                "chapters/chapter-08/u-02-08-04-contraction-mapping/index.html"
            ],
        )
        self.assertIn(
            "第三部：函数极限、连续性与方程",
            REQUIRED_NAVIGATION_MARKERS[
                "chapters/chapter-12/u-03-12-02-certified-bisection/index.html"
            ],
        )

    def test_checks_representative_anchors_and_navigation_for_part_four(self) -> None:
        page = "chapters/chapter-13/u-04-13-03-local-linearization/index.html"
        self.assertIn(page, REQUIRED_RENDERED_ANCHORS)
        self.assertIn(page, REQUIRED_NAVIGATION_MARKERS)
        self.assertEqual(
            [
                "thm-u-04-13-03-linearization-equivalence",
                "thm-u-04-13-03-differentiable-continuous",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )
        self.assertEqual(
            [
                "md-sidebar",
                "第四部：微分与局部线性化",
                "第 13 章：导数、微分与局部线性模型",
            ],
            REQUIRED_NAVIGATION_MARKERS[page],
        )

    def test_checks_chapter_seventeen_safeguarded_newton_page(self) -> None:
        page = "chapters/chapter-17/u-04-17-04-safeguarded-newton/index.html"
        self.assertEqual(
            [
                "alg-u-04-17-04-safeguarded-newton",
                "thm-u-04-17-04-bracket-contraction",
                "def-u-04-17-04-verifiable-certificate",
                "tbl-u-04-17-04-certificate-comparison",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )
        self.assertEqual(
            [
                "md-sidebar",
                "第四部：微分与局部线性化",
                "第 17 章：凸性、优化、函数形态与 Newton 方法",
            ],
            REQUIRED_NAVIGATION_MARKERS[page],
        )

    def test_checks_chapter_fourteen_chain_rule_page(self) -> None:
        page = "chapters/chapter-14/u-04-14-02-chain-rule/index.html"
        self.assertIn(page, REQUIRED_RENDERED_ANCHORS)
        self.assertIn(page, REQUIRED_NAVIGATION_MARKERS)
        self.assertEqual(
            [
                "thm-u-04-14-02-chain-rule",
                "ex-u-04-14-02-zero-inner-increment",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )
        self.assertEqual(
            [
                "md-sidebar",
                "第四部：微分与局部线性化",
                "第 14 章：求导法则、反函数与高阶导数",
            ],
            REQUIRED_NAVIGATION_MARKERS[page],
        )

    def test_checks_chapter_fourteen_derivative_fluency_page(self) -> None:
        page = (
            "chapters/chapter-14/"
            "u-04-14-05-derivative-fluency-for-antiderivatives/index.html"
        )
        self.assertEqual(
            [
                "tbl-u-04-14-05-structure-signals",
                "ex-u-04-14-05-nested-chain",
                "ex-u-04-14-05-error-diagnosis",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )
        self.assertEqual(
            [
                "md-sidebar",
                "第四部：微分与局部线性化",
                "第 14 章：求导法则、反函数与高阶导数",
            ],
            REQUIRED_NAVIGATION_MARKERS[page],
        )

    def test_checks_chapter_fifteen_cauchy_page(self) -> None:
        page = "chapters/chapter-15/u-04-15-03-cauchy-mean-value/index.html"
        self.assertIn(page, REQUIRED_RENDERED_ANCHORS)
        self.assertIn(page, REQUIRED_NAVIGATION_MARKERS)
        self.assertEqual(
            [
                "thm-u-04-15-03-cauchy-cross",
                "cor-u-04-15-03-cauchy-ratio",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )
        self.assertEqual(
            [
                "md-sidebar",
                "第四部：微分与局部线性化",
                "第 15 章：微分中值定理",
            ],
            REQUIRED_NAVIGATION_MARKERS[page],
        )

    def test_checks_chapter_sixteen_trusted_approximation_page(self) -> None:
        page = "chapters/chapter-16/u-04-16-04-trusted-approximation/index.html"
        self.assertIn(page, REQUIRED_RENDERED_ANCHORS)
        self.assertIn(page, REQUIRED_NAVIGATION_MARKERS)
        self.assertEqual(
            [
                "alg-u-04-16-04-horner",
                "alg-u-04-16-04-centered-difference",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )
        self.assertEqual(
            [
                "md-sidebar",
                "第四部：微分与局部线性化",
                "第 16 章：Taylor 公式与余项",
            ],
            REQUIRED_NAVIGATION_MARKERS[page],
        )


if __name__ == "__main__":
    unittest.main()
