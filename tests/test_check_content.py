from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.check_content import validate_content


VALID_FRONT_MATTER = """---
title: 集合怎样组织数学对象？
unit_id: u-01-01-01
hours:
  theory: 1.5
  applied: 0.5
difficulty: 1
prerequisites:
  book: ["第 0 章导学"]
  higher_algebra: ["集合记号"]
  analytic_geometry: []
  python: []
capabilities: ["concepts", "proof"]
learning_goals: ["写出集合的基本关系"]
content_standard: 2
---
"""

VALID_BODY = """# 集合怎样组织数学对象？ {#u-01-01-01}

## 先备知识
## 学习目标
## 牵引问题
## 探索与猜想
## 概念与理论
### 例题 1 {#ex-u-01-01-01-01}
### 例题 2 {#ex-u-01-01-01-02}
## 例题与迁移
## 即时检验与回望
## 习题与答案
### 习题 1 {#pr-u-01-01-01-01}
### 习题 2 {#pr-u-01-01-01-02}
### 习题 3 {#pr-u-01-01-01-03}
### 习题 4 {#pr-u-01-01-01-04}
### 习题 5 {#pr-u-01-01-01-05}
??? note "答案"
    一
??? note "答案"
    二
??? note "答案"
    三
??? note "答案"
    四
??? note "答案"
    五
??? note "答案"
    六
??? note "答案"
    七
## 常见误区与后续
"""


class ContentValidationTests(unittest.TestCase):
    def write_unit(self, root: Path, *, front_matter: str = VALID_FRONT_MATTER, body: str = VALID_BODY) -> Path:
        page = root / "chapters/01-analysis-language/01-01-sets.md"
        page.parent.mkdir(parents=True)
        page.write_text(front_matter + "\n" + body, encoding="utf-8")
        return page

    def test_accepts_a_complete_v2_unit(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_unit(root)
            self.assertEqual(validate_content(root), [])

    def test_reports_missing_unit_metadata_and_invalid_hours(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            front_matter = VALID_FRONT_MATTER.replace("unit_id: u-01-01-01\n", "").replace(
                "applied: 0.5", "applied: 0.76"
            )
            self.write_unit(root, front_matter=front_matter)
            errors = validate_content(root)
            self.assertIn(
                "chapters/01-analysis-language/01-01-sets.md: unit_id must be a nonblank string",
                errors,
            )
            self.assertIn(
                "chapters/01-analysis-language/01-01-sets.md: hours total must be <= 2.25, got 2.26",
                errors,
            )

    def test_reports_missing_required_structure_and_v2_counts(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            body = VALID_BODY.replace("## 概念与理论\n", "").replace(
                "### 例题 2 {#ex-u-01-01-01-02}\n", ""
            )
            body = body.replace("### 习题 5 {#pr-u-01-01-01-05}\n", "")
            body = body.replace('??? note "答案"\n    七\n', "")
            self.write_unit(root, body=body)
            errors = validate_content(root)
            self.assertIn(
                "chapters/01-analysis-language/01-01-sets.md: missing heading: ## 概念与理论",
                errors,
            )
            self.assertIn(
                "chapters/01-analysis-language/01-01-sets.md: v2 content must contain at least 2 anchored examples",
                errors,
            )
            self.assertIn(
                "chapters/01-analysis-language/01-01-sets.md: v2 content must contain at least 5 anchored exercises",
                errors,
            )
            self.assertIn(
                "chapters/01-analysis-language/01-01-sets.md: v2 content must contain at least 7 collapsed answers",
                errors,
            )

    def test_reports_invalid_relative_markdown_link(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            body = VALID_BODY + "\n[不存在的页面](missing.md)\n"
            self.write_unit(root, body=body)
            self.assertIn(
                "chapters/01-analysis-language/01-01-sets.md: links to missing Markdown page: missing.md",
                validate_content(root),
            )


if __name__ == "__main__":
    unittest.main()
