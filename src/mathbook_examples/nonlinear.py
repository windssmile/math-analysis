"""Small, dependency-free Newton solver for textbook nonlinear systems."""

from dataclasses import dataclass
import math
from typing import Callable, Iterable


Vector = tuple[float, ...]
Matrix = tuple[tuple[float, ...], ...]


@dataclass(frozen=True)
class SystemNewtonResult:
    point: Vector
    converged: bool
    iterations: int
    reason: str
    residual_norm: float
    last_step_norm: float | None
    jacobian_condition: float | None
    trace: tuple[Vector, ...]


def _positive_finite(value: float, field: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0.0:
        raise ValueError(f"{field} must be positive and finite")
    return number


def _vector(values: Iterable[float], field: str, *, size: int | None = None) -> Vector:
    try:
        result = tuple(float(value) for value in values)
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError(f"{field} must contain finite numbers") from error
    if not result or (size is not None and len(result) != size):
        expected = "nonempty" if size is None else f"length {size}"
        raise ValueError(f"{field} must be {expected}")
    if not all(math.isfinite(value) for value in result):
        raise ValueError(f"{field} must contain finite numbers")
    return result


def _matrix(values: Iterable[Iterable[float]], size: int) -> Matrix:
    try:
        rows = tuple(tuple(float(value) for value in row) for row in values)
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError("jacobian must be a finite square matrix") from error
    if len(rows) != size or any(len(row) != size for row in rows):
        raise ValueError(f"jacobian must have shape {size} by {size}")
    if not all(math.isfinite(value) for row in rows for value in row):
        raise ValueError("jacobian must contain finite numbers")
    return rows


def _norm(values: Vector) -> float:
    return max(abs(value) for value in values)


def _solve(matrix: Matrix, right: Vector) -> Vector | None:
    size = len(matrix)
    augmented = [list(matrix[row]) + [right[row]] for row in range(size)]
    scale = max((abs(value) for row in matrix for value in row), default=0.0)
    threshold = math.ulp(1.0) * max(1.0, scale) * size
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) <= threshold:
            return None
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        for row in range(column + 1, size):
            factor = augmented[row][column] / pivot_value
            for entry in range(column, size + 1):
                augmented[row][entry] -= factor * augmented[column][entry]
    solution = [0.0] * size
    for row in range(size - 1, -1, -1):
        numerator = augmented[row][size] - sum(
            augmented[row][column] * solution[column] for column in range(row + 1, size)
        )
        solution[row] = numerator / augmented[row][row]
    if not all(math.isfinite(value) for value in solution):
        return None
    return tuple(solution)


def _condition(matrix: Matrix) -> float | None:
    size = len(matrix)
    columns: list[Vector] = []
    for column in range(size):
        basis = tuple(1.0 if row == column else 0.0 for row in range(size))
        solution = _solve(matrix, basis)
        if solution is None:
            return None
        columns.append(solution)
    inverse_rows = tuple(tuple(columns[column][row] for column in range(size)) for row in range(size))
    matrix_norm = max(sum(abs(value) for value in row) for row in matrix)
    inverse_norm = max(sum(abs(value) for value in row) for row in inverse_rows)
    estimate = matrix_norm * inverse_norm
    return estimate if math.isfinite(estimate) else math.inf


def newton_system(
    function: Callable[[Vector], Iterable[float]],
    jacobian: Callable[[Vector], Iterable[Iterable[float]]],
    initial: Iterable[float],
    *,
    residual_tolerance: float = 1e-10,
    step_tolerance: float = 1e-10,
    condition_limit: float = 1e12,
    max_iterations: int = 50,
) -> SystemNewtonResult:
    """Apply pure Newton iteration and report explicit, uncertified stop reasons."""

    point = _vector(initial, "initial")
    residual_tolerance = _positive_finite(residual_tolerance, "residual_tolerance")
    step_tolerance = _positive_finite(step_tolerance, "step_tolerance")
    condition_limit = _positive_finite(condition_limit, "condition_limit")
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, int) or max_iterations <= 0:
        raise ValueError("max_iterations must be a positive integer")

    trace = [point]
    last_step: float | None = None
    last_condition: float | None = None
    try:
        residual = _vector(function(point), "function output", size=len(point))
    except ValueError:
        raise
    residual_norm = _norm(residual)
    if residual_norm <= residual_tolerance:
        return SystemNewtonResult(point, True, 0, "residual", residual_norm, None, None, tuple(trace))

    for iteration in range(1, max_iterations + 1):
        try:
            matrix = _matrix(jacobian(point), len(point))
        except ValueError as error:
            if "finite" not in str(error):
                raise
            return SystemNewtonResult(
                point, False, iteration - 1, "nonfinite_value", residual_norm, last_step, None, tuple(trace)
            )
        last_condition = _condition(matrix)
        if last_condition is None:
            return SystemNewtonResult(
                point, False, iteration - 1, "singular_jacobian", residual_norm, last_step, None, tuple(trace)
            )
        if last_condition > condition_limit:
            return SystemNewtonResult(
                point,
                False,
                iteration - 1,
                "ill_conditioned_jacobian",
                residual_norm,
                last_step,
                last_condition,
                tuple(trace),
            )
        step = _solve(matrix, tuple(-value for value in residual))
        if step is None:
            return SystemNewtonResult(
                point, False, iteration - 1, "singular_jacobian", residual_norm, last_step, None, tuple(trace)
            )
        candidate = tuple(point[index] + step[index] for index in range(len(point)))
        if not all(math.isfinite(value) for value in candidate):
            return SystemNewtonResult(
                point, False, iteration - 1, "nonfinite_value", residual_norm, last_step, last_condition, tuple(trace)
            )
        try:
            candidate_residual = _vector(function(candidate), "function output", size=len(point))
        except ValueError:
            return SystemNewtonResult(
                point, False, iteration - 1, "nonfinite_value", residual_norm, last_step, last_condition, tuple(trace)
            )
        point = candidate
        residual = candidate_residual
        residual_norm = _norm(residual)
        last_step = _norm(step)
        trace.append(point)
        if residual_norm <= residual_tolerance:
            return SystemNewtonResult(
                point, True, iteration, "residual", residual_norm, last_step, last_condition, tuple(trace)
            )
        if last_step <= step_tolerance:
            return SystemNewtonResult(
                point, True, iteration, "step", residual_norm, last_step, last_condition, tuple(trace)
            )

    return SystemNewtonResult(
        point,
        False,
        max_iterations,
        "max_iterations",
        residual_norm,
        last_step,
        last_condition,
        tuple(trace),
    )
