from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ProjectStructureTests(unittest.TestCase):
    def test_required_book_shell_files_exist(self):
        required_files = [
            "_quarto.yml",
            "index.qmd",
            "styles.css",
            "book/preface.qmd",
            "Makefile",
        ]
        missing = [path for path in required_files if not (ROOT / path).is_file()]
        self.assertEqual(missing, [])

    def test_parts_two_three_dependency_map_is_frozen(self):
        dependency_map = (
            ROOT / "curriculum/parts-02-03-dependencies.md"
        ).read_text(encoding="utf-8")
        required_markers = [
            "supremum -> monotone",
            "monotone -> nested intervals",
            "nested intervals -> Bolzano-Weierstrass",
            "Bolzano-Weierstrass -> Cauchy",
            "Part II owns contraction convergence",
            "Part III owns continuous existence",
        ]

        for marker in required_markers:
            with self.subTest(marker=marker):
                self.assertIn(marker, dependency_map)


if __name__ == "__main__":
    unittest.main()
