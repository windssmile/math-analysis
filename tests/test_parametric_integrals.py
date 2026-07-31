from dataclasses import FrozenInstanceError
from math import gamma, inf, isfinite, nan
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mathbook_examples.parametric_integrals import beta_integral, gamma_integral

class ParametricIntegralTests(unittest.TestCase):
    def test_gamma_two_is_certified_with_supplied_bound(self):
        result = gamma_integral(2.0, 1e-5, 4096, fourth_derivative_bound=10.0)
        self.assertEqual("target_met", result.status)
        self.assertTrue(result.target_met)
        self.assertLessEqual(abs(result.value - gamma(2.0)), result.total_error_bound)
        self.assertTrue(isfinite(result.endpoint_error_bound))

    def test_missing_regular_bound_is_uncertified(self):
        result = beta_integral(2.0, 3.0, 1e-5, 512)
        self.assertEqual("uncertified", result.status)
        self.assertIsNone(result.quadrature_error_bound)
        self.assertIsNone(result.total_error_bound)
        self.assertFalse(result.target_met)

    def test_low_budget_returns_finite_valid_bound(self):
        result = gamma_integral(2.0, 1e-12, 2, fourth_derivative_bound=10.0)
        self.assertEqual("budget_exhausted", result.status)
        self.assertFalse(result.target_met)
        self.assertTrue(isfinite(result.total_error_bound))
        self.assertGreater(result.total_error_bound, 1e-12)

    def test_beta_certified_bound_contains_exact_value(self):
        result = beta_integral(2.0, 3.0, 1e-5, 4096, fourth_derivative_bound=100.0)
        self.assertLessEqual(abs(result.value - 1 / 12), result.total_error_bound)

    def test_result_is_frozen(self):
        result = gamma_integral(1.0, 1e-3, 64)
        with self.assertRaises(FrozenInstanceError):
            result.status = "changed"

    def test_rejects_invalid_inputs(self):
        for value in (0.0, -1.0, nan, inf, True):
            with self.subTest(parameter=value):
                with self.assertRaises(ValueError):
                    gamma_integral(value, 1e-3, 64)
        for tolerance in (0.0, -1.0, nan, inf, True):
            with self.subTest(tolerance=tolerance):
                with self.assertRaises(ValueError):
                    gamma_integral(1.0, tolerance, 64)
        for budget in (0, 1, -1, 2.5, True):
            with self.subTest(budget=budget):
                with self.assertRaises(ValueError):
                    beta_integral(1.0, 1.0, 1e-3, budget)
        for bound in (-1.0, nan, inf, True):
            with self.subTest(bound=bound):
                with self.assertRaises(ValueError):
                    beta_integral(1.0, 1.0, 1e-3, 64, fourth_derivative_bound=bound)

if __name__ == "__main__":
    unittest.main()
