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

    def test_readme_uses_zensical_commands_and_current_release_scope(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("第六部第 27 章，共 125 个学习单元", readme)
        self.assertIn("第九部第 41 章，共 189 个学习单元、337 学时", readme)
        self.assertIn("zensical serve", readme)
        self.assertIn("zensical build --strict", readme)
        self.assertNotIn("mkdocs serve", readme)
        self.assertNotIn("mkdocs build", readme)


if __name__ == "__main__":
    unittest.main()
