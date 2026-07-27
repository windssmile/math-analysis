"""Behavioral tests for pure and safeguarded Newton iterations."""

from dataclasses import FrozenInstanceError
from math import inf, isclose, nan
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mathbook_examples.newton import NewtonResult, newton


def cubic(point: float) -> float:
    return point**3 - point - 1


def cubic_prime(point: float) -> float:
    return 3 * point**2 - 1


def cycling_cubic(point: float) -> float:
    return point**3 - 2 * point + 2


def cycling_cubic_prime(point: float) -> float:
    return 3 * point**2 - 2


class PureNewtonTest(unittest.TestCase):
    def test_returns_frozen_uncertified_result_for_simple_root(self) -> None:
        result = newton(cubic, cubic_prime, 1.5)

        self.assertIsInstance(result, NewtonResult)
        self.assertTrue(result.converged)
        self.assertFalse(result.certified)
        self.assertEqual("residual", result.reason)
        self.assertLess(result.residual, 1e-10)
        self.assertIsNone(result.bracket)
        self.assertIsNone(result.error_bound)
        self.assertEqual(result.iterations, len(result.step_types))
        self.assertTrue(all(step == "newton" for step in result.step_types))
        self.assertTrue(
            isclose(result.value, 1.3247179572447458, rel_tol=0.0, abs_tol=1e-10)
        )
        with self.assertRaisesRegex(FrozenInstanceError, "cannot assign to field"):
            result.value = 0.0  # type: ignore[misc]

    def test_initial_root_stops_without_taking_a_step(self) -> None:
        result = newton(lambda point: point - 2, lambda _point: 1.0, 2.0)

        self.assertTrue(result.converged)
        self.assertFalse(result.certified)
        self.assertEqual("residual", result.reason)
        self.assertEqual(0, result.iterations)
        self.assertEqual(0.0, result.residual)
        self.assertIsNone(result.last_step)
        self.assertEqual((), result.step_types)

    def test_small_derivative_returns_diagnostic_result(self) -> None:
        result = newton(
            lambda point: point * point + 1,
            lambda point: 2 * point,
            0.0,
        )

        self.assertFalse(result.converged)
        self.assertFalse(result.certified)
        self.assertEqual("derivative_too_small", result.reason)
        self.assertEqual(0, result.iterations)
        self.assertEqual(1.0, result.residual)
        self.assertIsNone(result.last_step)

    def test_nonfinite_function_or_derivative_returns_diagnostic_result(self) -> None:
        function_result = newton(lambda _point: nan, lambda _point: 1.0, 0.0)
        derivative_result = newton(lambda _point: 1.0, lambda _point: inf, 0.0)

        self.assertEqual("nonfinite_value", function_result.reason)
        self.assertEqual(inf, function_result.residual)
        self.assertEqual("nonfinite_value", derivative_result.reason)
        self.assertEqual(1.0, derivative_result.residual)
        self.assertFalse(function_result.converged)
        self.assertFalse(derivative_result.converged)

    def test_nonfinite_candidate_or_candidate_value_keeps_last_finite_state(self) -> None:
        candidate_result = newton(
            lambda point: point,
            lambda _point: 1e-308,
            1e308,
            derivative_tolerance=1e-320,
        )

        def finite_only_at_zero(point: float) -> float:
            return 1.0 if point == 0.0 else nan

        value_result = newton(finite_only_at_zero, lambda _point: 1.0, 0.0)

        self.assertEqual("nonfinite_value", candidate_result.reason)
        self.assertEqual(1e308, candidate_result.value)
        self.assertEqual("nonfinite_value", value_result.reason)
        self.assertEqual(0.0, value_result.value)
        self.assertEqual(0, value_result.iterations)
        self.assertEqual((), value_result.step_types)

    def test_cycle_exhausts_iteration_budget_with_trace(self) -> None:
        result = newton(
            cycling_cubic,
            cycling_cubic_prime,
            0.0,
            residual_tolerance=1e-15,
            step_tolerance=1e-15,
            max_iterations=4,
        )

        self.assertFalse(result.converged)
        self.assertFalse(result.certified)
        self.assertEqual("max_iterations", result.reason)
        self.assertEqual(4, result.iterations)
        self.assertEqual(0.0, result.value)
        self.assertEqual(1.0, result.last_step)
        self.assertEqual(("newton",) * 4, result.step_types)

    def test_step_tolerance_is_only_an_uncertified_stop_signal(self) -> None:
        result = newton(
            lambda point: point * point - 2,
            lambda point: 2 * point,
            1.0,
            residual_tolerance=1e-30,
            step_tolerance=1.0,
        )

        self.assertTrue(result.converged)
        self.assertFalse(result.certified)
        self.assertEqual("step", result.reason)
        self.assertEqual(1, result.iterations)
        self.assertEqual(0.5, result.last_step)
        self.assertEqual(0.25, result.residual)

    def test_rejects_invalid_arguments(self) -> None:
        for initial in (nan, inf, -inf):
            with self.subTest(initial=initial):
                with self.assertRaisesRegex(ValueError, "^initial must be finite$"):
                    newton(cubic, cubic_prime, initial)

        tolerance_cases = (
            ("residual_tolerance", {"residual_tolerance": 0.0}),
            ("residual_tolerance", {"residual_tolerance": nan}),
            ("step_tolerance", {"step_tolerance": -1.0}),
            ("step_tolerance", {"step_tolerance": inf}),
            ("derivative_tolerance", {"derivative_tolerance": 0.0}),
            ("derivative_tolerance", {"derivative_tolerance": nan}),
        )
        for name, arguments in tolerance_cases:
            with self.subTest(arguments=arguments):
                with self.assertRaisesRegex(
                    ValueError, rf"^{name} must be positive and finite$"
                ):
                    newton(cubic, cubic_prime, 1.5, **arguments)

        for budget in (0, -1, 1.5, True):
            with self.subTest(max_iterations=budget):
                with self.assertRaisesRegex(
                    ValueError, "^max_iterations must be a positive integer$"
                ):
                    newton(
                        cubic,
                        cubic_prime,
                        1.5,
                        max_iterations=budget,  # type: ignore[arg-type]
                    )


if __name__ == "__main__":
    unittest.main()
