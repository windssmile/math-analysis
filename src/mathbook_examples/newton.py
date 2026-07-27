"""Pure and safeguarded Newton iterations with explicit certificate semantics."""

from collections.abc import Callable
from dataclasses import dataclass
from math import inf, isfinite


@dataclass(frozen=True)
class NewtonResult:
    """Describe a Newton-family exit without conflating stops and certificates."""

    value: float
    converged: bool
    certified: bool
    iterations: int
    reason: str
    residual: float
    last_step: float | None
    bracket: tuple[float, float] | None
    error_bound: float | None
    step_types: tuple[str, ...]


def _positive_finite(value: float, name: str) -> None:
    if not isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be positive and finite")


def _iteration_budget(value: int) -> None:
    if type(value) is not int or value <= 0:
        raise ValueError("max_iterations must be a positive integer")


def _failure(
    value: float,
    iterations: int,
    reason: str,
    residual: float,
    last_step: float | None,
    step_types: list[str],
) -> NewtonResult:
    return NewtonResult(
        value=value,
        converged=False,
        certified=False,
        iterations=iterations,
        reason=reason,
        residual=residual,
        last_step=last_step,
        bracket=None,
        error_bound=None,
        step_types=tuple(step_types),
    )


def _pure_success(
    value: float,
    iterations: int,
    reason: str,
    residual: float,
    last_step: float | None,
    step_types: list[str],
) -> NewtonResult:
    return NewtonResult(
        value=value,
        converged=True,
        certified=False,
        iterations=iterations,
        reason=reason,
        residual=residual,
        last_step=last_step,
        bracket=None,
        error_bound=None,
        step_types=tuple(step_types),
    )


def _midpoint(left: float, right: float) -> float:
    """Return a finite midpoint without overflowing opposite-sign endpoints."""
    if left < 0.0 < right:
        return (left + right) / 2.0
    return left + (right - left) / 2.0


def _half_width(left: float, midpoint: float, right: float) -> float:
    """Bound the midpoint's distance to either bracket endpoint."""
    return max(midpoint - left, right - midpoint)


def _same_sign(first: float, second: float) -> bool:
    return (first > 0.0) == (second > 0.0)


def _safeguarded_result(
    *,
    value: float,
    converged: bool,
    certified: bool,
    reason: str,
    residual: float,
    last_step: float | None,
    bracket: tuple[float, float],
    error_bound: float | None,
    step_types: list[str],
) -> NewtonResult:
    return NewtonResult(
        value=value,
        converged=converged,
        certified=certified,
        iterations=len(step_types),
        reason=reason,
        residual=residual,
        last_step=last_step,
        bracket=bracket,
        error_bound=error_bound,
        step_types=tuple(step_types),
    )


def _finite_endpoint_value(
    function: Callable[[float], float], point: float, location: str
) -> float:
    value = function(point)
    if not isfinite(value):
        raise ValueError(f"function value at {location} endpoint must be finite")
    return value


def _finite_midpoint_result(
    function: Callable[[float], float],
    left: float,
    right: float,
    *,
    converged: bool,
    reason: str,
    last_step: float | None,
    step_types: list[str],
) -> NewtonResult:
    midpoint = _midpoint(left, right)
    midpoint_value = function(midpoint)
    if not isfinite(midpoint_value):
        return _safeguarded_result(
            value=midpoint,
            converged=False,
            certified=False,
            reason="nonfinite_value",
            residual=inf,
            last_step=last_step,
            bracket=(left, right),
            error_bound=None,
            step_types=step_types,
        )
    return _safeguarded_result(
        value=midpoint,
        converged=converged,
        certified=True,
        reason=reason,
        residual=abs(midpoint_value),
        last_step=last_step,
        bracket=(left, right),
        error_bound=_half_width(left, midpoint, right),
        step_types=step_types,
    )


def newton(
    function: Callable[[float], float],
    derivative: Callable[[float], float],
    initial: float,
    *,
    residual_tolerance: float = 1e-12,
    step_tolerance: float = 1e-12,
    derivative_tolerance: float = 1e-14,
    max_iterations: int = 50,
) -> NewtonResult:
    """Run pure Newton iteration.

    Residual and step tolerances are heuristic stop signals, not root-error
    certificates.  Function-domain exceptions raised by the caller are
    preserved.
    """
    if not isfinite(initial):
        raise ValueError("initial must be finite")
    _positive_finite(residual_tolerance, "residual_tolerance")
    _positive_finite(step_tolerance, "step_tolerance")
    _positive_finite(derivative_tolerance, "derivative_tolerance")
    _iteration_budget(max_iterations)

    point = initial
    function_value = function(point)
    if not isfinite(function_value):
        return _failure(point, 0, "nonfinite_value", inf, None, [])

    residual = abs(function_value)
    if residual <= residual_tolerance:
        return _pure_success(point, 0, "residual", residual, None, [])

    step_types: list[str] = []
    last_step: float | None = None
    for _ in range(max_iterations):
        derivative_value = derivative(point)
        if not isfinite(derivative_value):
            return _failure(
                point,
                len(step_types),
                "nonfinite_value",
                residual,
                last_step,
                step_types,
            )
        if abs(derivative_value) <= derivative_tolerance:
            return _failure(
                point,
                len(step_types),
                "derivative_too_small",
                residual,
                last_step,
                step_types,
            )

        candidate = point - function_value / derivative_value
        if not isfinite(candidate):
            return _failure(
                point,
                len(step_types),
                "nonfinite_value",
                residual,
                last_step,
                step_types,
            )

        candidate_value = function(candidate)
        if not isfinite(candidate_value):
            return _failure(
                point,
                len(step_types),
                "nonfinite_value",
                residual,
                last_step,
                step_types,
            )

        last_step = abs(candidate - point)
        point = candidate
        function_value = candidate_value
        residual = abs(function_value)
        step_types.append("newton")
        iterations = len(step_types)

        if residual <= residual_tolerance:
            return _pure_success(
                point,
                iterations,
                "residual",
                residual,
                last_step,
                step_types,
            )
        if last_step <= step_tolerance:
            return _pure_success(
                point,
                iterations,
                "step",
                residual,
                last_step,
                step_types,
            )

    return _failure(
        point,
        len(step_types),
        "max_iterations",
        residual,
        last_step,
        step_types,
    )


def safeguarded_newton(
    function: Callable[[float], float],
    derivative: Callable[[float], float],
    left: float,
    right: float,
    *,
    interval_tolerance: float = 1e-10,
    derivative_tolerance: float = 1e-14,
    max_iterations: int = 100,
) -> NewtonResult:
    """Run Newton steps inside a sign-changing bracket.

    A certified result is conditional on the caller having proved that
    ``function`` is continuous throughout the initial bracket.  The program
    checks finite endpoint values and their sign change, but finite sampling
    cannot establish continuity.
    """
    _positive_finite(interval_tolerance, "interval_tolerance")
    _positive_finite(derivative_tolerance, "derivative_tolerance")
    _iteration_budget(max_iterations)
    if not isfinite(left) or not isfinite(right):
        raise ValueError("endpoints must be finite")
    if left >= right:
        raise ValueError("left endpoint must be smaller than right endpoint")

    left_value = _finite_endpoint_value(function, left, "left")
    right_value = _finite_endpoint_value(function, right, "right")
    if left_value == 0:
        return _safeguarded_result(
            value=left,
            converged=True,
            certified=True,
            reason="endpoint",
            residual=0.0,
            last_step=None,
            bracket=(left, left),
            error_bound=0.0,
            step_types=[],
        )
    if right_value == 0:
        return _safeguarded_result(
            value=right,
            converged=True,
            certified=True,
            reason="endpoint",
            residual=0.0,
            last_step=None,
            bracket=(right, right),
            error_bound=0.0,
            step_types=[],
        )
    if _same_sign(left_value, right_value):
        raise ValueError("endpoint values must have opposite signs")

    if right - left <= interval_tolerance:
        return _finite_midpoint_result(
            function,
            left,
            right,
            converged=True,
            reason="bracket",
            last_step=None,
            step_types=[],
        )

    if abs(left_value) <= abs(right_value):
        point = left
        function_value = left_value
    else:
        point = right
        function_value = right_value

    step_types: list[str] = []
    last_step: float | None = None
    for _ in range(max_iterations):
        midpoint = _midpoint(left, right)
        central_left = _midpoint(left, midpoint)
        central_right = _midpoint(midpoint, right)

        derivative_value = derivative(point)
        step_type = "bisection"
        candidate = midpoint
        if isfinite(derivative_value) and abs(derivative_value) > derivative_tolerance:
            newton_candidate = point - function_value / derivative_value
            if (
                isfinite(newton_candidate)
                and central_left <= newton_candidate <= central_right
            ):
                candidate = newton_candidate
                step_type = "newton"

        candidate_value = function(candidate)
        if not isfinite(candidate_value) and step_type == "newton":
            candidate = midpoint
            candidate_value = function(candidate)
            step_type = "bisection"
        if not isfinite(candidate_value):
            return _safeguarded_result(
                value=midpoint,
                converged=False,
                certified=False,
                reason="nonfinite_value",
                residual=inf,
                last_step=last_step,
                bracket=(left, right),
                error_bound=None,
                step_types=step_types,
            )

        last_step = abs(candidate - point)
        step_types.append(step_type)
        if candidate_value == 0:
            return _safeguarded_result(
                value=candidate,
                converged=True,
                certified=True,
                reason="endpoint",
                residual=0.0,
                last_step=last_step,
                bracket=(candidate, candidate),
                error_bound=0.0,
                step_types=step_types,
            )

        if _same_sign(left_value, candidate_value):
            left = candidate
            left_value = candidate_value
        else:
            right = candidate
            right_value = candidate_value

        point = candidate
        function_value = candidate_value
        if right - left <= interval_tolerance:
            return _finite_midpoint_result(
                function,
                left,
                right,
                converged=True,
                reason="bracket",
                last_step=last_step,
                step_types=step_types,
            )

    return _finite_midpoint_result(
        function,
        left,
        right,
        converged=False,
        reason="max_iterations",
        last_step=last_step,
        step_types=step_types,
    )
