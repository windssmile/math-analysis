from dataclasses import FrozenInstanceError
import math
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mathbook_examples.fourier_series import (
    fejer_mean,
    fourier_partial_sum,
    sampled_fourier_coefficients,
)


class SampledFourierCoefficientsTests(unittest.TestCase):
    def test_constant_function_has_only_constant_coefficient(self) -> None:
        result = sampled_fourier_coefficients(lambda x: 3.0, 2 * math.pi, 2, 200)
        self.assertAlmostEqual(6.0, result.a0, places=12)
        self.assertTrue(all(abs(value) < 1e-12 for value in result.cosine_coefficients))
        self.assertTrue(all(abs(value) < 1e-12 for value in result.sine_coefficients))
        self.assertEqual((2, 200, "composite_midpoint", "finite_quadrature_only"),
                         (result.harmonics, result.panels, result.method, result.status))

    def test_single_harmonic_is_recovered_by_midpoint_quadrature(self) -> None:
        result = sampled_fourier_coefficients(math.sin, 2 * math.pi, 2, 200)
        self.assertAlmostEqual(0.0, result.a0, places=12)
        self.assertAlmostEqual(1.0, result.sine_coefficients[0], places=12)
        self.assertAlmostEqual(0.0, result.sine_coefficients[1], places=12)

    def test_result_is_frozen(self) -> None:
        result = sampled_fourier_coefficients(lambda x: 1.0, 2.0, 0, 4)
        with self.assertRaises(FrozenInstanceError):
            result.a0 = 1.0

    def test_rejects_invalid_contracts_and_callable_outputs(self) -> None:
        cases = (
            (lambda x: 1.0, True, 1, 4),
            (lambda x: 1.0, 0, 1, 4),
            (lambda x: 1.0, math.inf, 1, 4),
            (lambda x: 1.0, 2.0, -1, 4),
            (lambda x: 1.0, 2.0, 1.5, 4),
            (lambda x: 1.0, 2.0, 1, 0),
            (lambda x: 1.0, 2.0, 1, True),
            (lambda x: math.inf, 2.0, 1, 4),
            (lambda x: True, 2.0, 1, 4),
        )
        for args in cases:
            with self.subTest(args=args[1:]):
                with self.assertRaises((TypeError, ValueError)):
                    sampled_fourier_coefficients(*args)


class FiniteFourierValueTests(unittest.TestCase):
    def test_partial_sum_evaluates_real_series(self) -> None:
        result = fourier_partial_sum(math.pi / 2, 0.0, (0.0,), (1.0,), 2 * math.pi)
        self.assertAlmostEqual(1.0, result.value)
        self.assertEqual((1, "partial_sum", "finite_truncation_only"),
                         (result.order, result.method, result.status))

    def test_fejer_mean_uses_cesaro_weights(self) -> None:
        result = fejer_mean(0.0, 0.0, (2.0, 4.0), (0.0, 0.0), 2 * math.pi)
        self.assertAlmostEqual(8.0 / 3.0, result.value)
        self.assertEqual((2, "fejer_mean", "finite_truncation_only"),
                         (result.order, result.method, result.status))

    def test_zero_order_keeps_half_constant_term(self) -> None:
        partial = fourier_partial_sum(3.0, 6.0, (), (), 5.0)
        fejer = fejer_mean(3.0, 6.0, (), (), 5.0)
        self.assertEqual((3.0, 3.0), (partial.value, fejer.value))

    def test_results_are_frozen(self) -> None:
        result = fourier_partial_sum(0.0, 0.0, (), (), 1.0)
        with self.assertRaises(FrozenInstanceError):
            result.value = 1.0

    def test_rejects_malformed_coefficients_and_nonfinite_arithmetic(self) -> None:
        invalid = (
            (0.0, 0.0, (1.0,), (), 2.0),
            (True, 0.0, (), (), 2.0),
            (0.0, False, (), (), 2.0),
            (0.0, 0.0, (math.inf,), (0.0,), 2.0),
            (0.0, 0.0, "1", "1", 2.0),
            (0.0, 0.0, (), (), 0.0),
            (1e308, 0.0, (1e308,), (0.0,), 2.0),
        )
        for function in (fourier_partial_sum, fejer_mean):
            for args in invalid:
                with self.subTest(function=function.__name__, args=args):
                    with self.assertRaises((TypeError, ValueError)):
                        function(*args)


if __name__ == "__main__":
    unittest.main()
