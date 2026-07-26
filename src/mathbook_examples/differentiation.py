"""Finite Taylor evaluation and uncertified numerical differentiation."""

from collections.abc import Sequence
from math import isfinite


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
