from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ProjectStructureTests(unittest.TestCase):
    def test_required_mkdocs_shell_files_exist(self):
        required_files = [
            "mkdocs.yml",
            "requirements.txt",
            "content/index.md",
            "Makefile",
        ]
        missing = [path for path in required_files if not (ROOT / path).is_file()]
        self.assertEqual(missing, [])

    def test_pages_workflow_builds_the_mkdocs_site_without_quarto(self) -> None:
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
        for marker in (
            "pip install --requirement requirements.txt",
            "make verify",
            "path: site",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, workflow)
        for removed_marker in (
            "quarto-dev/quarto-actions",
            "make render",
            "_site",
            "DENO_DIR",
        ):
            with self.subTest(removed_marker=removed_marker):
                self.assertNotIn(removed_marker, workflow)

    def test_parts_two_three_dependency_map_is_frozen(self) -> None:
        dependency_map = (
            ROOT / "docs/curriculum/parts-02-03-dependencies.md"
        ).read_text(encoding="utf-8")
        required_markers = (
            "supremum -> monotone",
            "monotone -> nested intervals",
            "nested intervals -> Bolzano-Weierstrass",
            "Bolzano-Weierstrass -> Cauchy",
            "Part II owns contraction convergence",
            "Part III owns continuous existence",
            "finite function limits -> continuity",
            "Bolzano-Weierstrass + closed interval -> sequential compactness",
            "continuity + sequential compactness -> boundedness/extreme value/uniform continuity",
            "continuity + nested intervals -> IVT",
            "IVT -> continuous self-map fixed point existence",
            "IVT/sign invariant + interval length -> bisection certificates",
            "IVT independent of extreme value and uniform continuity",
            "bisection error independent of compactness",
        )

        for marker in required_markers:
            with self.subTest(marker=marker):
                self.assertIn(marker, dependency_map)


if __name__ == "__main__":
    unittest.main()
