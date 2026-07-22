from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_site import REQUIRED_RENDERED_ANCHORS, validate_site


class SiteValidationTest(unittest.TestCase):
    def test_valid_minimal_site(self) -> None:
        with TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "index.html").write_text('<a href="unit.html">unit</a>', encoding="utf-8")
            (site / "unit.html").write_text('<div id="u-03-12-01">二分法</div>', encoding="utf-8")
            self.assertEqual([], validate_site(site))

    def test_broken_internal_link_is_reported(self) -> None:
        with TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "index.html").write_text('<a href="missing.html">missing</a>', encoding="utf-8")
            errors = validate_site(site)
            self.assertEqual(["index.html links to missing missing.html"], errors)

    def test_registered_page_must_exist_in_rendered_site(self) -> None:
        with TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "index.html").write_text("book", encoding="utf-8")
            self.assertEqual(
                [
                    "rendered site is missing registered unit page: "
                    "book/part-01/chapter-01/u-01-01-01-sets.html"
                ],
                validate_site(
                    site,
                    expected_pages=[
                        "book/part-01/chapter-01/u-01-01-01-sets.html"
                    ],
                ),
            )

    def test_automatic_chapter_number_is_reported(self) -> None:
        with TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "index.html").write_text("book", encoding="utf-8")
            page = site / "unit.html"
            page.write_text(
                '<h1><span class="chapter-number">17</span> Unit</h1>',
                encoding="utf-8",
            )
            self.assertEqual(
                ["rendered unit page unit.html contains automatic chapter numbering"],
                validate_site(site, expected_pages=["unit.html"]),
            )

    def test_automatic_heading_number_is_reported(self) -> None:
        with TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "index.html").write_text("book", encoding="utf-8")
            page = site / "unit.html"
            page.write_text(
                '<h2><span class="header-section-number">17.1</span> Goal</h2>',
                encoding="utf-8",
            )
            self.assertEqual(
                ["rendered unit page unit.html contains automatic heading numbering"],
                validate_site(site, expected_pages=["unit.html"]),
            )

    def test_required_rendered_anchor_must_exist_on_its_page(self) -> None:
        with TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "index.html").write_text("book", encoding="utf-8")
            page = site / "book" / "cut.html"
            page.parent.mkdir()
            page.write_text('<section id="wrong-anchor">cut</section>', encoding="utf-8")
            self.assertEqual(
                [
                    "rendered site page book/cut.html is missing required anchor: "
                    "def-u-01-02-02-dedekind-cut"
                ],
                validate_site(
                    site,
                    expected_anchors={
                        "book/cut.html": ["def-u-01-02-02-dedekind-cut"]
                    },
                ),
            )

    def test_interval_bisection_rendered_anchors_are_required(self) -> None:
        page = "book/part-01/chapter-04/u-01-04-02-interval-bisection.html"
        self.assertEqual(
            [
                "def-u-01-04-02-interval-bisection",
                "ex-u-01-04-02-sqrt2-certificate",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )

    def test_approximation_error_rendered_anchors_are_required(self) -> None:
        page = "book/part-01/chapter-04/u-01-04-03-approximation-error.html"
        self.assertEqual(
            [
                "def-u-01-04-03-error-guarantee",
                "thm-u-01-04-03-bisection-step-count",
                "ex-u-01-04-03-bisection-step-count",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )

    def test_failure_of_infinite_approximation_rendered_anchors_are_required(self) -> None:
        page = "book/part-01/chapter-04/u-01-04-04-failure-of-infinite-approximation.html"
        self.assertEqual(
            [
                "def-u-01-04-04-uncertified-approximation",
                "ex-u-01-04-04-small-residual",
                "ex-u-01-04-04-false-bisection",
            ],
            REQUIRED_RENDERED_ANCHORS[page],
        )

    def test_part_three_rendered_anchors_are_required(self) -> None:
        self.assertEqual(
            ["def-u-03-09-02-function-limit"],
            REQUIRED_RENDERED_ANCHORS[
                "book/part-03/chapter-09/u-03-09-02-epsilon-delta-limit.html"
            ],
        )
        self.assertEqual(
            ["thm-u-03-09-04-sequential-criterion"],
            REQUIRED_RENDERED_ANCHORS[
                "book/part-03/chapter-09/u-03-09-04-sequential-function-limits.html"
            ],
        )

    def test_part_two_rendered_anchors_are_required(self) -> None:
        expected = {
            "book/part-02/chapter-08/u-02-08-03-cauchy-criterion.html": [
                "thm-u-02-08-03-criterion"
            ],
            "book/part-02/chapter-08/u-02-08-04-contraction-mapping.html": [
                "thm-u-02-08-04-contraction"
            ],
            "book/part-02/chapter-08/u-02-08-05-limsup-liminf.html": [
                "def-u-02-08-05-tail-bounds"
            ],
            "book/part-02/chapter-08/u-02-08-08-limsup-subsequences.html": [
                "thm-u-02-08-08-convergence"
            ],
        }
        for page, anchors in expected.items():
            with self.subTest(page=page):
                self.assertEqual(anchors, REQUIRED_RENDERED_ANCHORS[page])


if __name__ == "__main__":
    unittest.main()
