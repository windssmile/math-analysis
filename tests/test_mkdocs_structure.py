from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class MkDocsStructureTests(unittest.TestCase):
    def test_mkdocs_shell_declares_the_content_site_contract(self) -> None:
        required = (
            "requirements.txt",
            "mkdocs.yml",
            "content/index.md",
            "content/javascripts/mathjax.js",
        )
        missing = [path for path in required if not (ROOT / path).is_file()]
        self.assertEqual(missing, [])
        if missing:
            return

        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        for marker in (
            "docs_dir: content",
            "site_dir: site",
            "strict: true",
            "content.code.copy",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, config)


if __name__ == "__main__":
    unittest.main()
