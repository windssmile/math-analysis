"""Finite-dimensional Jacobian diagnostics with explicit non-certificate semantics."""

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from math import isfinite


Vector = tuple[float, ...]
Matrix = tuple[tuple[float, ...], ...]


@dataclass(frozen=True)
class JacobianCheck:
    """Keep analytic and numerical Jacobians separate from differentiability proofs."""

    analytic: Matrix
    finite_difference: Matrix
    max_abs_difference: float
    step: float
    condition_estimate: float | None
    status: str
    assumptions: tuple[str, ...]


def _positive_finite(value: float, name: str) -> None:
    if not isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be positive and finite")


def _finite_vector(values: Iterable[float], name: str) -> Vector:
    vector = tuple(values)
    if not vector:
        raise ValueError(f"{name} must be nonempty")
    if not all(type(value) in (int, float) and isfinite(value) for value in vector):
        raise ValueError(f"{name} values must be finite")
    return tuple(float(value) for value in vector)


def _function_value(
    function: Callable[[Vector], Iterable[float]],
    point: Vector,
    expected_dimension: int | None = None,
) -> Vector:
    value = tuple(function(point))
    if expected_dimension is not None and len(value) != expected_dimension:
        raise ValueError("function output dimension changed")
    if not value:
        raise ValueError("function output must be nonempty")
    if not all(type(entry) in (int, float) and isfinite(entry) for entry in value):
        raise ValueError("function values must be finite")
    return tuple(float(entry) for entry in value)


def _analytic_matrix(
    jacobian: Callable[[Vector], Iterable[Iterable[float]]],
    point: Vector,
    output_dimension: int,
) -> Matrix:
    rows = tuple(tuple(row) for row in jacobian(point))
    if len(rows) != output_dimension:
        raise ValueError("jacobian row count must match output dimension")
    if any(len(row) != len(point) for row in rows):
        raise ValueError("jacobian column count must match point dimension")
    if not all(
        type(value) in (int, float) and isfinite(value)
        for row in rows
        for value in row
    ):
        raise ValueError("jacobian values must be finite")
    return tuple(tuple(float(value) for value in row) for row in rows)


def _central_difference(
    function: Callable[[Vector], Iterable[float]],
    point: Vector,
    output_dimension: int,
    step: float,
) -> Matrix:
    columns: list[Vector] = []
    for column in range(len(point)):
        plus = list(point)
        minus = list(point)
        plus[column] += step
        minus[column] -= step
        plus_value = _function_value(function, tuple(plus), output_dimension)
        minus_value = _function_value(function, tuple(minus), output_dimension)
        columns.append(
            tuple(
                (plus_value[row] - minus_value[row]) / (2.0 * step)
                for row in range(output_dimension)
            )
        )
    return tuple(
        tuple(columns[column][row] for column in range(len(point)))
        for row in range(output_dimension)
    )


def _matrix_inf_norm(matrix: Matrix) -> float:
    return max(sum(abs(value) for value in row) for row in matrix)


def _inverse(matrix: Matrix) -> Matrix | None:
    size = len(matrix)
    augmented = [
        list(row) + [1.0 if row_index == column else 0.0 for column in range(size)]
        for row_index, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot_row = max(range(column, size), key=lambda row: abs(augmented[row][column]))
        pivot = augmented[pivot_row][column]
        if abs(pivot) <= 1e-15:
            return None
        augmented[column], augmented[pivot_row] = (
            augmented[pivot_row],
            augmented[column],
        )
        pivot = augmented[column][column]
        augmented[column] = [value / pivot for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(augmented[row], augmented[column])
            ]
    inverse = tuple(tuple(row[size:]) for row in augmented)
    if not all(isfinite(value) for row in inverse for value in row):
        return None
    return inverse


def check_jacobian(
    function: Callable[[Vector], Iterable[float]],
    jacobian: Callable[[Vector], Iterable[Iterable[float]]],
    point: Iterable[float],
    *,
    step: float = 1e-6,
    condition_limit: float = 1e12,
) -> JacobianCheck:
    """Compare an analytic Jacobian with central differences.

    Agreement is a diagnostic only.  It neither proves Fréchet differentiability
    nor certifies the accuracy of the analytic Jacobian.
    """

    _positive_finite(step, "step")
    _positive_finite(condition_limit, "condition_limit")
    normalized_point = _finite_vector(point, "point")
    base_value = _function_value(function, normalized_point)
    analytic = _analytic_matrix(
        jacobian,
        normalized_point,
        len(base_value),
    )
    numerical = _central_difference(
        function,
        normalized_point,
        len(base_value),
        step,
    )
    max_difference = max(
        abs(analytic[row][column] - numerical[row][column])
        for row in range(len(analytic))
        for column in range(len(normalized_point))
    )

    condition_estimate: float | None = None
    status = "checked"
    if len(analytic) == len(normalized_point):
        inverse = _inverse(analytic)
        if inverse is None:
            status = "singular"
        else:
            condition_estimate = _matrix_inf_norm(analytic) * _matrix_inf_norm(inverse)
            if condition_estimate > condition_limit:
                status = "ill_conditioned"

    return JacobianCheck(
        analytic=analytic,
        finite_difference=numerical,
        max_abs_difference=max_difference,
        step=step,
        condition_estimate=condition_estimate,
        status=status,
        assumptions=(
            "analytic_jacobian_supplied_by_caller",
            "finite_difference_is_diagnostic",
            "agreement_does_not_prove_differentiability",
        ),
    )
