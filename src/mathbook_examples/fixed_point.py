"""Certified iteration for a caller-proven contraction on a real interval."""

from collections.abc import Callable
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class FixedPointResult:
    """An iterate accompanied by a mathematically certified error bound."""

    value: float
    error_bound: float
    iterations: int


def _require_finite(value: float, label: str) -> None:
    if not isfinite(value):
        raise ValueError(f"{label} must be finite")


def iterate_trace(
    function: Callable[[float], float], initial: float, *, steps: int
) -> tuple[float, ...]:
    """Return an uncertified iteration trace for comparison experiments."""
    _require_finite(initial, "initial value")
    if type(steps) is not int or steps <= 0:
        raise ValueError("steps must be a positive integer")

    values = [initial]
    for iteration in range(1, steps + 1):
        value = function(values[-1])
        if not isfinite(value):
            raise ValueError(f"function value at iteration {iteration} must be finite")
        values.append(value)
    return tuple(values)


def iterate_contraction(
    function: Callable[[float], float],
    initial: float,
    *,
    contraction: float,
    tolerance: float = 1e-8,
    max_iterations: int = 100,
) -> FixedPointResult:
    """Iterate a caller-certified contraction until its a-posteriori bound passes.

    The caller must already have proved that ``function`` maps the relevant
    closed interval into itself and has Lipschitz constant at most
    ``contraction``.  Runtime samples cannot establish that hypothesis.
    """
    _require_finite(tolerance, "tolerance")
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    _require_finite(contraction, "contraction")
    if not 0 <= contraction < 1:
        raise ValueError("contraction must be in [0, 1)")
    _require_finite(initial, "initial value")
    if type(max_iterations) is not int or max_iterations <= 0:
        raise ValueError("max_iterations must be a positive integer")

    previous = initial
    multiplier = contraction / (1 - contraction)
    for iteration in range(1, max_iterations + 1):
        current = function(previous)
        if not isfinite(current):
            raise ValueError(f"function value at iteration {iteration} must be finite")
        error_bound = multiplier * abs(current - previous)
        if error_bound <= tolerance:
            return FixedPointResult(current, error_bound, iteration)
        previous = current

    raise RuntimeError("maximum iterations reached before tolerance")
