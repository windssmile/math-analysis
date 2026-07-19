"""A bisection method implementation with a certified error bound."""

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class BisectionResult:
    """The approximation returned by :func:`bisect`."""

    root: float
    error_bound: float
    iterations: int


def bisect(
    function: Callable[[float], float],
    left: float,
    right: float,
    *,
    tolerance: float = 1e-8,
    max_iterations: int = 100,
) -> BisectionResult:
    """Locate a root bracketed by ``left`` and ``right``.

    The returned ``error_bound`` is half the width of the final bracket.
    """
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    if left >= right:
        raise ValueError("left must be less than right")

    left_value = function(left)
    if left_value == 0:
        return BisectionResult(root=left, error_bound=0, iterations=0)

    right_value = function(right)
    if right_value == 0:
        return BisectionResult(root=right, error_bound=0, iterations=0)
    if left_value * right_value > 0:
        raise ValueError("function values at interval endpoints must have opposite signs")

    for iteration in range(1, max_iterations + 1):
        midpoint = (left + right) / 2
        midpoint_value = function(midpoint)
        if midpoint_value == 0:
            return BisectionResult(root=midpoint, error_bound=0, iterations=iteration)

        if left_value * midpoint_value > 0:
            left = midpoint
            left_value = midpoint_value
        else:
            right = midpoint
            right_value = midpoint_value

        error_bound = (right - left) / 2
        midpoint = (left + right) / 2
        if error_bound <= tolerance:
            return BisectionResult(
                root=midpoint,
                error_bound=error_bound,
                iterations=iteration,
            )

    raise RuntimeError("maximum iterations exceeded")
