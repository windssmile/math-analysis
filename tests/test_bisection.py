"""Behavioral tests for the certified bisection example."""

from math import inf, isfinite, nan, sqrt
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mathbook_examples.bisection import bisect


class BisectionTest(unittest.TestCase):
    def test_approximates_square_root_two_with_certified_error(self) -> None:
        result = bisect(lambda x: x * x - 2, 1.0, 2.0, tolerance=1e-8)

        self.assertLessEqual(abs(result.root - sqrt(2)), result.error_bound)
        self.assertLessEqual(result.error_bound, 1e-8)
        self.assertGreater(result.iterations, 0)

    def test_returns_an_endpoint_root(self) -> None:
        result = bisect(lambda x: x - 1, 1.0, 3.0, tolerance=1e-6)

        self.assertEqual(1.0, result.root)
        self.assertEqual(0.0, result.error_bound)
        self.assertEqual(0, result.iterations)

    def test_rejects_interval_without_sign_change(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "^endpoint values must have opposite signs$"
        ):
            bisect(lambda x: x * x + 1, -1.0, 1.0)

    def test_rejects_tiny_same_sign_endpoint_values(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "^endpoint values must have opposite signs$"
        ):
            bisect(lambda x: 1e-300, -1.0, 1.0)

    def test_rejects_nonpositive_tolerance(self) -> None:
        with self.assertRaisesRegex(ValueError, "^tolerance must be positive$"):
            bisect(lambda x: x, -1.0, 1.0, tolerance=0)

    def test_large_finite_bracket_converges_without_overflow(self) -> None:
        expected_root = 1.4e308

        result = bisect(
            lambda x: x - expected_root,
            1e308,
            1.7e308,
            tolerance=1e300,
        )

        self.assertTrue(isfinite(result.root))
        self.assertTrue(isfinite(result.error_bound))
        self.assertLessEqual(abs(result.root - expected_root), result.error_bound)
        self.assertLessEqual(result.error_bound, 1e300)

    def test_rejects_nan_returning_function(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "^function value at left endpoint must be finite$"
        ):
            bisect(lambda x: nan, -1.0, 1.0)

    def test_rejects_nonfinite_inputs(self) -> None:
        for left, right in ((nan, 1.0), (-1.0, inf), (-inf, 1.0)):
            with self.subTest(left=left, right=right):
                with self.assertRaisesRegex(ValueError, "^endpoints must be finite$"):
                    bisect(lambda x: x, left, right)

        for tolerance in (nan, inf, -inf):
            with self.subTest(tolerance=tolerance):
                with self.assertRaisesRegex(ValueError, "^tolerance must be finite$"):
                    bisect(lambda x: x - 0.25, -1.0, 1.0, tolerance=tolerance)

    def test_rejects_nonfinite_function_values(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "^function value at right endpoint must be finite$"
        ):
            bisect(lambda x: inf if x == 1.0 else 0.0, -1.0, 1.0)

        with self.assertRaisesRegex(
            ValueError, "^function value at midpoint must be finite$"
        ):
            bisect(lambda x: nan if x == 0.0 else x, -1.0, 1.0)

    def test_rejects_too_small_iteration_budget(self) -> None:
        with self.assertRaisesRegex(
            RuntimeError, "^maximum iterations reached before tolerance$"
        ):
            bisect(lambda x: x * x - 2, 1.0, 2.0, tolerance=1e-12, max_iterations=2)


if __name__ == "__main__":
    unittest.main()
