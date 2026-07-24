import unittest

from scripts.migrate_quarto_to_mkdocs import convert_markdown, metadata_from_unit


class QuartoMigrationTests(unittest.TestCase):
    def test_maps_registry_metadata_into_one_page_front_matter(self) -> None:
        metadata = metadata_from_unit(
            {
                "id": "u-01-04-02",
                "title": "区间怎样把目标逐步夹住？",
                "theory_hours": 1.25,
                "applied_hours": 1.0,
                "difficulty": 3,
                "book_prerequisites": ["chapter-03"],
                "higher_algebra_prerequisites": ["不等式"],
                "analytic_geometry_prerequisites": [],
                "python_prerequisites": ["while 循环"],
                "capabilities": ["proof", "numerical_algorithm"],
                "learning_goals": ["给出二分法误差界"],
                "content_standard": 2,
            }
        )
        self.assertEqual(metadata["unit_id"], "u-01-04-02")
        self.assertEqual(metadata["hours"], {"theory": 1.25, "applied": 1.0})
        self.assertEqual(metadata["prerequisites"]["python"], ["while 循环"])
        self.assertEqual(metadata["learning_goals"], ["给出二分法误差界"])

    def test_converts_supported_quarto_surface_syntax_without_losing_anchors(self) -> None:
        source = """# 单元标题 {.unnumbered #u-01-01-01}

见[下一页](next.qmd#u-01-01-02)。
见[课程地图](../../curriculum-map.qmd#chapter-01)。

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
        self.assertIn("[课程地图](../../course-map.md#chapter-01)", converted)
        self.assertIn('??? note "答案"', converted)
        self.assertIn("    结论。", converted)
        self.assertIn("!!! note", converted)
        self.assertIn("### 定义 {#def-u-01-01-01-set}", converted)
        self.assertNotIn(".unnumbered", converted)
        self.assertNotIn("## 答案", converted)


if __name__ == "__main__":
    unittest.main()
