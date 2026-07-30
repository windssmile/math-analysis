from dataclasses import FrozenInstanceError
from math import e, exp, inf, isclose, nan
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mathbook_examples.quadrature import (
    QuadratureEvaluationError,
    QuadratureResult,
    certified_simpson,
    composite_midpoint,
    composite_simpson,
    composite_trapezoid,
)


class FixedGridQuadratureTests(unittest.TestCase):
    def test_midpoint_and_trapezoid_return_frozen_fixed_grid_results(self) -> None:
        midpoint = composite_midpoint(lambda x: x * x, 0.0, 1.0, 8, 2.0)
        trapezoid = composite_trapezoid(lambda x: x * x, 0.0, 1.0, 8, 2.0)

        self.assertIsInstance(midpoint, QuadratureResult)
        self.assertEqual("midpoint", midpoint.method)
        self.assertEqual("trapezoid", trapezoid.method)
        self.assertEqual("fixed_grid", midpoint.status)
        self.assertIsNone(midpoint.target_tolerance)
        self.assertIsNone(midpoint.target_met)
        self.assertEqual(8, midpoint.subdivisions)
        self.assertEqual(8, midpoint.evaluations)
        self.assertEqual(9, trapezoid.evaluations)
        self.assertLessEqual(
            abs(midpoint.value - 1 / 3),
            midpoint.error_bound + 1e-15,
        )
        self.assertLessEqual(
            abs(trapezoid.value - 1 / 3),
            trapezoid.error_bound + 1e-15,
        )
        with self.assertRaisesRegex(FrozenInstanceError, "cannot assign to field"):
            midpoint.value = 0.0  # type: ignore[misc]

    def test_second_derivative_error_bounds_use_the_proved_constants(self) -> None:
        midpoint = composite_midpoint(lambda x: x * x, 0.0, 1.0, 4, 2.0)
        trapezoid = composite_trapezoid(lambda x: x * x, 0.0, 1.0, 4, 2.0)

        self.assertTrue(
            isclose(midpoint.error_bound, 1 / 192, rel_tol=0.0, abs_tol=1e-16)
        )
        self.assertTrue(
            isclose(trapezoid.error_bound, 1 / 96, rel_tol=0.0, abs_tol=1e-16)
        )

    def test_simpson_is_exact_for_a_cubic_and_requires_even_grid(self) -> None:
        result = composite_simpson(
            lambda x: x**3 - 2 * x + 1,
            -1.0,
            2.0,
            6,
            0.0,
        )

        self.assertTrue(isclose(result.value, 3.75, rel_tol=0.0, abs_tol=1e-14))
        self.assertEqual(0.0, result.error_bound)
        self.assertEqual(7, result.evaluations)
        with self.assertRaisesRegex(
            ValueError,
            "^subdivisions must be a positive even integer$",
        ):
            composite_simpson(lambda x: x, 0.0, 1.0, 3, 0.0)

    def test_simpson_error_bound_uses_the_fourth_derivative_formula(self) -> None:
        result = composite_simpson(lambda x: x**4, 0.0, 1.0, 4, 24.0)

        expected_bound = 24.0 / (180.0 * 4**4)
        self.assertTrue(
            isclose(result.error_bound, expected_bound, rel_tol=0.0, abs_tol=1e-18)
        )
        self.assertLessEqual(abs(result.value - 0.2), result.error_bound)

    def test_rejects_invalid_intervals_subdivisions_and_bounds(self) -> None:
        for left, right in ((nan, 1.0), (0.0, inf), (-inf, 1.0)):
            with self.subTest(left=left, right=right):
                with self.assertRaisesRegex(
                    ValueError,
                    "^endpoints must be finite$",
                ):
                    composite_midpoint(lambda x: x, left, right, 2, 0.0)

        for left, right in ((1.0, 1.0), (2.0, 1.0)):
            with self.subTest(left=left, right=right):
                with self.assertRaisesRegex(
                    ValueError,
                    "^left endpoint must be smaller than right endpoint$",
                ):
                    composite_trapezoid(lambda x: x, left, right, 2, 0.0)

        for subdivisions in (0, -1, 1.5, True):
            with self.subTest(subdivisions=subdivisions):
                with self.assertRaisesRegex(
                    ValueError,
                    "^subdivisions must be a positive integer$",
                ):
                    composite_midpoint(
                        lambda x: x,
                        0.0,
                        1.0,
                        subdivisions,  # type: ignore[arg-type]
                        0.0,
                    )

        for bound in (-1.0, nan, inf):
            with self.subTest(bound=bound):
                with self.assertRaisesRegex(
                    ValueError,
                    "^second_derivative_bound must be nonnegative and finite$",
                ):
                    composite_midpoint(lambda x: x, 0.0, 1.0, 2, bound)

        for bound in (-1.0, nan, inf):
            with self.subTest(bound=bound):
                with self.assertRaisesRegex(
                    ValueError,
                    "^fourth_derivative_bound must be nonnegative and finite$",
                ):
                    composite_simpson(lambda x: x, 0.0, 1.0, 2, bound)

    def test_reports_failed_and_nonfinite_function_evaluations(self) -> None:
        with self.assertRaisesRegex(
            QuadratureEvaluationError,
            r"^function value at x=.* must be finite$",
        ):
            composite_midpoint(lambda _x: nan, 0.0, 1.0, 2, 0.0)

        def outside_domain(_point: float) -> float:
            raise ArithmeticError("sample failed")

        with self.assertRaisesRegex(
            QuadratureEvaluationError,
            r"^function evaluation at x=.* failed$",
        ) as caught:
            composite_trapezoid(outside_domain, 0.0, 1.0, 2, 0.0)
        self.assertIsInstance(caught.exception.__cause__, ArithmeticError)


class BudgetedSimpsonTests(unittest.TestCase):
    def test_distinguishes_target_met_and_budget_exhaustion(self) -> None:
        met = certified_simpson(exp, 0.0, 1.0, 1e-8, e, 1000)
        exhausted = certified_simpson(exp, 0.0, 1.0, 1e-12, e, 4)

        self.assertEqual("target_met", met.status)
        self.assertTrue(met.target_met)
        self.assertEqual(1e-8, met.target_tolerance)
        self.assertLessEqual(met.error_bound, 1e-8)
        self.assertEqual("budget_exhausted", exhausted.status)
        self.assertFalse(exhausted.target_met)
        self.assertEqual(4, exhausted.subdivisions)
        self.assertGreater(exhausted.error_bound, 1e-12)

    def test_uses_the_smallest_even_grid_that_meets_the_bound(self) -> None:
        result = certified_simpson(
            lambda x: x**4,
            0.0,
            1.0,
            2e-4,
            24.0,
            100,
        )

        self.assertEqual(6, result.subdivisions)
        self.assertLessEqual(result.error_bound, 2e-4)
        previous_bound = 24.0 / (180.0 * 4**4)
        self.assertGreater(previous_bound, 2e-4)

    def test_odd_budget_uses_the_largest_permitted_even_grid(self) -> None:
        result = certified_simpson(exp, 0.0, 1.0, 1e-14, e, 5)

        self.assertEqual(4, result.subdivisions)
        self.assertEqual("budget_exhausted", result.status)
        self.assertFalse(result.target_met)

    def test_zero_fourth_derivative_bound_needs_only_one_panel(self) -> None:
        result = certified_simpson(
            lambda x: 3 * x + 2,
            -2.0,
            5.0,
            1e-30,
            0.0,
            2,
        )

        self.assertEqual(2, result.subdivisions)
        self.assertEqual(0.0, result.error_bound)
        self.assertTrue(result.target_met)

    def test_rejects_invalid_tolerance_and_budget(self) -> None:
        for tolerance in (0.0, -1.0, nan, inf):
            with self.subTest(tolerance=tolerance):
                with self.assertRaisesRegex(
                    ValueError,
                    "^tolerance must be positive and finite$",
                ):
                    certified_simpson(exp, 0.0, 1.0, tolerance, e, 10)

        for budget in (0, 1, -2, 2.5, True):
            with self.subTest(budget=budget):
                with self.assertRaisesRegex(
                    ValueError,
                    "^max_subintervals must be an integer at least 2$",
                ):
                    certified_simpson(
                        exp,
                        0.0,
                        1.0,
                        1e-6,
                        e,
                        budget,  # type: ignore[arg-type]
                    )

    def test_documentation_keeps_certificate_assumptions_explicit(self) -> None:
        source = (
            ROOT / "src" / "mathbook_examples" / "quadrature.py"
        ).read_text(encoding="utf-8")

        self.assertIn("caller must prove", source)
        self.assertIn("floating-point rounding", source)
        self.assertIn("does not verify the derivative bound", source)


if __name__ == "__main__":
    unittest.main()
