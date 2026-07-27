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
