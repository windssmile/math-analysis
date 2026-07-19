"""Behavioral tests for the certified contraction iteration example."""

from math import inf, nan, sqrt
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mathbook_examples.fixed_point import iterate_contraction


class FixedPointTest(unittest.TestCase):
    def test_contraction_iteration_returns_a_posteriori_certificate(self) -> None:
        result = iterate_contraction(
            lambda x: 1 / (2 + x),
            0.0,
            contraction=0.25,
            tolerance=1e-8,
        )

        self.assertLessEqual(abs(result.value - (sqrt(2) - 1)), result.error_bound)
        self.assertLessEqual(result.error_bound, 1e-8)
        self.assertGreater(result.iterations, 0)

    def test_rejects_invalid_scalar_inputs(self) -> None:
        for tolerance in (nan, inf, -inf):
            with self.subTest(tolerance=tolerance):
                with self.assertRaisesRegex(ValueError, "^tolerance must be finite$"):
                    iterate_contraction(lambda x: x / 2, 1.0, contraction=0.5, tolerance=tolerance)
        with self.assertRaisesRegex(ValueError, "^tolerance must be positive$"):
            iterate_contraction(lambda x: x / 2, 1.0, contraction=0.5, tolerance=0)
        for contraction in (nan, inf, -inf):
            with self.subTest(contraction=contraction):
                with self.assertRaisesRegex(ValueError, "^contraction must be finite$"):
                    iterate_contraction(lambda x: x / 2, 1.0, contraction=contraction)
        for contraction in (-0.1, 1.0):
            with self.subTest(contraction=contraction):
                with self.assertRaisesRegex(ValueError, r"^contraction must be in \[0, 1\)$"):
                    iterate_contraction(lambda x: x / 2, 1.0, contraction=contraction)
        with self.assertRaisesRegex(ValueError, "^initial value must be finite$"):
            iterate_contraction(lambda x: x / 2, inf, contraction=0.5)

    def test_rejects_nonfinite_iterate(self) -> None:
        with self.assertRaisesRegex(ValueError, "^function value at iteration 1 must be finite$"):
            iterate_contraction(lambda x: nan, 0.0, contraction=0.5)

    def test_rejects_too_small_iteration_budget(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "^maximum iterations reached before tolerance$"):
            iterate_contraction(lambda x: x / 2, 1.0, contraction=0.5, tolerance=1e-12, max_iterations=2)


if __name__ == "__main__":
    unittest.main()
