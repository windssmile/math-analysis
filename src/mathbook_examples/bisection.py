"""A bisection method implementation with a certified error bound."""

from collections.abc import Callable
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class BisectionResult:
    """The approximation returned by :func:`bisect`."""

    root: float
    error_bound: float
    iterations: int


def _midpoint(left: float, right: float) -> float:
    """Return a finite midpoint without overflowing finite endpoints."""
    if left < 0.0 < right:
        return (left + right) / 2.0
    return left + (right - left) / 2.0


def _error_bound(left: float, midpoint: float, right: float) -> float:
    """Bound the distance from ``midpoint`` to either bracket endpoint."""
    return max(midpoint - left, right - midpoint)


def _function_value(
    function: Callable[[float], float], point: float, location: str
) -> float:
    value = function(point)
    if not isfinite(value):
        raise ValueError(f"function value at {location} must be finite")
    return value


def _same_sign(first: float, second: float) -> bool:
    return (first > 0.0) == (second > 0.0)


def bisect(
    function: Callable[[float], float],
    left: float,
    right: float,
    *,
    tolerance: float = 1e-8,
    max_iterations: int = 100,
) -> BisectionResult:
    """Locate a root bracketed by ``left`` and ``right``.

    The returned ``error_bound`` covers the distance from ``root`` to either
    endpoint of the final bracket.
    """
    if not isfinite(tolerance):
        raise ValueError("tolerance must be finite")
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    if not isfinite(left) or not isfinite(right):
        raise ValueError("endpoints must be finite")
    if left >= right:
        raise ValueError("left endpoint must be smaller than right endpoint")

    left_value = _function_value(function, left, "left endpoint")
    right_value = _function_value(function, right, "right endpoint")
    if left_value == 0:
        return BisectionResult(root=left, error_bound=0, iterations=0)
    if right_value == 0:
        return BisectionResult(root=right, error_bound=0, iterations=0)
    if _same_sign(left_value, right_value):
        raise ValueError("endpoint values must have opposite signs")

    for iteration in range(1, max_iterations + 1):
        midpoint = _midpoint(left, right)
        midpoint_value = _function_value(function, midpoint, "midpoint")
        if midpoint_value == 0:
            return BisectionResult(root=midpoint, error_bound=0, iterations=iteration)

        if _same_sign(left_value, midpoint_value):
            left = midpoint
            left_value = midpoint_value
        else:
            right = midpoint

        midpoint = _midpoint(left, right)
        error_bound = _error_bound(left, midpoint, right)
        if error_bound <= tolerance:
            midpoint_value = _function_value(function, midpoint, "midpoint")
            if midpoint_value == 0:
                return BisectionResult(
                    root=midpoint,
                    error_bound=0,
                    iterations=iteration,
                )
            return BisectionResult(
                root=midpoint,
                error_bound=error_bound,
                iterations=iteration,
            )

    raise RuntimeError("maximum iterations reached before tolerance")
