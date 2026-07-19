"""Contract tests for the learning-unit registry."""

from __future__ import annotations

import copy
from pathlib import Path
import tomllib
import unittest

from scripts.check_units import validate_units


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "curriculum" / "units.toml"
OUTLINE = ROOT / "curriculum" / "outline.toml"
UNIT_ID = "u-03-12-01"
CONTENT_PATH = "book/part-03/chapter-12/u-03-12-01-ivt-bisection.qmd"


class UnitValidationTests(unittest.TestCase):
    def load_registry(self) -> dict:
        with UNITS.open("rb") as handle:
            return tomllib.load(handle)

    def load_outline(self) -> dict:
        with OUTLINE.open("rb") as handle:
            return tomllib.load(handle)

    def validate(self, data: object) -> list[str]:
        return validate_units(data, self.load_outline(), root=ROOT)

    def test_real_registry_only_lacks_the_task_6_content_file(self) -> None:
        self.assertEqual(
            self.validate(self.load_registry()),
            [f"{UNIT_ID} content file does not exist: {CONTENT_PATH}"],
        )

    def test_rejects_unknown_chapter(self) -> None:
        data = copy.deepcopy(self.load_registry())
        data["units"][0]["chapter_id"] = "chapter-99"
        self.assertIn(
            f"{UNIT_ID} references unknown chapter chapter-99",
            self.validate(data),
        )

    def test_rejects_missing_required_list(self) -> None:
        data = copy.deepcopy(self.load_registry())
        del data["units"][0]["analytic_geometry_prerequisites"]
        self.assertIn(
            f"{UNIT_ID}.analytic_geometry_prerequisites must be a list",
            self.validate(data),
        )

    def test_rejects_more_than_two_combined_hours(self) -> None:
        data = copy.deepcopy(self.load_registry())
        data["units"][0]["applied_hours"] = 1
        self.assertIn(
            f"{UNIT_ID} theory_hours + applied_hours must be > 0 and <= 2, got 2.25",
            self.validate(data),
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
