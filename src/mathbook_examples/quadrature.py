"""Composite quadrature with explicit conditional error-bound semantics.

The caller must prove that the supplied derivative bound holds on the whole
integration interval.  This module validates the numeric parameter but does
not verify function behavior: it does not verify the derivative bound from a
black-box function.  The analytic bounds exclude floating-point rounding and
external evaluation error.
"""

from collections.abc import Callable
from dataclasses import dataclass, replace
from math import ceil, exp, fsum, isfinite, log


class QuadratureEvaluationError(ValueError):
    """Report a failed or nonfinite black-box function evaluation."""


@dataclass(frozen=True)
class QuadratureResult:
    """Describe one fixed-grid or budgeted composite quadrature result."""

    method: str
    value: float
    subdivisions: int
    evaluations: int
    error_bound: float
    target_tolerance: float | None
    target_met: bool | None
    status: str


def _validate_interval(left: float, right: float) -> float:
    try:
        finite_endpoints = isfinite(left) and isfinite(right)
    except TypeError as error:
        raise ValueError("endpoints must be finite") from error
    if not finite_endpoints:
        raise ValueError("endpoints must be finite")
    if left >= right:
        raise ValueError("left endpoint must be smaller than right endpoint")
    width = right - left
    if not isfinite(width):
        raise ValueError("interval width must be finite")
    return width


def _validate_subdivisions(subdivisions: int, *, even: bool = False) -> None:
    if even:
        if (
            type(subdivisions) is not int
            or subdivisions <= 0
            or subdivisions % 2 != 0
        ):
            raise ValueError("subdivisions must be a positive even integer")
        return
    if type(subdivisions) is not int or subdivisions <= 0:
        raise ValueError("subdivisions must be a positive integer")


def _validate_derivative_bound(bound: float, name: str) -> None:
    try:
        valid = not isinstance(bound, bool) and isfinite(bound) and bound >= 0
    except TypeError as error:
        raise ValueError(f"{name} must be nonnegative and finite") from error
    if not valid:
        raise ValueError(f"{name} must be nonnegative and finite")


def _positive_finite(value: float, name: str) -> None:
    try:
        valid = not isinstance(value, bool) and isfinite(value) and value > 0
    except TypeError as error:
        raise ValueError(f"{name} must be positive and finite") from error
    if not valid:
        raise ValueError(f"{name} must be positive and finite")


def _sample(function: Callable[[float], float], point: float) -> float:
    try:
        raw_value = function(point)
    except Exception as error:
        raise QuadratureEvaluationError(
            f"function evaluation at x={point!r} failed"
        ) from error
    try:
        value = float(raw_value)
    except (TypeError, ValueError, OverflowError) as error:
        raise QuadratureEvaluationError(
            f"function value at x={point!r} must be finite"
        ) from error
    if not isfinite(value):
        raise QuadratureEvaluationError(
            f"function value at x={point!r} must be finite"
        )
    return value


def _finite_calculation(value: float, name: str) -> float:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _fixed_result(
    *,
    method: str,
    value: float,
    subdivisions: int,
    evaluations: int,
    error_bound: float,
) -> QuadratureResult:
    return QuadratureResult(
        method=method,
        value=_finite_calculation(value, "quadrature value"),
        subdivisions=subdivisions,
        evaluations=evaluations,
        error_bound=_finite_calculation(error_bound, "error bound"),
        target_tolerance=None,
        target_met=None,
        status="fixed_grid",
    )


def composite_midpoint(
    function: Callable[[float], float],
    left: float,
    right: float,
    subdivisions: int,
    second_derivative_bound: float,
) -> QuadratureResult:
    """Apply the uniform composite midpoint rule."""
    width = _validate_interval(left, right)
    _validate_subdivisions(subdivisions)
    _validate_derivative_bound(
        second_derivative_bound,
        "second_derivative_bound",
    )

    step = width / subdivisions
    samples = [
        _sample(function, left + (index + 0.5) * step)
        for index in range(subdivisions)
    ]
    try:
        value = step * fsum(samples)
        error_bound = width * second_derivative_bound * step**2 / 24.0
    except (OverflowError, ValueError) as error:
        raise ValueError("quadrature calculation must be finite") from error
    return _fixed_result(
        method="midpoint",
        value=value,
        subdivisions=subdivisions,
        evaluations=subdivisions,
        error_bound=error_bound,
    )


def composite_trapezoid(
    function: Callable[[float], float],
    left: float,
    right: float,
    subdivisions: int,
    second_derivative_bound: float,
) -> QuadratureResult:
    """Apply the uniform composite trapezoid rule."""
    width = _validate_interval(left, right)
    _validate_subdivisions(subdivisions)
    _validate_derivative_bound(
        second_derivative_bound,
        "second_derivative_bound",
    )

    step = width / subdivisions
    values = [
        _sample(function, left + index * step)
        for index in range(subdivisions + 1)
    ]
    try:
        weighted = 0.5 * values[0] + fsum(values[1:-1]) + 0.5 * values[-1]
        value = step * weighted
        error_bound = width * second_derivative_bound * step**2 / 12.0
    except (OverflowError, ValueError) as error:
        raise ValueError("quadrature calculation must be finite") from error
    return _fixed_result(
        method="trapezoid",
        value=value,
        subdivisions=subdivisions,
        evaluations=subdivisions + 1,
        error_bound=error_bound,
    )


def composite_simpson(
    function: Callable[[float], float],
    left: float,
    right: float,
    subdivisions: int,
    fourth_derivative_bound: float,
) -> QuadratureResult:
    """Apply the uniform composite Simpson rule."""
    width = _validate_interval(left, right)
    _validate_subdivisions(subdivisions, even=True)
    _validate_derivative_bound(
        fourth_derivative_bound,
        "fourth_derivative_bound",
    )

    step = width / subdivisions
    values = [
        _sample(function, left + index * step)
        for index in range(subdivisions + 1)
    ]
    try:
        weighted = values[0] + values[-1]
        weighted += 4.0 * fsum(
            values[index] for index in range(1, subdivisions, 2)
        )
        weighted += 2.0 * fsum(
            values[index] for index in range(2, subdivisions, 2)
        )
        value = step * weighted / 3.0
        error_bound = width * fourth_derivative_bound * step**4 / 180.0
    except (OverflowError, ValueError) as error:
        raise ValueError("quadrature calculation must be finite") from error
    return _fixed_result(
        method="simpson",
        value=value,
        subdivisions=subdivisions,
        evaluations=subdivisions + 1,
        error_bound=error_bound,
    )


def _simpson_bound(width: float, bound: float, subdivisions: int) -> float:
    step = width / subdivisions
    try:
        result = width * bound * step**4 / 180.0
    except OverflowError:
        return float("inf")
    return result


def _required_even_subdivisions(
    width: float,
    tolerance: float,
    bound: float,
    max_subintervals: int,
) -> int | None:
    if bound == 0:
        return 2

    log_requirement = (
        log(bound)
        + 5.0 * log(width)
        - log(180.0)
        - log(tolerance)
    ) / 4.0
    if log_requirement > log(max_subintervals):
        return None

    raw_requirement = exp(log_requirement)
    candidate = max(2, ceil(raw_requirement))
    if candidate % 2:
        candidate += 1

    while candidate > 2 and _simpson_bound(width, bound, candidate - 2) <= tolerance:
        candidate -= 2
    while _simpson_bound(width, bound, candidate) > tolerance:
        candidate += 2
        if candidate > max_subintervals:
            return None
    return candidate


def certified_simpson(
    function: Callable[[float], float],
    left: float,
    right: float,
    tolerance: float,
    fourth_derivative_bound: float,
    max_subintervals: int,
) -> QuadratureResult:
    """Choose an even Simpson grid under a finite evaluation budget."""
    width = _validate_interval(left, right)
    _positive_finite(tolerance, "tolerance")
    _validate_derivative_bound(
        fourth_derivative_bound,
        "fourth_derivative_bound",
    )
    if type(max_subintervals) is not int or max_subintervals < 2:
        raise ValueError("max_subintervals must be an integer at least 2")

    required = _required_even_subdivisions(
        width,
        tolerance,
        fourth_derivative_bound,
        max_subintervals,
    )
    subdivisions = (
        required
        if required is not None
        else max_subintervals - max_subintervals % 2
    )
    fixed = composite_simpson(
        function,
        left,
        right,
        subdivisions,
        fourth_derivative_bound,
    )
    target_met = fixed.error_bound <= tolerance
    return replace(
        fixed,
        target_tolerance=tolerance,
        target_met=target_met,
        status="target_met" if target_met else "budget_exhausted",
    )
