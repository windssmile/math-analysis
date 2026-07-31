"""Certificate-aware real Gamma and Beta integral approximations."""

from dataclasses import dataclass
from math import exp, isfinite, log

from .quadrature import certified_simpson, composite_midpoint


@dataclass(frozen=True)
class ParametricIntegralResult:
    value: float
    truncation: tuple[float, float]
    endpoint_error_bound: float
    quadrature_error_bound: float | None
    total_error_bound: float | None
    evaluations: int
    status: str
    target_met: bool


def _positive(value: float, name: str) -> float:
    try:
        valid = not isinstance(value, bool) and isfinite(value) and value > 0
    except TypeError as error:
        raise ValueError(f"{name} must be positive and finite") from error
    if not valid:
        raise ValueError(f"{name} must be positive and finite")
    return float(value)


def _budget(value: int) -> int:
    if type(value) is not int or value < 2:
        raise ValueError("max_subintervals must be an integer at least 2")
    return value


def _bound(value: float | None) -> float | None:
    if value is None:
        return None
    try:
        valid = not isinstance(value, bool) and isfinite(value) and value >= 0
    except TypeError as error:
        raise ValueError("fourth_derivative_bound must be nonnegative and finite") from error
    if not valid:
        raise ValueError("fourth_derivative_bound must be nonnegative and finite")
    return float(value)


def _finish(function, left, right, endpoint_bound, tolerance, budget, bound):
    regular_tolerance = tolerance - endpoint_bound
    if bound is None:
        diagnostic = composite_midpoint(function, left, right, budget, 0.0)
        return ParametricIntegralResult(
            diagnostic.value, (left, right), endpoint_bound, None, None,
            diagnostic.evaluations, "uncertified", False,
        )
    regular = certified_simpson(
        function, left, right, regular_tolerance, bound, budget
    )
    total = endpoint_bound + regular.error_bound
    met = total <= tolerance
    return ParametricIntegralResult(
        regular.value, (left, right), endpoint_bound, regular.error_bound, total,
        regular.evaluations, "target_met" if met else "budget_exhausted", met,
    )


def gamma_integral(
    parameter: float,
    tolerance: float,
    max_subintervals: int,
    *,
    fourth_derivative_bound: float | None = None,
) -> ParametricIntegralResult:
    """Approximate Gamma(parameter) with analytic truncation bounds."""
    p = _positive(parameter, "parameter")
    tol = _positive(tolerance, "tolerance")
    budget = _budget(max_subintervals)
    bound = _bound(fourth_derivative_bound)

    tail_budget = tol / 4.0
    left = min(0.5, exp(log(p * tail_budget) / p))
    left_bound = left**p / p

    right = max(2.0, 2.0 * max(p - 1.0, 1.0))
    while True:
        decay = 1.0 - (p - 1.0) / right
        right_bound = exp((p - 1.0) * log(right) - right) / decay
        if right_bound <= tail_budget:
            break
        right *= 2.0
        if not isfinite(right):
            raise ValueError("could not construct a finite Gamma truncation")

    function = lambda x: exp((p - 1.0) * log(x) - x)
    return _finish(
        function, left, right, left_bound + right_bound, tol, budget, bound
    )


def beta_integral(
    first_parameter: float,
    second_parameter: float,
    tolerance: float,
    max_subintervals: int,
    *,
    fourth_derivative_bound: float | None = None,
) -> ParametricIntegralResult:
    """Approximate Beta(first_parameter, second_parameter)."""
    p = _positive(first_parameter, "first_parameter")
    q = _positive(second_parameter, "second_parameter")
    tol = _positive(tolerance, "tolerance")
    budget = _budget(max_subintervals)
    bound = _bound(fourth_derivative_bound)

    epsilon = min(0.25, exp(log(min(p, q) * tol / 8.0) / min(p, q)))
    while True:
        left_factor = max(1.0, (1.0 - epsilon) ** (q - 1.0))
        right_factor = max(1.0, (1.0 - epsilon) ** (p - 1.0))
        left_bound = left_factor * epsilon**p / p
        right_bound = right_factor * epsilon**q / q
        if left_bound + right_bound <= tol / 2.0:
            break
        epsilon /= 2.0

    function = lambda x: exp(
        (p - 1.0) * log(x) + (q - 1.0) * log(1.0 - x)
    )
    return _finish(
        function, epsilon, 1.0 - epsilon, left_bound + right_bound,
        tol, budget, bound,
    )
