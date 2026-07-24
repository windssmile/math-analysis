from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.check_site import published_page_paths, validate_site


class MkDocsSiteValidationTests(unittest.TestCase):
    def test_verify_target_runs_the_mkdocs_site_checker(self) -> None:
        makefile = (Path(__file__).resolve().parents[1] / "Makefile").read_text(
            encoding="utf-8"
        )
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


if __name__ == "__main__":
    unittest.main()
