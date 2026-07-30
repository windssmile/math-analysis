"""Reliable Bernstein approximation helpers for Chapter 27."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable


@dataclass(frozen=True)
class BernsteinResult:
    """One approximation with separate analytic and observed error fields."""

    approximation: float
    degree: int
    interval: tuple[float, float]
    theoretical_error_bound: float | None
    observed_grid_error: float | None
    status: str
    assumptions: tuple[str, ...]


def _finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _optional_nonnegative(value: float | None, name: str) -> float | None:
    if value is None:
        return None
    value = _finite(value, name)
    if value < 0.0:
        raise ValueError(f"{name} must be nonnegative")
    return value


def _sample(function: Callable[[float], float], point: float) -> float:
    try:
        value = float(function(point))
    except Exception as exc:
        raise ValueError("function sampling failed") from exc
    if not math.isfinite(value):
        raise ValueError("function samples must be finite")
    return value


def _de_casteljau(values: list[float], parameter: float) -> float:
    """Evaluate Bernstein data using repeated convex interpolation."""

    work = values.copy()
    one_minus = 1.0 - parameter
    for width in range(len(work) - 1, 0, -1):
        for index in range(width):
            work[index] = one_minus * work[index] + parameter * work[index + 1]
            if not math.isfinite(work[index]):
                raise ValueError("nonfinite Bernstein intermediate")
    return work[0]


def bernstein_approximation(
    function: Callable[[float], float],
    left: float,
    right: float,
    degree: int,
    point: float,
    *,
    lipschitz_constant: float | None = None,
    second_derivative_bound: float | None = None,
    grid_points: int | None = None,
) -> BernsteinResult:
    """Evaluate a Bernstein approximation and optional proved error bounds.

    A supplied Lipschitz constant or second-derivative bound is trusted as a
    mathematical assumption from the caller. A grid error remains an observed
    diagnostic and is never promoted to a certificate.
    """

    left = _finite(left, "left")
    right = _finite(right, "right")
    point = _finite(point, "point")
    if not left < right:
        raise ValueError("interval must be nondegenerate with left < right")
    if isinstance(degree, bool) or not isinstance(degree, int) or degree < 0:
        raise ValueError("degree must be a nonnegative integer")
    if point < left or point > right:
        raise ValueError("point must lie in the closed interval")
    lipschitz_constant = _optional_nonnegative(
        lipschitz_constant, "lipschitz_constant"
    )
    second_derivative_bound = _optional_nonnegative(
        second_derivative_bound, "second_derivative_bound"
    )
    if grid_points is not None:
        if (
            isinstance(grid_points, bool)
            or not isinstance(grid_points, int)
            or grid_points < 2
        ):
            raise ValueError("grid_points must be an integer of at least 2")

    length = right - left
    samples = [
        _sample(function, left + length * index / degree)
        for index in range(degree + 1)
    ] if degree else [_sample(function, left)]
    parameter = (point - left) / length
    approximation = _de_casteljau(samples, parameter)

    bounds: list[float] = []
    assumptions: list[str] = ["function finite at all Bernstein nodes"]
    if degree > 0 and lipschitz_constant is not None:
        bounds.append(lipschitz_constant * length / (2.0 * math.sqrt(degree)))
        assumptions.append("Lipschitz constant supplied by caller")
    if degree > 0 and second_derivative_bound is not None:
        bounds.append(second_derivative_bound * length * length / (8.0 * degree))
        assumptions.append("second-derivative bound supplied by caller")
    theoretical = min(bounds) if bounds else None

    observed = None
    if grid_points is not None:
        errors = []
        for index in range(grid_points):
            grid_point = left + length * index / (grid_points - 1)
            grid_parameter = (grid_point - left) / length
            errors.append(
                abs(
                    _de_casteljau(samples, grid_parameter)
                    - _sample(function, grid_point)
                )
            )
        observed = max(errors)
        assumptions.append("grid error is observational, not a sup-norm certificate")

    return BernsteinResult(
        approximation=approximation,
        degree=degree,
        interval=(left, right),
        theoretical_error_bound=theoretical,
        observed_grid_error=observed,
        status="certified" if theoretical is not None else "uncertified",
        assumptions=tuple(assumptions),
    )

