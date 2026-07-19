"""Contract tests for the machine-readable course outline."""

from __future__ import annotations

import copy
import unittest
from pathlib import Path

from scripts.check_outline import load_outline, validate_outline


ROOT = Path(__file__).resolve().parents[1]
OUTLINE = ROOT / "curriculum" / "outline.toml"


class OutlineValidationTests(unittest.TestCase):
    def load_outline(self) -> dict:
        return load_outline(OUTLINE)

    def test_real_outline_is_valid(self) -> None:
        self.assertEqual(validate_outline(self.load_outline()), [])

    def test_rejects_non_sequential_chapter_numbers(self) -> None:
        data = copy.deepcopy(self.load_outline())
        data["parts"][1]["chapters"][0]["number"] = 1
        self.assertIn(
            "chapter numbers must be exactly 1..54",
            validate_outline(data),
        )

    def test_rejects_incorrect_theory_hour_total(self) -> None:
        data = copy.deepcopy(self.load_outline())
        data["parts"][0]["theory_hours"] = 21
        self.assertIn(
            "theory hours must total 270, got 271",
            validate_outline(data),
        )

    def test_rejects_missing_guiding_question(self) -> None:
        data = copy.deepcopy(self.load_outline())
        data["parts"][0]["question"] = ""
        self.assertIn(
            "part-01 must have a guiding question",
            validate_outline(data),
        )

    def test_rejects_wrong_book_title(self) -> None:
        data = copy.deepcopy(self.load_outline())
        data["book"]["title"] = "数学分析"
        self.assertIn(
            "book.title must be exactly '数学分析：理论、算法与模型', got '数学分析'",
            validate_outline(data),
        )

    def test_rejects_changed_part_title(self) -> None:
        data = copy.deepcopy(self.load_outline())
        data["parts"][0]["title"] = "实数"
        self.assertIn(
            "part-01 title must be exactly '实数、函数与分析语言', got '实数'",
            validate_outline(data),
        )

    def test_rejects_changed_part_question(self) -> None:
        data = copy.deepcopy(self.load_outline())
        data["parts"][0]["question"] = "函数是什么？"
        self.assertIn(
            "part-01 question must be exactly '有限符号怎样描述无限与连续？', got '函数是什么？'",
            validate_outline(data),
        )

    def test_rejects_redistributed_part_hours(self) -> None:
        data = copy.deepcopy(self.load_outline())
        data["parts"][0]["theory_hours"] -= 1
        data["parts"][1]["theory_hours"] += 1
        errors = validate_outline(data)
        self.assertIn(
            "part-01 theory_hours must be exactly 20, got 19",
            errors,
        )
        self.assertIn(
            "part-02 theory_hours must be exactly 26, got 27",
            errors,
        )

    def test_rejects_changed_chapter_title(self) -> None:
        data = copy.deepcopy(self.load_outline())
        data["parts"][0]["chapters"][0]["title"] = "集合"
        self.assertIn(
            "chapter-01 title must be exactly '函数、集合与数学陈述', got '集合'",
            validate_outline(data),
        )

    def test_rejects_changed_chapter_id(self) -> None:
        data = copy.deepcopy(self.load_outline())
        data["parts"][0]["chapters"][0]["id"] = "chapter-x"
        self.assertIn(
            "chapter 1 ID must be exactly 'chapter-01', got 'chapter-x'",
            validate_outline(data),
        )

    def test_rejects_chapter_moved_to_another_part(self) -> None:
        data = copy.deepcopy(self.load_outline())
        chapter = data["parts"][1]["chapters"].pop(0)
        data["parts"][0]["chapters"].append(chapter)
        self.assertIn(
            "chapter-05 must belong to part-02, got part-01",
            validate_outline(data),
        )


if __name__ == "__main__":
    unittest.main()
