"""Tests for the generated curriculum map."""

from __future__ import annotations

import tomllib
import unittest
from pathlib import Path

from scripts.render_curriculum_map import render_map


ROOT = Path(__file__).resolve().parents[1]
OUTLINE = ROOT / "curriculum" / "outline.toml"
MAP = ROOT / "book" / "curriculum-map.qmd"


class CurriculumMapTests(unittest.TestCase):
    def test_renders_the_confirmed_course_structure(self) -> None:
        with OUTLINE.open("rb") as handle:
            rendered = render_map(tomllib.load(handle))

        self.assertEqual(rendered.count("## 第"), 12)
        self.assertIn("1. [函数、集合与数学陈述]{#chapter-01}", rendered)
        self.assertIn(
            "54. [周期模型、逼近误差与 Gibbs 现象]{#chapter-54}",
            rendered,
        )
        self.assertIn("**学时：** 理论 270 + 应用 90 = 360", rendered)
        self.assertEqual(rendered.count("]{#chapter-"), 54)
        self.assertIn(
            "10. [连续函数与连续运算]{#chapter-10}",
            rendered,
        )
        self.assertIn(
            "11. [闭区间上的整体性质]{#chapter-11}",
            rendered,
        )

        self.assertEqual(MAP.read_text(encoding="utf-8"), rendered)


if __name__ == "__main__":
    unittest.main()
