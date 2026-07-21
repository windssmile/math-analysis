"""Behavioral tests for the certified contraction iteration example."""

from math import inf, nan, sqrt
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mathbook_examples.fixed_point import iterate_contraction, iterate_trace


class FixedPointTest(unittest.TestCase):
    def test_iteration_trace_preserves_initial_and_requested_length(self) -> None:
        trace = iterate_trace(lambda x: 1 / (2 + x), 0.0, steps=4)
        self.assertEqual(len(trace), 5)
        self.assertEqual(trace[0], 0.0)

    def test_iteration_trace_rejects_invalid_steps(self) -> None:
        for steps in (True, False, 1.5, "2", 0, -1):
            with self.subTest(steps=steps):
                with self.assertRaisesRegex(ValueError, "^steps must be a positive integer$"):
                    iterate_trace(lambda x: x / 2, 1.0, steps=steps)  # type: ignore[arg-type]

    def test_iteration_trace_rejects_nonfinite_values(self) -> None:
        with self.assertRaisesRegex(ValueError, "^initial value must be finite$"):
            iterate_trace(lambda x: x / 2, inf, steps=2)
        with self.assertRaisesRegex(ValueError, "^function value at iteration 2 must be finite$"):
            iterate_trace(lambda x: nan if x == 0.5 else x / 2, 1.0, steps=3)

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
