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


if __name__ == "__main__":
    unittest.main()
