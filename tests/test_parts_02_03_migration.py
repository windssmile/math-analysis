from pathlib import Path
import re
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "chapters"

EXPECTED_UNIT_PAGES = [
    "chapter-05/u-02-05-01-sequences.md",
    "chapter-05/u-02-05-02-epsilon-n.md",
    "chapter-05/u-02-05-03-divergence-infinity.md",
    "chapter-05/u-02-05-04-iteration-evidence.md",
    "chapter-05/u-02-05-05-limit-consequences.md",
    "chapter-06/u-02-06-01-limit-laws.md",
    "chapter-06/u-02-06-02-order-squeeze.md",
    "chapter-06/u-02-06-03-error-propagation.md",
    "chapter-06/u-02-06-04-reciprocal-quotient.md",
    "chapter-07/u-02-07-01-monotone-sequences.md",
    "chapter-07/u-02-07-02-recursive-invariants.md",
    "chapter-07/u-02-07-03-nested-intervals.md",
    "chapter-07/u-02-07-04-completeness-criteria.md",
    "chapter-08/u-02-08-01-subsequences.md",
    "chapter-08/u-02-08-02-bolzano-weierstrass.md",
    "chapter-08/u-02-08-03-cauchy-criterion.md",
    "chapter-08/u-02-08-04-contraction-mapping.md",
    "chapter-08/u-02-08-05-limsup-liminf.md",
    "chapter-08/u-02-08-06-fixed-point-certificates.md",
    "chapter-08/u-02-08-07-iteration-lab.md",
    "chapter-08/u-02-08-08-limsup-subsequences.md",
    "chapter-09/u-03-09-01-local-neighborhoods.md",
    "chapter-09/u-03-09-02-epsilon-delta-limit.md",
    "chapter-09/u-03-09-03-function-limit-laws.md",
    "chapter-09/u-03-09-04-sequential-function-limits.md",
    "chapter-09/u-03-09-05-epsilon-delta-workshop.md",
    "chapter-09/u-03-09-06-one-sided-limits.md",
    "chapter-09/u-03-09-07-infinite-limits-at-point.md",
    "chapter-09/u-03-09-08-limits-at-infinity.md",
    "chapter-10/u-03-10-01-epsilon-delta-continuity.md",
    "chapter-10/u-03-10-02-continuous-operations.md",
    "chapter-10/u-03-10-03-discontinuities-elementary-functions.md",
    "chapter-11/u-03-11-01-compact-intervals.md",
    "chapter-11/u-03-11-02-extreme-value-theorem.md",
    "chapter-11/u-03-11-03-uniform-continuity.md",
    "chapter-12/u-03-12-01-intermediate-value-theorem.md",
    "chapter-12/u-03-12-02-certified-bisection.md",
    "chapter-12/u-03-12-03-fixed-points-and-iteration.md",
]

REPRESENTATIVE_ANCHORS = {
    "chapter-08/u-02-08-04-contraction-mapping.md": "thm-u-02-08-04-contraction",
    "chapter-08/u-02-08-03-cauchy-criterion.md": "thm-u-02-08-03-criterion",
    "chapter-08/u-02-08-05-limsup-liminf.md": "def-u-02-08-05-tail-bounds",
    "chapter-09/u-03-09-02-epsilon-delta-limit.md": "def-u-03-09-02-function-limit",
    "chapter-11/u-03-11-01-compact-intervals.md": "thm-u-03-11-01-heine-borel",
    "chapter-12/u-03-12-01-intermediate-value-theorem.md": "thm-u-03-12-01-intermediate-value",
    "chapter-12/u-03-12-02-certified-bisection.md": "alg-u-03-12-02-bisection",
}


class PartsTwoAndThreeMigrationTests(unittest.TestCase):
    def test_all_unit_pages_keep_their_page_local_ids_and_h1_anchors(self) -> None:
        self.assertEqual(38, len(EXPECTED_UNIT_PAGES))
        missing = [path for path in EXPECTED_UNIT_PAGES if not (CONTENT / path).is_file()]
        self.assertEqual([], missing)
        for relative_path in EXPECTED_UNIT_PAGES:
            with self.subTest(page=relative_path):
                text = (CONTENT / relative_path).read_text(encoding="utf-8")
                metadata = yaml.safe_load(text.split("---\n", 2)[1])
                self.assertRegex(metadata["unit_id"], r"^u-0[23]-")
                self.assertRegex(
                    text,
                    re.compile(rf"^# .+ \{{#{metadata['unit_id']}\}}$", re.MULTILINE),
                )

    def test_chapter_guides_and_representative_stable_anchors_are_present(self) -> None:
        for chapter in range(5, 13):
            self.assertTrue((CONTENT / f"chapter-{chapter:02d}" / "index.md").is_file())
        for relative_path, anchor in REPRESENTATIVE_ANCHORS.items():
            with self.subTest(page=relative_path):
                self.assertIn(anchor, (CONTENT / relative_path).read_text(encoding="utf-8"))

    def test_python_knowledge_bridge_links_back_to_the_units_that_use_it(self) -> None:
        bridge = (ROOT / "content" / "bridges" / "python-functions-loops.md").read_text(
            encoding="utf-8"
        )
        for link in (
            "../chapters/chapter-05/u-02-05-04-iteration-evidence.md",
            "../chapters/chapter-06/u-02-06-03-error-propagation.md",
            "../chapters/chapter-07/u-02-07-02-recursive-invariants.md",
        ):
            with self.subTest(link=link):
                self.assertIn(link, bridge)


if __name__ == "__main__":
    unittest.main()
