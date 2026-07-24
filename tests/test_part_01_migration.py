from pathlib import Path
import re
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]

PART_ONE_UNITS = {
    "chapter-01": (
        "u-01-01-01-sets.md",
        "u-01-01-02-quantifiers.md",
        "u-01-01-03-proofs.md",
        "u-01-01-04-functions.md",
    ),
    "chapter-02": (
        "u-01-02-01-rational-gaps.md",
        "u-01-02-02-dedekind-cuts.md",
        "u-01-02-03-cut-order-operations.md",
    ),
    "chapter-03": (
        "u-01-03-01-bounds.md",
        "u-01-03-02-supremum-principle.md",
        "u-01-03-03-completeness-consequences.md",
    ),
    "chapter-04": (
        "u-01-04-01-recurrence.md",
        "u-01-04-02-interval-bisection.md",
        "u-01-04-03-approximation-error.md",
        "u-01-04-04-failure-of-infinite-approximation.md",
    ),
}


class PartOneMigrationTests(unittest.TestCase):
    def test_all_part_one_units_have_page_local_metadata(self) -> None:
        for chapter, filenames in PART_ONE_UNITS.items():
            for filename in filenames:
                with self.subTest(chapter=chapter, filename=filename):
                    page = ROOT / "content/chapters" / chapter / filename
                    self.assertTrue(page.is_file())
                    text = page.read_text(encoding="utf-8")
                    front_matter, _ = text.split("---", 2)[1:]
                    metadata = yaml.safe_load(front_matter)
                    expected_id = re.match(r"(u-\d{2}-\d{2}-\d{2})-", filename)
                    self.assertIsNotNone(expected_id)
                    self.assertEqual(metadata["unit_id"], expected_id.group(1))
                    self.assertIn(f"{{#{metadata['unit_id']}}}", text)

    def test_navigation_lists_part_one_before_the_python_bridge(self) -> None:
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        first_part = config.index("第一部：实数、函数与分析语言")
        appendix = config.index("附录:")
        self.assertLess(first_part, appendix)
        for chapter in range(1, 5):
            self.assertIn(f"chapter-{chapter:02d}/index.md", config)


if __name__ == "__main__":
    unittest.main()
