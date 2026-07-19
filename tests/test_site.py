from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_site import validate_site


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


if __name__ == "__main__":
    unittest.main()
