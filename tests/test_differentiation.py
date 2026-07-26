"""Behavioral tests for finite Taylor and differentiation examples."""

from dataclasses import FrozenInstanceError
from math import e, exp, inf, isclose, nan, sqrt
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mathbook_examples.differentiation import (
    DifferenceEstimate,
    centered_difference,
    evaluate_taylor,
    forward_difference,
)


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


class DifferenceTest(unittest.TestCase):
    def test_returns_frozen_result_with_method_and_explicit_step(self) -> None:
        result = forward_difference(lambda x: x * x, 2.0, step=1e-5)
        self.assertIsInstance(result, DifferenceEstimate)
        self.assertEqual("forward", result.method)
        self.assertEqual(1e-5, result.step)
        self.assertLess(abs(result.value - 4.0), 2e-5)
        with self.assertRaisesRegex(FrozenInstanceError, "cannot assign to field"):
            result.value = 0.0  # type: ignore[misc]

    def test_centered_difference_is_accurate_for_a_smooth_function(self) -> None:
        result = centered_difference(exp, 0.0, step=1e-4)
        self.assertEqual("centered", result.method)
        self.assertLess(abs(result.value - 1.0), 2e-9)

    def test_result_has_no_certificate_fields(self) -> None:
        result = centered_difference(exp, 0.0)
        self.assertFalse(hasattr(result, "error_bound"))
        self.assertFalse(hasattr(result, "certified"))

    def test_automatic_steps_follow_the_documented_rules(self) -> None:
        scale = 3.0
        forward = forward_difference(lambda x: x * x, -scale)
        centered = centered_difference(lambda x: x * x, -scale)
        self.assertEqual(sqrt(sys.float_info.epsilon) * scale, forward.step)
        self.assertEqual(sys.float_info.epsilon ** (1 / 3) * scale, centered.step)
        self.assertEqual(sqrt(sys.float_info.epsilon), forward_difference(exp, 0.25).step)

    def test_documentation_calls_defaults_uncertified_heuristics(self) -> None:
        module_doc = sys.modules[forward_difference.__module__].__doc__ or ""
        for text in (
            module_doc,
            forward_difference.__doc__ or "",
            centered_difference.__doc__ or "",
        ):
            self.assertIn("heuristic", text)
            self.assertIn("not an error certificate", text)

    def test_rejects_nonfinite_point_and_invalid_explicit_step(self) -> None:
        for point in (nan, inf, -inf):
            with self.subTest(point=point):
                with self.assertRaisesRegex(ValueError, "^point must be finite$"):
                    forward_difference(exp, point)
        for step in (0.0, -1.0, nan, inf, -inf):
            with self.subTest(step=step):
                with self.assertRaisesRegex(
                    ValueError, "^step must be positive and finite$"
                ):
                    centered_difference(exp, 0.0, step=step)

    def test_rejects_nonfinite_sample_points_and_function_values(self) -> None:
        with self.assertRaisesRegex(ValueError, "^sample point must be finite$"):
            forward_difference(lambda x: x, 1e308, step=1e308)
        for output in (nan, inf, -inf):
            with self.subTest(output=output):
                with self.assertRaisesRegex(ValueError, "^function value must be finite$"):
                    centered_difference(lambda _x, value=output: value, 0.0)

    def test_preserves_function_domain_exceptions(self) -> None:
        def unavailable(_x: float) -> float:
            raise RuntimeError("domain unavailable")

        with self.assertRaisesRegex(RuntimeError, "^domain unavailable$"):
            forward_difference(unavailable, 0.0)


if __name__ == "__main__":
    unittest.main()
