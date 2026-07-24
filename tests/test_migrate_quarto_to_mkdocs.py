import unittest

from scripts.migrate_quarto_to_mkdocs import convert_markdown


class QuartoMigrationTests(unittest.TestCase):
    def test_converts_supported_quarto_surface_syntax_without_losing_anchors(self) -> None:
        source = """# 单元标题 {.unnumbered #u-01-01-01}

见[下一页](next.qmd#u-01-01-02)。

::: {.callout-note collapse=\"true\"}
## 答案

结论。
:::

::: {.callout-note}
提示。
:::

### 定义 {#def-u-01-01-01-set}
"""
        converted = convert_markdown(source)
        self.assertIn("# 单元标题 {#u-01-01-01}", converted)
        self.assertIn("[下一页](next.md#u-01-01-02)", converted)
        self.assertIn('??? note "答案"', converted)
        self.assertIn("    结论。", converted)
        self.assertIn("!!! note", converted)
        self.assertIn("### 定义 {#def-u-01-01-01-set}", converted)
        self.assertNotIn(".unnumbered", converted)
        self.assertNotIn("## 答案", converted)


if __name__ == "__main__":
    unittest.main()
