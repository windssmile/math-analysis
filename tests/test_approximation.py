from dataclasses import FrozenInstanceError
import math
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mathbook_examples.approximation import bernstein_approximation


class BernsteinApproximationTests(unittest.TestCase):
    def test_preserves_constants_and_linear_functions(self) -> None:
        constant = bernstein_approximation(lambda x: 3.0, -2.0, 4.0, 8, 1.25)
        linear = bernstein_approximation(lambda x: 2.0 * x - 1.0, -2.0, 4.0, 8, 1.25)
        self.assertAlmostEqual(3.0, constant.approximation)
        self.assertAlmostEqual(1.5, linear.approximation)

    def test_supports_general_interval_and_endpoint_evaluation(self) -> None:
        left = bernstein_approximation(lambda x: x * x, 2.0, 5.0, 12, 2.0)
        right = bernstein_approximation(lambda x: x * x, 2.0, 5.0, 12, 5.0)
        self.assertEqual(4.0, left.approximation)
        self.assertEqual(25.0, right.approximation)

    def test_lipschitz_bound_is_a_certificate_not_grid_observation(self) -> None:
        result = bernstein_approximation(
            lambda x: abs(x),
            -1.0,
            1.0,
            100,
            0.2,
            lipschitz_constant=1.0,
            grid_points=101,
        )
        self.assertEqual("certified", result.status)
        self.assertAlmostEqual(0.1, result.theoretical_error_bound)
        self.assertIsNotNone(result.observed_grid_error)
        self.assertIn("Lipschitz constant supplied by caller", result.assumptions)

    def test_second_derivative_bound_uses_proved_constant(self) -> None:
        result = bernstein_approximation(
            lambda x: x * x, 0.0, 1.0, 10, 0.4, second_derivative_bound=2.0
        )
        self.assertAlmostEqual(1.0 / 40.0, result.theoretical_error_bound)

    def test_without_regularizer_reports_no_certificate(self) -> None:
        result = bernstein_approximation(lambda x: x * x, 0.0, 1.0, 5, 0.3)
        self.assertEqual("uncertified", result.status)
        self.assertIsNone(result.theoretical_error_bound)
        self.assertIsNone(result.observed_grid_error)

    def test_rejects_invalid_inputs_and_nonfinite_samples(self) -> None:
        invalid = (
            (lambda x: x, 0.0, 0.0, 2, 0.0),
            (lambda x: x, math.nan, 1.0, 2, 0.0),
            (lambda x: x, 0.0, 1.0, -1, 0.0),
            (lambda x: x, 0.0, 1.0, 2, 1.1),
            (lambda x: math.nan, 0.0, 1.0, 2, 0.5),
        )
        for args in invalid:
            with self.subTest(args=args), self.assertRaises(ValueError):
                bernstein_approximation(*args)

    def test_rejects_invalid_bounds_and_grid(self) -> None:
        for kwargs in (
            {"lipschitz_constant": -1.0},
            {"second_derivative_bound": math.inf},
            {"grid_points": 1},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                bernstein_approximation(lambda x: x, 0.0, 1.0, 3, 0.5, **kwargs)

    def test_result_is_frozen(self) -> None:
        result = bernstein_approximation(lambda x: x, 0.0, 1.0, 2, 0.5)
        with self.assertRaises(FrozenInstanceError):
            result.status = "changed"

