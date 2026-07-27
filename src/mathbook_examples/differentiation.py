"""Finite Taylor tools with heuristic differences, not an error certificate."""

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from math import isfinite
import sys


@dataclass(frozen=True)
class DifferenceEstimate:
    """An uncertified finite-difference estimate."""

    value: float
    step: float
    method: str


def _require_finite(value: float, label: str) -> float:
    converted = float(value)
    if not isfinite(converted):
        raise ValueError(f"{label} must be finite")
    return converted


def evaluate_taylor(
    coefficients: Sequence[float], center: float, point: float
) -> float:
    """Evaluate ascending-power Taylor coefficients by reverse Horner steps.

    ``coefficients[k]`` is the coefficient of ``(point - center) ** k`` and
    therefore already includes any factorial denominator. This function does
    not certify the Taylor remainder.
    """
    if not coefficients:
        raise ValueError("coefficients must not be empty")
    center_value = _require_finite(center, "center")
    point_value = _require_finite(point, "point")
    finite_coefficients = []
    for index, coefficient in enumerate(coefficients):
        finite_coefficients.append(_require_finite(coefficient, f"coefficient {index}"))

    offset = point_value - center_value
    if not isfinite(offset):
        raise ValueError("Taylor evaluation must remain finite")
    value = finite_coefficients[-1]
    for coefficient in reversed(finite_coefficients[:-1]):
        value = value * offset + coefficient
        if not isfinite(value):
            raise ValueError("Taylor evaluation must remain finite")
    return value


def _difference_step(point: float, step: float | None, power: float) -> float:
    if step is not None:
        step_value = float(step)
        if not isfinite(step_value) or step_value <= 0:
            raise ValueError("step must be positive and finite")
        return step_value
    return sys.float_info.epsilon**power * max(1.0, abs(point))


def _sample(function: Callable[[float], float], point: float) -> float:
    if not isfinite(point):
        raise ValueError("sample point must be finite")
    value = float(function(point))
    if not isfinite(value):
        raise ValueError("function value must be finite")
    return value


def forward_difference(
    function: Callable[[float], float], point: float, *, step: float | None = None
) -> DifferenceEstimate:
    """Use a heuristic step for an estimate, not an error certificate."""
    point_value = _require_finite(point, "point")
    step_value = _difference_step(point_value, step, 0.5)
    right = point_value + step_value
    value = (_sample(function, right) - _sample(function, point_value)) / step_value
    if not isfinite(value):
        raise ValueError("difference estimate must be finite")
    return DifferenceEstimate(value, step_value, "forward")


def centered_difference(
    function: Callable[[float], float], point: float, *, step: float | None = None
) -> DifferenceEstimate:
    """Use a heuristic step for an estimate, not an error certificate."""
    point_value = _require_finite(point, "point")
    step_value = _difference_step(point_value, step, 1 / 3)
    right = point_value + step_value
    left = point_value - step_value
    value = (_sample(function, right) - _sample(function, left)) / (2 * step_value)
    if not isfinite(value):
        raise ValueError("difference estimate must be finite")
    return DifferenceEstimate(value, step_value, "centered")
