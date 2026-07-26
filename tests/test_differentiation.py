"""Behavioral tests for finite Taylor and differentiation examples."""

from math import e, inf, isclose, nan
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mathbook_examples.differentiation import evaluate_taylor


class TaylorEvaluationTest(unittest.TestCase):
    def test_evaluates_constant_and_ascending_power_coefficients(self) -> None:
        self.assertEqual(3.5, evaluate_taylor([3.5], 2.0, -7.0))
        self.assertEqual(17.0, evaluate_taylor([1.0, 2.0, 3.0], 0.0, 2.0))

    def test_evaluates_about_a_nonzero_center(self) -> None:
        self.assertEqual(3.0, evaluate_taylor([1.0, -2.0, 4.0], 2.0, 3.0))

    def test_uses_coefficients_that_already_include_factorials(self) -> None:
        approximation = evaluate_taylor([1.0, 1.0, 0.5, 1 / 6], 0.0, 1.0)
        self.assertTrue(isclose(approximation, 8 / 3, rel_tol=0.0, abs_tol=1e-15))
        self.assertLess(abs(approximation - e), 0.052)

    def test_rejects_empty_or_nonfinite_coefficients(self) -> None:
        with self.assertRaisesRegex(ValueError, "^coefficients must not be empty$"):
            evaluate_taylor([], 0.0, 1.0)
        for coefficient in (nan, inf, -inf):
            with self.subTest(coefficient=coefficient):
                with self.assertRaisesRegex(ValueError, "^coefficient 1 must be finite$"):
                    evaluate_taylor([1.0, coefficient], 0.0, 1.0)

    def test_rejects_nonfinite_center_and_point(self) -> None:
        for center in (nan, inf, -inf):
            with self.subTest(center=center):
                with self.assertRaisesRegex(ValueError, "^center must be finite$"):
                    evaluate_taylor([1.0], center, 0.0)
        for point in (nan, inf, -inf):
            with self.subTest(point=point):
                with self.assertRaisesRegex(ValueError, "^point must be finite$"):
                    evaluate_taylor([1.0], 0.0, point)

    def test_rejects_nonfinite_horner_intermediate(self) -> None:
        with self.assertRaisesRegex(ValueError, "^Taylor evaluation must remain finite$"):
            evaluate_taylor([1e308, 1e308], 0.0, 2.0)


if __name__ == "__main__":
    unittest.main()
