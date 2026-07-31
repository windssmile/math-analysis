from dataclasses import FrozenInstanceError
import math
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mathbook_examples.multiple_integration import (
    Midpoint2DResult,
    tensor_midpoint_2d,
)


class TensorMidpointTests(unittest.TestCase):
    def test_constant_result_metadata_and_immutability(self) -> None:
        result = tensor_midpoint_2d(
            lambda x, y: 3.0,
            x_bounds=(0.0, 2.0),
            y_bounds=(-1.0, 1.0),
            nx=4,
            ny=5,
        )
        self.assertIsInstance(result, Midpoint2DResult)
        self.assertAlmostEqual(12.0, result.value)
        self.assertEqual((4, 5, 20), (result.nx, result.ny, result.evaluations))
        self.assertEqual(((0.0, 2.0), (-1.0, 1.0)), (result.x_bounds, result.y_bounds))
        with self.assertRaises(FrozenInstanceError):
            result.value = 0.0

    def test_is_exact_for_affine_and_separable_bilinear_functions(self) -> None:
        affine = tensor_midpoint_2d(
            lambda x, y: 2.0 * x - 3.0 * y + 4.0,
            x_bounds=(-1.0, 2.0),
            y_bounds=(1.0, 5.0),
            nx=3,
            ny=8,
        )
        self.assertAlmostEqual(-48.0, affine.value)
        bilinear = tensor_midpoint_2d(
            lambda x, y: x * y,
            x_bounds=(0.0, 2.0),
            y_bounds=(1.0, 3.0),
            nx=7,
            ny=9,
        )
        self.assertAlmostEqual(8.0, bilinear.value)

    def test_rejects_invalid_bounds_and_subdivisions(self) -> None:
        valid = dict(function=lambda x, y: 1.0, x_bounds=(0.0, 1.0), y_bounds=(0.0, 1.0), nx=2, ny=2)
        for field, value in (
            ("x_bounds", (1.0, 0.0)),
            ("x_bounds", (1.0, 1.0)),
            ("y_bounds", (1.0, 0.0)),
            ("y_bounds", (0.0, math.inf)),
            ("nx", 0),
            ("nx", -1),
            ("nx", True),
            ("ny", 2.5),
        ):
            arguments = valid | {field: value}
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                tensor_midpoint_2d(**arguments)

    def test_rejects_non_scalar_nonfinite_and_overflowing_values(self) -> None:
        common = dict(x_bounds=(0.0, 1.0), y_bounds=(0.0, 1.0), nx=2, ny=2)
        for function in (
            lambda x, y: (x, y),
            lambda x, y: math.nan,
            lambda x, y: math.inf,
        ):
            with self.subTest(function=function), self.assertRaises(ValueError):
                tensor_midpoint_2d(function, **common)
        with self.assertRaises(ValueError):
            tensor_midpoint_2d(
                lambda x, y: 1e308,
                x_bounds=(0.0, 1e308),
                y_bounds=(0.0, 2.0),
                nx=1,
                ny=1,
            )


if __name__ == "__main__":
    unittest.main()
