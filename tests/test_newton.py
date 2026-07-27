"""Behavioral tests for pure and safeguarded Newton iterations."""

from dataclasses import FrozenInstanceError
from math import inf, isclose, nan
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mathbook_examples.newton import NewtonResult, newton, safeguarded_newton


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


class SafeguardedNewtonTest(unittest.TestCase):
    def test_converges_with_a_certified_midpoint_error_bound(self) -> None:
        result = safeguarded_newton(
            lambda point: point * point - 2,
            lambda point: 2 * point,
            1.0,
            2.0,
            interval_tolerance=1e-12,
        )

        self.assertTrue(result.converged)
        self.assertTrue(result.certified)
        self.assertEqual("bracket", result.reason)
        self.assertIsNotNone(result.error_bound)
        assert result.error_bound is not None
        self.assertLessEqual(result.error_bound, 5e-13)
        self.assertIn("newton", result.step_types)
        self.assertLessEqual(abs(result.value - 2**0.5), result.error_bound)
        self.assertEqual(result.iterations, len(result.step_types))

    def test_returns_exact_endpoint_roots_without_iteration(self) -> None:
        left_result = safeguarded_newton(
            lambda point: point - 1,
            lambda _point: 1.0,
            1.0,
            2.0,
        )
        right_result = safeguarded_newton(
            lambda point: point - 1,
            lambda _point: 1.0,
            0.0,
            1.0,
        )

        for result, expected in ((left_result, 1.0), (right_result, 1.0)):
            with self.subTest(expected=expected):
                self.assertTrue(result.converged)
                self.assertTrue(result.certified)
                self.assertEqual("endpoint", result.reason)
                self.assertEqual(expected, result.value)
                self.assertEqual(0.0, result.error_bound)
                self.assertEqual(0, result.iterations)
                self.assertEqual((), result.step_types)

    def test_collapses_bracket_when_candidate_is_exact_root(self) -> None:
        result = safeguarded_newton(
            lambda point: point,
            lambda _point: 1.0,
            -1.0,
            1.0,
        )

        self.assertTrue(result.converged)
        self.assertTrue(result.certified)
        self.assertEqual("endpoint", result.reason)
        self.assertEqual(0.0, result.value)
        self.assertEqual((0.0, 0.0), result.bracket)
        self.assertEqual(0.0, result.error_bound)
        self.assertEqual(("newton",), result.step_types)

    def test_initially_narrow_bracket_stops_at_iteration_zero(self) -> None:
        result = safeguarded_newton(
            lambda point: point - 2e-14,
            lambda _point: 1.0,
            -1e-13,
            1e-13,
            interval_tolerance=1e-12,
        )

        self.assertTrue(result.converged)
        self.assertTrue(result.certified)
        self.assertEqual("bracket", result.reason)
        self.assertEqual(0, result.iterations)
        self.assertEqual(0.0, result.value)
        self.assertEqual(1e-13, result.error_bound)

    def test_rejects_invalid_bracket_arguments(self) -> None:
        for left, right in ((nan, 1.0), (0.0, inf), (-inf, inf)):
            with self.subTest(left=left, right=right):
                with self.assertRaisesRegex(ValueError, "^endpoints must be finite$"):
                    safeguarded_newton(
                        lambda point: point,
                        lambda _point: 1.0,
                        left,
                        right,
                    )

        for left, right in ((1.0, 1.0), (2.0, 1.0)):
            with self.subTest(left=left, right=right):
                with self.assertRaisesRegex(
                    ValueError, "^left endpoint must be smaller than right endpoint$"
                ):
                    safeguarded_newton(
                        lambda point: point,
                        lambda _point: 1.0,
                        left,
                        right,
                    )

        with self.assertRaisesRegex(
            ValueError, "^endpoint values must have opposite signs$"
        ):
            safeguarded_newton(
                lambda point: point * point + 1,
                lambda point: 2 * point,
                -1.0,
                1.0,
            )

        with self.assertRaisesRegex(
            ValueError, "^function value at left endpoint must be finite$"
        ):
            safeguarded_newton(
                lambda point: nan if point == -1.0 else point,
                lambda _point: 1.0,
                -1.0,
                1.0,
            )

        with self.assertRaisesRegex(
            ValueError, "^function value at right endpoint must be finite$"
        ):
            safeguarded_newton(
                lambda point: nan if point == 1.0 else point,
                lambda _point: 1.0,
                -1.0,
                1.0,
            )

        tolerance_cases = (
            (
                "interval_tolerance",
                {"interval_tolerance": 0.0},
            ),
            (
                "interval_tolerance",
                {"interval_tolerance": nan},
            ),
            (
                "derivative_tolerance",
                {"derivative_tolerance": -1.0},
            ),
            (
                "derivative_tolerance",
                {"derivative_tolerance": inf},
            ),
        )
        for name, arguments in tolerance_cases:
            with self.subTest(arguments=arguments):
                with self.assertRaisesRegex(
                    ValueError, rf"^{name} must be positive and finite$"
                ):
                    safeguarded_newton(
                        lambda point: point,
                        lambda _point: 1.0,
                        -1.0,
                        1.0,
                        **arguments,
                    )

        for budget in (0, -1, 1.5, True):
            with self.subTest(max_iterations=budget):
                with self.assertRaisesRegex(
                    ValueError, "^max_iterations must be a positive integer$"
                ):
                    safeguarded_newton(
                        lambda point: point,
                        lambda _point: 1.0,
                        -1.0,
                        1.0,
                        max_iterations=budget,  # type: ignore[arg-type]
                    )

    def test_rejects_outside_newton_candidate_and_uses_bisection(self) -> None:
        result = safeguarded_newton(
            cycling_cubic,
            cycling_cubic_prime,
            -2.0,
            -1.0,
            interval_tolerance=1e-30,
            max_iterations=1,
        )

        self.assertFalse(result.converged)
        self.assertTrue(result.certified)
        self.assertEqual("max_iterations", result.reason)
        self.assertEqual(("bisection",), result.step_types)
        self.assertEqual((-2.0, -1.5), result.bracket)
        self.assertEqual(-1.75, result.value)
        self.assertEqual(0.25, result.error_bound)

    def test_accepts_newton_candidate_inside_central_half(self) -> None:
        result = safeguarded_newton(
            lambda point: point * point - 2,
            lambda point: 2 * point,
            1.0,
            2.0,
            interval_tolerance=1e-30,
            max_iterations=1,
        )

        self.assertEqual(("newton",), result.step_types)
        self.assertEqual((1.0, 1.5), result.bracket)
        self.assertEqual(1.25, result.value)
        self.assertEqual(0.25, result.error_bound)

    def test_small_or_nonfinite_derivative_falls_back_to_bisection(self) -> None:
        for derivative_value in (0.0, nan, inf):
            with self.subTest(derivative_value=derivative_value):
                result = safeguarded_newton(
                    lambda point: point,
                    lambda _point, value=derivative_value: value,
                    -1.0,
                    2.0,
                    interval_tolerance=1e-30,
                    max_iterations=1,
                )
                self.assertEqual(("bisection",), result.step_types)

    def test_nonfinite_newton_value_retries_midpoint(self) -> None:
        def function(point: float) -> float:
            return (
                nan
                if isclose(point, 1.3, rel_tol=0.0, abs_tol=1e-15)
                else point * point - 2
            )

        result = safeguarded_newton(
            function,
            lambda _point: 10 / 3,
            1.0,
            2.0,
            interval_tolerance=1e-30,
            max_iterations=1,
        )

        self.assertEqual(("bisection",), result.step_types)
        self.assertEqual((1.0, 1.5), result.bracket)
        self.assertTrue(result.certified)

    def test_nonfinite_midpoint_returns_uncertified_diagnostic(self) -> None:
        def function(point: float) -> float:
            return nan if point == 0.0 else point

        result = safeguarded_newton(
            function,
            lambda _point: 0.0,
            -1.0,
            1.0,
        )

        self.assertFalse(result.converged)
        self.assertFalse(result.certified)
        self.assertEqual("nonfinite_value", result.reason)
        self.assertIsNone(result.error_bound)
        self.assertEqual((), result.step_types)

    def test_every_budget_preserves_bracket_and_worst_case_contraction(self) -> None:
        function = lambda point: point * point - 2
        for budget in range(1, 9):
            with self.subTest(max_iterations=budget):
                result = safeguarded_newton(
                    function,
                    lambda point: 2 * point,
                    1.0,
                    2.0,
                    interval_tolerance=1e-30,
                    max_iterations=budget,
                )
                self.assertFalse(result.converged)
                self.assertTrue(result.certified)
                self.assertEqual("max_iterations", result.reason)
                self.assertEqual(budget, result.iterations)
                self.assertEqual(budget, len(result.step_types))
                self.assertIsNotNone(result.bracket)
                self.assertIsNotNone(result.error_bound)
                assert result.bracket is not None
                assert result.error_bound is not None
                left, right = result.bracket
                self.assertLessEqual(function(left), 0.0)
                self.assertGreaterEqual(function(right), 0.0)
                self.assertEqual((left + right) / 2, result.value)
                self.assertLessEqual(
                    result.error_bound,
                    0.5 * (0.75**budget) + 1e-15,
                )

    def test_simple_and_repeated_roots_show_different_error_orders(self) -> None:
        root = 1.3247179572447458
        simple_errors = []
        repeated_errors = []
        for budget in range(1, 5):
            simple = newton(
                cubic,
                cubic_prime,
                1.5,
                residual_tolerance=1e-30,
                step_tolerance=1e-30,
                max_iterations=budget,
            )
            repeated = newton(
                lambda point: (point - 1) ** 2,
                lambda point: 2 * (point - 1),
                2.0,
                residual_tolerance=1e-30,
                step_tolerance=1e-30,
                max_iterations=budget,
            )
            simple_errors.append(abs(simple.value - root))
            repeated_errors.append(abs(repeated.value - 1.0))

        for before, after in zip(simple_errors, simple_errors[1:]):
            self.assertLess(after, 2 * before * before)
        for budget, error in enumerate(repeated_errors, start=1):
            self.assertEqual(0.5**budget, error)


if __name__ == "__main__":
    unittest.main()
