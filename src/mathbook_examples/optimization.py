"""Dependency-free optimization examples with explicit diagnostic semantics."""

from dataclasses import dataclass
import math
from typing import Callable, Iterable


Vector = tuple[float, ...]
Matrix = tuple[tuple[float, ...], ...]


@dataclass(frozen=True)
class OptimizationResult:
    point: Vector
    converged: bool
    iterations: int
    reason: str
    objective: float
    gradient_norm: float
    last_step_norm: float | None
    hessian_status: str | None
    trace: tuple[Vector, ...]


@dataclass(frozen=True)
class EqualityCandidateCheck:
    stationarity_residual: Vector
    stationarity_norm: float
    constraint_residual: Vector
    constraint_norm: float


def _vector(values: Iterable[float], field: str, size: int | None = None) -> Vector:
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


def _matrix(values: Iterable[Iterable[float]], field: str, rows: int, columns: int) -> Matrix:
    try:
        result = tuple(tuple(float(value) for value in row) for row in values)
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError(f"{field} must be a finite matrix") from error
    if len(result) != rows or any(len(row) != columns for row in result):
        raise ValueError(f"{field} must have shape {rows} by {columns}")
    if not all(math.isfinite(value) for row in result for value in row):
        raise ValueError(f"{field} must contain finite numbers")
    return result


def _positive(value: float, field: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0.0:
        raise ValueError(f"{field} must be positive and finite")
    return number


def _objective(function: Callable[[Vector], float], point: Vector) -> float:
    try:
        value = float(function(point))
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError("objective must return a finite number") from error
    if not math.isfinite(value):
        raise ValueError("objective must return a finite number")
    return value


def _norm(vector: Vector) -> float:
    return math.sqrt(sum(value * value for value in vector))


def _solve(matrix: Matrix, right: Vector) -> Vector | None:
    size = len(matrix)
    augmented = [list(matrix[row]) + [right[row]] for row in range(size)]
    scale = max(abs(value) for row in matrix for value in row)
    threshold = math.ulp(1.0) * max(1.0, scale) * size
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) <= threshold:
            return None
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        for row in range(column + 1, size):
            factor = augmented[row][column] / augmented[column][column]
            for entry in range(column, size + 1):
                augmented[row][entry] -= factor * augmented[column][entry]
    answer = [0.0] * size
    for row in range(size - 1, -1, -1):
        answer[row] = (
            augmented[row][size]
            - sum(augmented[row][column] * answer[column] for column in range(row + 1, size))
        ) / augmented[row][row]
    return tuple(answer) if all(math.isfinite(value) for value in answer) else None


def _hessian_status(matrix: Matrix) -> str:
    size = len(matrix)
    scale = max(abs(value) for row in matrix for value in row)
    tolerance = math.ulp(1.0) * max(1.0, scale) * size
    for row in range(size):
        for column in range(size):
            if abs(matrix[row][column] - matrix[column][row]) > tolerance:
                return "indefinite"
    lower = [[0.0] * size for _ in range(size)]
    for row in range(size):
        for column in range(row + 1):
            value = matrix[row][column] - sum(
                lower[row][index] * lower[column][index] for index in range(column)
            )
            if row == column:
                if value < -tolerance:
                    return "indefinite"
                if value <= tolerance:
                    return "singular"
                lower[row][column] = math.sqrt(value)
            else:
                lower[row][column] = value / lower[column][column]
    return "positive_definite"


def _result(
    point: Vector,
    converged: bool,
    iterations: int,
    reason: str,
    objective: float,
    gradient_norm: float,
    last_step_norm: float | None,
    hessian_status: str | None,
    trace: list[Vector],
) -> OptimizationResult:
    return OptimizationResult(
        point, converged, iterations, reason, objective, gradient_norm,
        last_step_norm, hessian_status, tuple(trace)
    )


def gradient_descent(
    objective: Callable[[Vector], float],
    gradient: Callable[[Vector], Iterable[float]],
    initial: Iterable[float],
    *,
    initial_step: float = 1.0,
    backtracking_factor: float = 0.5,
    armijo: float = 1e-4,
    gradient_tolerance: float = 1e-8,
    step_tolerance: float = 1e-12,
    max_iterations: int = 1000,
) -> OptimizationResult:
    point = _vector(initial, "initial")
    initial_step = _positive(initial_step, "initial_step")
    gradient_tolerance = _positive(gradient_tolerance, "gradient_tolerance")
    step_tolerance = _positive(step_tolerance, "step_tolerance")
    if not math.isfinite(backtracking_factor) or not 0.0 < backtracking_factor < 1.0:
        raise ValueError("backtracking_factor must lie strictly between zero and one")
    if not math.isfinite(armijo) or not 0.0 < armijo < 1.0:
        raise ValueError("armijo must lie strictly between zero and one")
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, int) or max_iterations <= 0:
        raise ValueError("max_iterations must be a positive integer")
    value = _objective(objective, point)
    grad = _vector(gradient(point), "gradient", len(point))
    grad_norm = _norm(grad)
    trace = [point]
    if grad_norm <= gradient_tolerance:
        return _result(point, True, 0, "gradient", value, grad_norm, None, None, trace)
    last_step = None
    for iteration in range(1, max_iterations + 1):
        direction = tuple(-entry for entry in grad)
        directional = -grad_norm * grad_norm
        alpha = initial_step
        candidate = point
        candidate_value = value
        accepted = False
        saw_nonfinite = False
        while alpha * grad_norm > step_tolerance:
            trial = tuple(point[index] + alpha * direction[index] for index in range(len(point)))
            if not all(math.isfinite(entry) for entry in trial):
                saw_nonfinite = True
                alpha *= backtracking_factor
                continue
            try:
                trial_value = _objective(objective, trial)
            except ValueError:
                saw_nonfinite = True
                alpha *= backtracking_factor
                continue
            if trial_value <= value + armijo * alpha * directional:
                candidate, candidate_value, accepted = trial, trial_value, True
                break
            alpha *= backtracking_factor
        if not accepted:
            reason = "nonfinite_value" if saw_nonfinite else "step"
            return _result(point, reason == "step", iteration - 1, reason, value, grad_norm, last_step, None, trace)
        step = tuple(candidate[index] - point[index] for index in range(len(point)))
        last_step = _norm(step)
        point, value = candidate, candidate_value
        trace.append(point)
        try:
            grad = _vector(gradient(point), "gradient", len(point))
        except ValueError:
            return _result(trace[-2], False, iteration - 1, "nonfinite_value", trace and _objective(objective, trace[-2]), grad_norm, last_step, None, trace[:-1])
        grad_norm = _norm(grad)
        if grad_norm <= gradient_tolerance:
            return _result(point, True, iteration, "gradient", value, grad_norm, last_step, None, trace)
        if last_step <= step_tolerance:
            return _result(point, True, iteration, "step", value, grad_norm, last_step, None, trace)
    return _result(point, False, max_iterations, "max_iterations", value, grad_norm, last_step, None, trace)


def newton_optimize(
    objective: Callable[[Vector], float],
    gradient: Callable[[Vector], Iterable[float]],
    hessian: Callable[[Vector], Iterable[Iterable[float]]],
    initial: Iterable[float],
    *,
    gradient_tolerance: float = 1e-8,
    step_tolerance: float = 1e-12,
    max_iterations: int = 100,
    require_positive_definite: bool = True,
) -> OptimizationResult:
    point = _vector(initial, "initial")
    gradient_tolerance = _positive(gradient_tolerance, "gradient_tolerance")
    step_tolerance = _positive(step_tolerance, "step_tolerance")
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, int) or max_iterations <= 0:
        raise ValueError("max_iterations must be a positive integer")
    value = _objective(objective, point)
    grad = _vector(gradient(point), "gradient", len(point))
    grad_norm = _norm(grad)
    trace = [point]
    if grad_norm <= gradient_tolerance:
        return _result(point, True, 0, "gradient", value, grad_norm, None, None, trace)
    last_step = None
    last_status = None
    for iteration in range(1, max_iterations + 1):
        try:
            matrix = _matrix(hessian(point), "hessian", len(point), len(point))
        except ValueError as error:
            if "shape" in str(error):
                raise
            return _result(point, False, iteration - 1, "nonfinite_value", value, grad_norm, last_step, None, trace)
        last_status = _hessian_status(matrix)
        if last_status == "singular":
            return _result(point, False, iteration - 1, "singular_hessian", value, grad_norm, last_step, last_status, trace)
        if require_positive_definite and last_status != "positive_definite":
            return _result(point, False, iteration - 1, "indefinite_hessian", value, grad_norm, last_step, last_status, trace)
        direction = _solve(matrix, tuple(-entry for entry in grad))
        if direction is None:
            return _result(point, False, iteration - 1, "singular_hessian", value, grad_norm, last_step, "singular", trace)
        if sum(grad[index] * direction[index] for index in range(len(point))) >= 0.0:
            return _result(point, False, iteration - 1, "non_descent_direction", value, grad_norm, last_step, last_status, trace)
        candidate = tuple(point[index] + direction[index] for index in range(len(point)))
        try:
            candidate_value = _objective(objective, candidate)
            candidate_grad = _vector(gradient(candidate), "gradient", len(point))
        except ValueError:
            return _result(point, False, iteration - 1, "nonfinite_value", value, grad_norm, last_step, last_status, trace)
        point, value, grad = candidate, candidate_value, candidate_grad
        grad_norm = _norm(grad)
        last_step = _norm(direction)
        trace.append(point)
        if grad_norm <= gradient_tolerance:
            return _result(point, True, iteration, "gradient", value, grad_norm, last_step, last_status, trace)
        if last_step <= step_tolerance:
            return _result(point, True, iteration, "step", value, grad_norm, last_step, last_status, trace)
    return _result(point, False, max_iterations, "max_iterations", value, grad_norm, last_step, last_status, trace)


def check_equality_candidate(
    gradient: Callable[[Vector], Iterable[float]],
    constraint_jacobian: Callable[[Vector], Iterable[Iterable[float]]],
    point: Iterable[float],
    multipliers: Iterable[float],
    *,
    constraints: Callable[[Vector], Iterable[float]] | None = None,
) -> EqualityCandidateCheck:
    normalized_point = _vector(point, "point")
    grad = _vector(gradient(normalized_point), "gradient", len(normalized_point))
    try:
        normalized_multipliers = tuple(float(value) for value in multipliers)
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError("multipliers must contain finite numbers") from error
    if not normalized_multipliers or not all(math.isfinite(value) for value in normalized_multipliers):
        raise ValueError("multipliers must be nonempty and finite")
    jacobian = _matrix(
        constraint_jacobian(normalized_point),
        "constraint_jacobian",
        len(normalized_multipliers),
        len(normalized_point),
    )
    stationarity = tuple(
        grad[column]
        + sum(jacobian[row][column] * normalized_multipliers[row] for row in range(len(jacobian)))
        for column in range(len(normalized_point))
    )
    if constraints is None:
        residual = tuple(0.0 for _ in normalized_multipliers)
    else:
        residual = _vector(constraints(normalized_point), "constraints", len(normalized_multipliers))
    return EqualityCandidateCheck(stationarity, _norm(stationarity), residual, _norm(residual))
