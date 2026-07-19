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


if __name__ == "__main__":
    unittest.main()
