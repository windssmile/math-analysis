from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ThemeContractTests(unittest.TestCase):
    def test_material_reading_theme_has_its_required_contract(self) -> None:
        required = (
            "content/stylesheets/extra.css",
            "overrides/main.html",
            "overrides/partials/unit-meta.html",
        )
        missing = [path for path in required if not (ROOT / path).is_file()]
        self.assertEqual(missing, [])
        if missing:
            return

        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        css = (ROOT / "content/stylesheets/extra.css").read_text(encoding="utf-8")
        partial = (ROOT / "overrides/partials/unit-meta.html").read_text(
            encoding="utf-8"
        )

        for marker in ("custom_dir: overrides", "extra_css:"):
            with self.subTest(config_marker=marker):
                self.assertIn(marker, config)
        for marker in ("--md-primary-fg-color", ".unit-meta", "@media"):
            with self.subTest(css_marker=marker):
                self.assertIn(marker, css)
        for marker in ("page.meta.unit_id", "page.meta.hours", "page.meta.learning_goals"):
            with self.subTest(partial_marker=marker):
                self.assertIn(marker, partial)


if __name__ == "__main__":
    unittest.main()
