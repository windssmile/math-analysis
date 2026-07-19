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


if __name__ == "__main__":
    unittest.main()
