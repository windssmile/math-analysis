from dataclasses import FrozenInstanceError
import math
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mathbook_examples.series import (
    geometric_series_certificate,
    p_series_integral_certificate,
)


class GeometricSeriesCertificateTests(unittest.TestCase):
    def test_returns_smallest_certified_term_count(self) -> None:
        result = geometric_series_certificate(1.0, 0.5, 0.01, 100)
        self.assertEqual("certified", result.status)
        self.assertEqual(8, result.terms_used)
        self.assertLessEqual(result.error_bound, 0.01)
        self.assertAlmostEqual(2.0 - 2.0**-7, result.approximation)
        self.assertIn("|r| < 1", result.assumptions)

    def test_reports_budget_unmet_without_false_certificate(self) -> None:
        result = geometric_series_certificate(1.0, 0.9, 1e-12, 4)
        self.assertEqual("budget_unmet", result.status)
        self.assertEqual(4, result.terms_used)
        self.assertGreater(result.error_bound, 1e-12)

    def test_rejects_invalid_geometric_inputs(self) -> None:
        invalid = (
            (math.nan, 0.5, 0.1, 10),
            (1.0, 1.0, 0.1, 10),
            (1.0, -1.0, 0.1, 10),
            (1.0, 0.5, 0.0, 10),
            (1.0, 0.5, 0.1, 0),
        )
        for args in invalid:
            with self.subTest(args=args), self.assertRaises(ValueError):
                geometric_series_certificate(*args)


class PSeriesCertificateTests(unittest.TestCase):
    def test_integral_tail_bound_certifies_requested_tolerance(self) -> None:
        result = p_series_integral_certificate(2.0, 0.01, 1_000)
        self.assertEqual("certified", result.status)
        self.assertEqual(100, result.terms_used)
        self.assertLessEqual(result.error_bound, 0.01)
        self.assertIn("p > 1", result.assumptions)

    def test_budget_unmet_keeps_the_proved_bound(self) -> None:
        result = p_series_integral_certificate(2.0, 1e-6, 100)
        self.assertEqual("budget_unmet", result.status)
        self.assertAlmostEqual(0.01, result.error_bound)

    def test_rejects_nonconvergent_or_nonfinite_inputs(self) -> None:
        for exponent in (1.0, 0.5, math.inf, math.nan):
            with self.subTest(exponent=exponent), self.assertRaises(ValueError):
                p_series_integral_certificate(exponent, 0.01, 100)

    def test_result_is_frozen(self) -> None:
        result = p_series_integral_certificate(2.0, 0.1, 100)
        with self.assertRaises(FrozenInstanceError):
            result.status = "changed"
