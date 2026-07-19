"""Contract tests for the learning-unit registry."""

from __future__ import annotations

import copy
from pathlib import Path
import tempfile
import tomllib
import unittest

from scripts.check_units import validate_units


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"
OUTLINE = ROOT / "curriculum" / "outline.toml"
UNIT_ID = "u-03-12-01"
CONTENT_PATH = "book/part-03/chapter-12/u-03-12-01-ivt-bisection.qmd"
BRIDGE_PATH = "book/bridges/python/functions-loops.qmd"
VALID_CONTENT = "\n".join(
    [
        f"# 介值定理与二分法 {{#{UNIT_ID}}}",
        "",
        "## 先备知识",
        "## 学习目标",
        "## 牵引问题",
        "## 探索与猜想",
        "## 概念与理论",
        "## 例题与迁移",
        "## 即时检验与回望",
        "## 习题与答案",
        "",
    ]
)


class UnitValidationTests(unittest.TestCase):
    def load_registry(self) -> dict:
        with UNITS.open("rb") as handle:
            return tomllib.load(handle)

    def load_outline(self) -> dict:
        with OUTLINE.open("rb") as handle:
            return tomllib.load(handle)

    def validate(self, data: object) -> list[str]:
        return validate_units(data, self.load_outline(), root=ROOT)

    def validate_with_content(
        self, data: object, content: str = VALID_CONTENT
    ) -> list[str]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            if isinstance(data, dict) and isinstance(data.get("units"), list):
                for unit in data["units"]:
                    if not isinstance(unit, dict) or not isinstance(unit.get("path"), str):
                        continue
                    unit_path = unit["path"]
                    content_path = root / unit_path
                    content_path.parent.mkdir(parents=True, exist_ok=True)
                    unit_id = unit.get("id", "placeholder")
                    if unit_path == CONTENT_PATH:
                        unit_content = content
                    else:
                        unit_content = "\n".join(
                            [
                                f"# 占位单元 {{#{unit_id}}}",
                                "",
                                "## 先备知识",
                                "## 学习目标",
                                "## 牵引问题",
                                "## 探索与猜想",
                                "## 概念与理论",
                                "## 例题与迁移",
                                "## 即时检验与回望",
                                "## 习题与答案",
                                "",
                            ]
                        )
                    content_path.write_text(unit_content, encoding="utf-8")
            bridge_path = root / BRIDGE_PATH
            bridge_path.parent.mkdir(parents=True)
            bridge_path.write_text("# Python 知识桥\n", encoding="utf-8")
            return validate_units(data, self.load_outline(), root=root)

    def test_real_registry_is_valid(self) -> None:
        self.assertEqual(self.validate(self.load_registry()), [])

    def test_rejects_unknown_chapter(self) -> None:
        data = copy.deepcopy(self.load_registry())
        data["units"][0]["chapter_id"] = "chapter-99"
        self.assertIn(
            f"{UNIT_ID} references unknown chapter chapter-99",
            self.validate(data),
        )

    def test_rejects_unknown_book_prerequisite_chapter(self) -> None:
        data = copy.deepcopy(self.load_registry())
        data["units"][0]["book_prerequisites"] = ["chapter-99"]
        self.assertIn(
            f"{UNIT_ID}.book_prerequisites[0] references unknown chapter chapter-99",
            self.validate_with_content(data),
        )

    def test_rejects_missing_required_list(self) -> None:
        data = copy.deepcopy(self.load_registry())
        del data["units"][0]["analytic_geometry_prerequisites"]
        self.assertIn(
            f"{UNIT_ID}.analytic_geometry_prerequisites must be a list",
            self.validate(data),
        )

    def test_rejects_more_than_two_and_a_half_combined_hours(self) -> None:
        data = copy.deepcopy(self.load_registry())
        data["units"][0]["theory_hours"] = 2
        data["units"][0]["applied_hours"] = 0.75
        self.assertIn(
            f"{UNIT_ID} theory_hours + applied_hours must be > 0 and <= 2.5, got 2.75",
            self.validate(data),
        )

    def test_rejects_non_finite_hours(self) -> None:
        for field in ("theory_hours", "applied_hours"):
            for value in (float("nan"), float("inf"), float("-inf")):
                with self.subTest(field=field, value=value):
                    data = copy.deepcopy(self.load_registry())
                    data["units"][0][field] = value
                    self.assertIn(
                        f"{UNIT_ID}.{field} must be a finite number",
                        self.validate(data),
                    )

    def test_accepts_combined_hours_of_two_and_a_quarter(self) -> None:
        data = copy.deepcopy(self.load_registry())
        data["units"][0]["theory_hours"] = 2
        data["units"][0]["applied_hours"] = 0.25
        self.assertEqual(self.validate_with_content(data), [])

    def test_rejects_negative_hour_component_even_when_total_is_valid(self) -> None:
        data = copy.deepcopy(self.load_registry())
        data["units"][0]["theory_hours"] = -1
        data["units"][0]["applied_hours"] = 2
        self.assertIn(
            f"{UNIT_ID}.theory_hours must be >= 0",
            self.validate_with_content(data),
        )

    def test_extremely_large_integer_hours_do_not_crash_validation(self) -> None:
        data = copy.deepcopy(self.load_registry())
        data["units"][0]["theory_hours"] = 10**10000
        errors = self.validate_with_content(data)
        self.assertTrue(
            any(
                error.startswith(
                    f"{UNIT_ID} theory_hours and applied_hours must each be <= 2"
                )
                for error in errors
            )
        )

    def test_rejects_anchor_that_only_appears_in_prose_or_code(self) -> None:
        content = VALID_CONTENT.replace(
            f"# 介值定理与二分法 {{#{UNIT_ID}}}",
            "\n".join(
                [
                    "# 介值定理与二分法",
                    f"正文中提到 {{#{UNIT_ID}}} 不算稳定锚点。",
                    "```markdown",
                    f"# 伪标题 {{#{UNIT_ID}}}",
                    "```",
                ]
            ),
        )
        self.assertIn(
            f"{UNIT_ID} content file first level-one heading must contain stable anchor "
            f"{{#{UNIT_ID}}}",
            self.validate_with_content(self.load_registry(), content),
        )

    def test_rejects_required_heading_that_only_appears_in_code(self) -> None:
        content = VALID_CONTENT.replace(
            "## 探索与猜想",
            "```markdown\n## 探索与猜想\n```",
        )
        self.assertIn(
            f"{UNIT_ID} content file is missing heading: ## 探索与猜想",
            self.validate_with_content(self.load_registry(), content),
        )

    def test_rejects_absolute_or_traversing_repository_paths(self) -> None:
        cases = (
            ("path", "/tmp/outside.qmd"),
            ("knowledge_bridges", ["../outside.qmd"]),
        )
        for field, value in cases:
            with self.subTest(field=field):
                data = copy.deepcopy(self.load_registry())
                data["units"][0][field] = value
                errors = self.validate_with_content(data)
                path_label = (
                    f"{UNIT_ID}.{field}"
                    if field == "path"
                    else f"{UNIT_ID}.{field}[0]"
                )
                self.assertIn(
                    f"{path_label} must be a normalized repository-relative path",
                    errors,
                )

    def test_rejects_non_mapping_registry_without_crashing(self) -> None:
        self.assertEqual(self.validate("not a registry"), ["registry must be a mapping"])

    def test_rejects_non_list_units_without_crashing(self) -> None:
        data = {"schema_version": 1, "units": "not a list"}
        self.assertIn("units must be a list", self.validate(data))

    def test_rejects_non_mapping_unit_without_crashing(self) -> None:
        data = {"schema_version": 1, "units": ["not a unit"]}
        self.assertIn("units[0] must be a mapping", self.validate(data))

    def test_rejects_boolean_hours_as_non_numeric(self) -> None:
        data = copy.deepcopy(self.load_registry())
        data["units"][0]["theory_hours"] = True
        self.assertIn(
            f"{UNIT_ID}.theory_hours must be a number",
            self.validate(data),
        )

    def test_rejects_boolean_difficulty_as_non_integer(self) -> None:
        data = copy.deepcopy(self.load_registry())
        data["units"][0]["difficulty"] = True
        self.assertIn(
            f"{UNIT_ID}.difficulty must be a positive integer",
            self.validate(data),
        )

    def test_rejects_invalid_required_list_type(self) -> None:
        data = copy.deepcopy(self.load_registry())
        data["units"][0]["capabilities"] = "proof"
        self.assertIn(
            f"{UNIT_ID}.capabilities must be a list",
            self.validate(data),
        )

    def test_rejects_unknown_capability(self) -> None:
        data = copy.deepcopy(self.load_registry())
        data["units"][0]["capabilities"] = ["proof", "symbolic_magic"]
        self.assertIn(
            f"{UNIT_ID}.capabilities contains unsupported capability symbolic_magic",
            self.validate(data),
        )

    def test_rejects_boolean_schema_version(self) -> None:
        data = copy.deepcopy(self.load_registry())
        data["schema_version"] = True
        self.assertIn("schema_version must be the integer 1", self.validate(data))


if __name__ == "__main__":
    unittest.main()
