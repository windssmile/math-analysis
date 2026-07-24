from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ZensicalStructureTests(unittest.TestCase):
    def test_zensical_shell_declares_the_content_site_contract(self) -> None:
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")

        self.assertEqual(requirements.strip(), "zensical==0.0.51")
        for marker in (
            "docs_dir: content",
            "site_dir: site",
            "strict: true",
            "variant: modern",
        ):
            with self.subTest(config_marker=marker):
                self.assertIn(marker, config)
        for marker in ("zensical build --strict", "zensical serve"):
            with self.subTest(make_marker=marker):
                self.assertIn(marker, makefile)
        self.assertNotIn("mkdocs build", makefile)
        self.assertNotIn("mkdocs serve", makefile)


if __name__ == "__main__":
    unittest.main()
