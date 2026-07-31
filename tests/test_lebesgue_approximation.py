from dataclasses import FrozenInstanceError
import math
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mathbook_examples.lebesgue_approximation import (
    finite_cover_upper_bound,
    simple_integral,
)


class SimpleIntegralTests(unittest.TestCase):
    def test_computes_signed_finite_simple_integral(self) -> None:
        self.assertEqual(-2.0, simple_integral([2, -1], [0.5, 3]))

    def test_rejects_malformed_sequences(self) -> None:
        for values, measures in (([], []), ([1], []), ([True], [1]), ([1], [False]),
                                 ([1], [-1]), ([1], [math.inf]), (["1"], [1])):
            with self.subTest(values=values, measures=measures):
                with self.assertRaises((TypeError, ValueError)):
                    simple_integral(values, measures)

    def test_rejects_nonfinite_products_and_sums(self) -> None:
        with self.assertRaises(ValueError):
            simple_integral([1e308], [1e308])
        with self.assertRaises(ValueError):
            simple_integral([1e308, 1e308], [1, 1])


class FiniteCoverTests(unittest.TestCase):
    def test_merges_intervals_and_reports_only_an_upper_bound(self) -> None:
        result = finite_cover_upper_bound([(0, 1), (0.5, 2), (3, 4)])
        self.assertEqual(3.0, result.upper_bound)
        self.assertEqual(((0.0, 2.0), (3.0, 4.0)), result.merged_intervals)
        self.assertEqual((3, 2), (result.input_count, result.merged_count))
        self.assertEqual("finite_cover_only", result.status)

    def test_touching_and_degenerate_intervals_merge(self) -> None:
        result = finite_cover_upper_bound([(2, 2), (0, 1), (1, 2)])
        self.assertEqual(((0.0, 2.0),), result.merged_intervals)
        self.assertEqual(2.0, result.upper_bound)

    def test_result_is_frozen(self) -> None:
        result = finite_cover_upper_bound([(0, 1)])
        with self.assertRaises(FrozenInstanceError):
            result.upper_bound = 2

    def test_rejects_invalid_intervals(self) -> None:
        for intervals in ([], [(1, 0)], [(0, math.inf)], [(False, 1)], [(0,)], ["01"]):
            with self.subTest(intervals=intervals):
                with self.assertRaises((TypeError, ValueError)):
                    finite_cover_upper_bound(intervals)

    def test_rejects_overflowing_total_length(self) -> None:
        with self.assertRaises(ValueError):
            finite_cover_upper_bound([(-1e308, 0), (1, 1e308)])


if __name__ == "__main__":
    unittest.main()
