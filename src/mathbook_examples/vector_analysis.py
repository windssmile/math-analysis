"""Oriented composite-midpoint line and flux integral approximations."""

from dataclasses import dataclass
import math
from typing import Callable, Iterable


Vector = tuple[float, ...]


@dataclass(frozen=True)
class LineIntegralResult:
    """Record one fixed composite-midpoint line integral calculation."""

    value: float
    bounds: tuple[float, float]
    n: int
    evaluations: int


@dataclass(frozen=True)
class FluxIntegralResult:
    """Record one fixed tensor midpoint flux integral calculation."""

    value: float
    u_bounds: tuple[float, float]
    v_bounds: tuple[float, float]
    nu: int
    nv: int
    evaluations: int


def _positive_integer(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _increasing_bounds(bounds: object, name: str) -> tuple[float, float]:
    try:
        lower_raw, upper_raw = bounds  # type: ignore[misc]
        lower, upper = float(lower_raw), float(upper_raw)
    except Exception as error:
        raise ValueError(f"{name} must contain two finite numbers") from error
    if not math.isfinite(lower) or not math.isfinite(upper):
        raise ValueError(f"{name} must contain two finite numbers")
    if not lower < upper:
        raise ValueError(f"{name} must be strictly increasing")
    return lower, upper


def _vector(callback: Callable[..., object], arguments: tuple[float, ...], name: str) -> Vector:
    try:
        vector = tuple(float(component) for component in callback(*arguments))  # type: ignore[union-attr]
    except Exception as error:
        raise ValueError(f"{name} must return a finite vector") from error
    if not all(math.isfinite(component) for component in vector):
        raise ValueError(f"{name} must return a finite vector")
    return vector


def _finite_fsum(values: Iterable[float], message: str) -> float:
    try:
        total = math.fsum(values)
    except OverflowError as error:
        raise ValueError(message) from error
    if not math.isfinite(total):
        raise ValueError(message)
    return total


def _finite_product(factors: Iterable[float], message: str) -> float:
    factors = tuple(factors)
    if not all(math.isfinite(factor) for factor in factors):
        raise ValueError(message)
    if any(factor == 0.0 for factor in factors):
        negative = sum(math.copysign(1.0, factor) < 0.0 for factor in factors) % 2
        return -0.0 if negative else 0.0
    mantissa = 1.0
    exponent = 0
    for factor in factors:
        factor_mantissa, factor_exponent = math.frexp(factor)
        mantissa, adjustment = math.frexp(mantissa * factor_mantissa)
        exponent += factor_exponent + adjustment
    try:
        product = math.ldexp(mantissa, exponent)
    except OverflowError as error:
        raise ValueError(message) from error
    if not math.isfinite(product):
        raise ValueError(message)
    return product


def composite_midpoint_line_integral(
    field: Callable[[Vector], object],
    *,
    curve: Callable[[float], object],
    curve_derivative: Callable[[float], object],
    bounds: tuple[float, float],
    n: int,
) -> LineIntegralResult:
    """Approximate ``integral F(r(t)) dot r'(t) dt`` without certification."""

    n = _positive_integer(n, "n")
    lower, upper = _increasing_bounds(bounds, "bounds")
    interval_length = upper - lower
    step = interval_length / n
    terms: list[float] = []
    for index in range(n):
        t = lower + (index + 0.5) * step
        point = _vector(curve, (t,), "curve")
        if len(point) not in (2, 3):
            raise ValueError("curve must return a 2- or 3-dimensional finite vector")
        derivative = _vector(curve_derivative, (t,), "curve_derivative")
        vector_field = _vector(field, (point,), "field")
        if len(derivative) != len(point) or len(vector_field) != len(point):
            raise ValueError("field, curve, and curve_derivative must have the same dimension")
        term = _finite_fsum(
            (a * b for a, b in zip(vector_field, derivative)),
            "line dot product must be finite",
        )
        terms.append(
            _finite_product(
                (term, 1.0 / n), "integral accumulation must be finite"
            )
        )
    value = _finite_product(
        (
            interval_length,
            _finite_fsum(terms, "integral accumulation must be finite"),
        ),
        "integral accumulation must be finite",
    )
    return LineIntegralResult(value, (lower, upper), n, n)


def composite_midpoint_flux_integral(
    field: Callable[[Vector], object],
    *,
    surface: Callable[[float, float], object],
    surface_u: Callable[[float, float], object],
    surface_v: Callable[[float, float], object],
    u_bounds: tuple[float, float],
    v_bounds: tuple[float, float],
    nu: int,
    nv: int,
) -> FluxIntegralResult:
    """Approximate flux at fixed midpoints without certification."""

    nu = _positive_integer(nu, "nu")
    nv = _positive_integer(nv, "nv")
    u0, u1 = _increasing_bounds(u_bounds, "u_bounds")
    v0, v1 = _increasing_bounds(v_bounds, "v_bounds")
    u_length, v_length = u1 - u0, v1 - v0
    du, dv = u_length / nu, v_length / nv
    terms: list[float] = []
    for i in range(nu):
        u = u0 + (i + 0.5) * du
        for j in range(nv):
            v = v0 + (j + 0.5) * dv
            point = _vector(surface, (u, v), "surface")
            tangent_u = _vector(surface_u, (u, v), "surface_u")
            tangent_v = _vector(surface_v, (u, v), "surface_v")
            vector_field = _vector(field, (point,), "field")
            if any(len(vector) != 3 for vector in (point, tangent_u, tangent_v, vector_field)):
                raise ValueError("field, surface, surface_u, and surface_v must be 3-dimensional")
            ux, uy, uz = tangent_u
            vx, vy, vz = tangent_v
            normal = (uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx)
            if not all(math.isfinite(component) for component in normal):
                raise ValueError("surface normal must be finite")
            if normal == (0.0, 0.0, 0.0):
                raise ValueError("surface_u and surface_v must define a nondegenerate normal")
            term = _finite_fsum(
                (a * b for a, b in zip(vector_field, normal)),
                "flux dot product must be finite",
            )
            terms.append(
                _finite_product(
                    (term, 1.0 / nu, 1.0 / nv),
                    "integral accumulation must be finite",
                )
            )
    value = _finite_product(
        (
            u_length,
            v_length,
            _finite_fsum(terms, "integral accumulation must be finite"),
        ),
        "integral accumulation must be finite",
    )
    return FluxIntegralResult(value, (u0, u1), (v0, v1), nu, nv, nu * nv)
