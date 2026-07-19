"""Tests for the generated curriculum map."""

from __future__ import annotations

import tomllib
import unittest
from pathlib import Path

from scripts.render_curriculum_map import render_map


ROOT = Path(__file__).resolve().parents[1]
OUTLINE = ROOT / "curriculum" / "outline.toml"


class CurriculumMapTests(unittest.TestCase):
    def test_renders_the_confirmed_course_structure(self) -> None:
        with OUTLINE.open("rb") as handle:
            rendered = render_map(tomllib.load(handle))

        self.assertEqual(rendered.count("## 第"), 12)
        self.assertIn("1. 函数、集合与数学陈述", rendered)
        self.assertIn("54. 周期模型、逼近误差与 Gibbs 现象", rendered)
        self.assertIn("**学时：** 理论 270 + 应用 90 = 360", rendered)


if __name__ == "__main__":
    unittest.main()
