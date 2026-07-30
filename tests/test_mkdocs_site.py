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
    def test_checks_chapter_twenty_four_core_pages(self) -> None:
        for page, anchors in {
            "chapters/chapter-24/u-06-24-02-leibniz-dirichlet-abel/index.html": (
                "thm-u-06-24-02-leibniz",
                "thm-u-06-24-02-dirichlet",
            ),
            "chapters/chapter-24/u-06-24-03-rearrangements/index.html": (
                "thm-u-06-24-03-absolute-rearrangement",
                "thm-u-06-24-03-riemann-rearrangement",
            ),
            "chapters/chapter-24/u-06-24-04-cauchy-products/index.html": (
                "def-u-06-24-04-cauchy-product",
                "thm-u-06-24-04-mertens",
            ),
        }.items():
            self.assertIn(page, REQUIRED_RENDERED_ANCHORS)
            for anchor in anchors:
                self.assertIn(anchor, REQUIRED_RENDERED_ANCHORS[page])
            self.assertEqual(
                [
                    "md-sidebar",
                    "第六部：无穷级数与函数逼近",
                    "第 24 章：一般项级数、重排与乘积",
                ],
                REQUIRED_NAVIGATION_MARKERS[page],
            )

    def test_checks_chapter_twenty_three_cauchy_and_integral_pages(self) -> None:
        for page, anchors in {
            "chapters/chapter-23/u-06-23-02-cauchy-tail/index.html": (
                "thm-u-06-23-02-cauchy-tail",
                "tbl-u-06-23-02-evidence-boundary",
            ),
            "chapters/chapter-23/u-06-23-05-integral-condensation/index.html": (
                "thm-u-06-23-05-integral-test",
                "alg-u-06-23-05-certified-truncation",
            ),
        }.items():
            self.assertIn(page, REQUIRED_RENDERED_ANCHORS)
            for anchor in anchors:
                self.assertIn(anchor, REQUIRED_RENDERED_ANCHORS[page])
            self.assertEqual(
                [
                    "md-sidebar",
                    "第六部：无穷级数与函数逼近",
                    "第 23 章：数项级数的收敛与正项判别",
                ],
                REQUIRED_NAVIGATION_MARKERS[page],
            )

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

    def test_checks_chapter_eighteen_antiderivative_page(self) -> None:
        page = "chapters/chapter-18/u-05-18-01-antiderivatives/index.html"
        self.assertIn(page, REQUIRED_RENDERED_ANCHORS)
        self.assertIn(page, REQUIRED_NAVIGATION_MARKERS)
        self.assertEqual(
            [
                "def-u-05-18-01-antiderivative",
                "thm-u-05-18-01-constant-difference",
                "ex-u-05-18-01-darboux-obstruction",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )
        self.assertEqual(
            [
                "md-sidebar",
                "第五部：积分、累积与数值求积",
                "第 18 章：原函数与积分方法",
            ],
            REQUIRED_NAVIGATION_MARKERS[page],
        )

    def test_checks_chapter_eighteen_method_selection_page(self) -> None:
        page = "chapters/chapter-18/u-05-18-05-method-selection/index.html"
        self.assertIn(page, REQUIRED_RENDERED_ANCHORS)
        self.assertIn(page, REQUIRED_NAVIGATION_MARKERS)
        self.assertEqual(
            [
                "alg-u-05-18-05-method-selection",
                "tbl-u-05-18-05-verification",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )
        self.assertEqual(
            [
                "md-sidebar",
                "第五部：积分、累积与数值求积",
                "第 18 章：原函数与积分方法",
            ],
            REQUIRED_NAVIGATION_MARKERS[page],
        )

    def test_checks_chapter_nineteen_equivalence_page(self) -> None:
        page = "chapters/chapter-19/u-05-19-02-riemann-darboux-equivalence/index.html"
        self.assertIn(page, REQUIRED_RENDERED_ANCHORS)
        self.assertIn(page, REQUIRED_NAVIGATION_MARKERS)
        self.assertEqual(
            [
                "thm-u-05-19-02-darboux-criterion",
                "lem-u-05-19-02-common-refinement-control",
                "thm-u-05-19-02-riemann-darboux-equivalence",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )
        self.assertEqual(
            [
                "md-sidebar",
                "第五部：积分、累积与数值求积",
                "第 19 章：Riemann 积分与可积性",
            ],
            REQUIRED_NAVIGATION_MARKERS[page],
        )

    def test_checks_chapter_nineteen_integral_properties_page(self) -> None:
        page = "chapters/chapter-19/u-05-19-04-integral-properties/index.html"
        self.assertIn(page, REQUIRED_RENDERED_ANCHORS)
        self.assertIn(page, REQUIRED_NAVIGATION_MARKERS)
        self.assertEqual(
            [
                "thm-u-05-19-04-algebra-closure",
                "thm-u-05-19-04-order-bounds",
                "thm-u-05-19-04-interval-additivity",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )
        self.assertEqual(
            [
                "md-sidebar",
                "第五部：积分、累积与数值求积",
                "第 19 章：Riemann 积分与可积性",
            ],
            REQUIRED_NAVIGATION_MARKERS[page],
        )

    def test_checks_chapter_twenty_ftc_page(self) -> None:
        page = "chapters/chapter-20/u-05-20-02-fundamental-theorem-part-one/index.html"
        self.assertEqual(
            [
                "lem-u-05-20-02-local-average-control",
                "thm-u-05-20-02-ftc-part-one-pointwise",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )
        self.assertEqual(
            [
                "md-sidebar",
                "第五部：积分、累积与数值求积",
                "第 20 章：微积分基本定理",
            ],
            REQUIRED_NAVIGATION_MARKERS[page],
        )

    def test_checks_chapter_twenty_newton_leibniz_page(self) -> None:
        page = "chapters/chapter-20/u-05-20-03-newton-leibniz/index.html"
        self.assertEqual(
            [
                "thm-u-05-20-03-newton-leibniz-continuous",
                "thm-u-05-20-03-newton-leibniz-integrable-derivative",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )
        self.assertEqual(
            [
                "md-sidebar",
                "第五部：积分、累积与数值求积",
                "第 20 章：微积分基本定理",
            ],
            REQUIRED_NAVIGATION_MARKERS[page],
        )

    def test_checks_chapter_twenty_practice_page(self) -> None:
        page = "chapters/chapter-20/u-05-20-05-definite-integral-practice/index.html"
        self.assertEqual(
            [
                "tbl-u-05-20-05-method-selection",
                "thm-u-05-20-05-reflection-symmetry",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )
        self.assertEqual(
            [
                "md-sidebar",
                "第五部：积分、累积与数值求积",
                "第 20 章：微积分基本定理",
            ],
            REQUIRED_NAVIGATION_MARKERS[page],
        )

    def test_checks_chapter_twenty_one_volume_page(self) -> None:
        page = "chapters/chapter-21/u-05-21-02-volume-models/index.html"
        self.assertEqual(
            [
                "lem-u-05-21-02-shell-remainder",
                "thm-u-05-21-02-shell-volume",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )
        self.assertEqual(
            [
                "md-sidebar",
                "第五部：积分、累积与数值求积",
                "第 21 章：积分的几何与物理模型",
            ],
            REQUIRED_NAVIGATION_MARKERS[page],
        )

    def test_checks_chapter_twenty_one_arc_length_page(self) -> None:
        page = "chapters/chapter-21/u-05-21-03-arc-length/index.html"
        self.assertEqual(
            [
                "def-u-05-21-03-graph-arc-length",
                "thm-u-05-21-03-c1-graph-arc-length",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )
        self.assertEqual(
            [
                "md-sidebar",
                "第五部：积分、累积与数值求积",
                "第 21 章：积分的几何与物理模型",
            ],
            REQUIRED_NAVIGATION_MARKERS[page],
        )

    def test_checks_chapter_twenty_one_practice_page(self) -> None:
        page = "chapters/chapter-21/u-05-21-05-modeling-practice/index.html"
        self.assertEqual(
            [
                "alg-u-05-21-05-modeling-workflow",
                "tbl-u-05-21-05-model-selection",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )
        self.assertEqual(
            [
                "md-sidebar",
                "第五部：积分、累积与数值求积",
                "第 21 章：积分的几何与物理模型",
            ],
            REQUIRED_NAVIGATION_MARKERS[page],
        )

    def test_checks_chapter_twenty_two_definition_page(self) -> None:
        page = "chapters/chapter-22/u-05-22-01-improper-definition/index.html"
        self.assertEqual(
            [
                "def-u-05-22-01-infinite-interval-improper-integral",
                "thm-u-05-22-01-cauchy-tail-criterion",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )
        self.assertEqual(
            [
                "md-sidebar",
                "第五部：积分、累积与数值求积",
                "第 22 章：反常积分与数值求积",
            ],
            REQUIRED_NAVIGATION_MARKERS[page],
        )

    def test_checks_chapter_twenty_two_simpson_page(self) -> None:
        page = "chapters/chapter-22/u-05-22-05-simpson-certificates/index.html"
        self.assertEqual(
            [
                "thm-u-05-22-05-simpson-error",
                "alg-u-05-22-05-certified-simpson-budget",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )
        self.assertEqual(
            [
                "md-sidebar",
                "第五部：积分、累积与数值求积",
                "第 22 章：反常积分与数值求积",
            ],
            REQUIRED_NAVIGATION_MARKERS[page],
        )

    def test_checks_chapter_twenty_two_total_error_page(self) -> None:
        page = (
            "chapters/chapter-22/"
            "u-05-22-06-certified-improper-quadrature/index.html"
        )
        self.assertEqual(
            [
                "alg-u-05-22-06-total-error-workflow",
                "thm-u-05-22-06-total-error-certificate",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )
        self.assertEqual(
            [
                "md-sidebar",
                "第五部：积分、累积与数值求积",
                "第 22 章：反常积分与数值求积",
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
