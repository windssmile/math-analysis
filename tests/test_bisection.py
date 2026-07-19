"""Behavioral tests for the certified bisection example."""

from math import sqrt

import pytest

from mathbook_examples.bisection import bisect


def test_bisects_sqrt_two_with_a_certified_error_bound() -> None:
    tolerance = 1e-8

    result = bisect(lambda x: x * x - 2, 1, 2, tolerance=tolerance)

    assert abs(result.root - sqrt(2)) <= result.error_bound
    assert result.error_bound <= tolerance
    assert result.iterations > 0


def test_returns_an_endpoint_root_without_iterations() -> None:
    result = bisect(lambda x: x - 1, 1, 3)

    assert result.root == 1
    assert result.error_bound == 0
    assert result.iterations == 0


def test_rejects_an_interval_whose_endpoint_values_have_the_same_sign() -> None:
    with pytest.raises(ValueError, match="opposite signs"):
        bisect(lambda x: x * x + 1, -1, 1)


def test_rejects_a_nonpositive_tolerance() -> None:
    with pytest.raises(ValueError, match="tolerance must be positive"):
        bisect(lambda x: x, -1, 1, tolerance=0)


def test_raises_when_the_iteration_limit_is_reached() -> None:
    with pytest.raises(RuntimeError, match="maximum iterations"):
        bisect(lambda x: x * x - 2, 1, 2, tolerance=1e-12, max_iterations=2)
