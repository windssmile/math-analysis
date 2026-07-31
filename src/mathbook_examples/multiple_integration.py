"""Tensor-product midpoint integration with explicit approximation semantics."""

from dataclasses import dataclass
import math
from typing import Callable


@dataclass(frozen=True)
class Midpoint2DResult:
    """Record one fixed rectangular midpoint calculation."""

    value: float
    x_bounds: tuple[float, float]
    y_bounds: tuple[float, float]
    nx: int
    ny: int
    evaluations: int


def _positive_integer(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _increasing_bounds(
    bounds: object,
    name: str,
) -> tuple[float, float]:
    try:
        lower_raw, upper_raw = bounds  # type: ignore[misc]
        lower = float(lower_raw)
        upper = float(upper_raw)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{name} must contain two finite numbers") from error
    if not math.isfinite(lower) or not math.isfinite(upper):
        raise ValueError(f"{name} must contain two finite numbers")
    if not lower < upper:
        raise ValueError(f"{name} must be strictly increasing")
    return lower, upper


def tensor_midpoint_2d(
    function: Callable[[float, float], float],
    *,
    x_bounds: tuple[float, float],
    y_bounds: tuple[float, float],
    nx: int,
    ny: int,
) -> Midpoint2DResult:
    """Approximate a scalar integral on one finite, nondegenerate rectangle."""

    nx = _positive_integer(nx, "nx")
    ny = _positive_integer(ny, "ny")
    x0, x1 = _increasing_bounds(x_bounds, "x_bounds")
    y0, y1 = _increasing_bounds(y_bounds, "y_bounds")
    dx = (x1 - x0) / nx
    dy = (y1 - y0) / ny

    values: list[float] = []
    for i in range(nx):
        x = x0 + (i + 0.5) * dx
        for j in range(ny):
            y = y0 + (j + 0.5) * dy
            try:
                value = float(function(x, y))
            except (TypeError, ValueError, OverflowError) as error:
                raise ValueError(
                    "integrand must return a finite scalar"
                ) from error
            if not math.isfinite(value):
                raise ValueError("integrand must return a finite scalar")
            values.append(value)

    value = dx * dy * math.fsum(values)
    if not math.isfinite(value):
        raise ValueError("integral accumulation must be finite")
    return Midpoint2DResult(
        value=value,
        x_bounds=(x0, x1),
        y_bounds=(y0, y1),
        nx=nx,
        ny=ny,
        evaluations=nx * ny,
    )
