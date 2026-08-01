"""Finite Fourier illustrations; no result certifies an infinite series."""

from dataclasses import dataclass
from math import cos, fsum, isfinite, pi, sin
from numbers import Real
from typing import Callable, Iterable


@dataclass(frozen=True)
class FourierCoefficients:
    """Midpoint approximations to finitely many real Fourier coefficients."""

    a0: float
    cosine_coefficients: tuple[float, ...]
    sine_coefficients: tuple[float, ...]
    period: float
    harmonics: int
    panels: int
    method: str = "composite_midpoint"
    status: str = "finite_quadrature_only"


@dataclass(frozen=True)
class FourierValue:
    """One finite trigonometric value, not an infinite-series limit."""

    value: float
    order: int
    period: float
    method: str
    status: str = "finite_truncation_only"


def _finite_real(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number, not bool")
    converted = float(value)
    if not isfinite(converted):
        raise ValueError(f"{name} must be finite")
    return converted


def _nonnegative_integer(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer, not bool")
    if value < 0:
        raise ValueError(f"{name} must be nonnegative")
    return value


def _positive_period(value: object) -> float:
    period = _finite_real(value, "period")
    if period <= 0:
        raise ValueError("period must be positive")
    angular_frequency = 2.0 * pi / period
    if not isfinite(angular_frequency):
        raise ValueError("period is too small for finite angular frequency")
    return period


def _coefficient_tuple(values: Iterable[Real], name: str) -> tuple[float, ...]:
    if isinstance(values, (str, bytes)):
        raise TypeError(f"{name} must be a finite iterable of real coefficients")
    try:
        raw_values = list(values)
    except TypeError as exc:
        raise TypeError(f"{name} must be a finite iterable of real coefficients") from exc
    return tuple(_finite_real(value, f"{name}[{index}]")
                 for index, value in enumerate(raw_values))


def _finite_sum(terms: Iterable[float], name: str) -> float:
    try:
        result = fsum(terms)
    except OverflowError as exc:
        raise ValueError(f"{name} is not finite") from exc
    if not isfinite(result):
        raise ValueError(f"{name} is not finite")
    return result


def sampled_fourier_coefficients(
    function: Callable[[float], Real],
    period: Real,
    harmonics: int,
    panels: int,
) -> FourierCoefficients:
    """Approximate a finite coefficient list by centered composite midpoints."""

    if not callable(function):
        raise TypeError("function must be callable")
    numeric_period = _positive_period(period)
    harmonic_count = _nonnegative_integer(harmonics, "harmonics")
    panel_count = _nonnegative_integer(panels, "panels")
    if panel_count == 0:
        raise ValueError("panels must be positive")

    width = numeric_period / panel_count
    half_period = numeric_period / 2.0
    omega = 2.0 * pi / numeric_period
    points = [-half_period + (index + 0.5) * width for index in range(panel_count)]
    samples = []
    for index, point in enumerate(points):
        try:
            value = function(point)
        except Exception as exc:
            raise ValueError(f"function evaluation failed at panel {index}") from exc
        samples.append(_finite_real(value, f"function result at panel {index}"))

    scale = 2.0 / numeric_period

    def coefficient(weights: Iterable[float], name: str) -> float:
        midpoint_sum = _finite_sum(weights, f"{name} midpoint sum")
        integral = midpoint_sum * width
        result = integral * scale
        if not isfinite(integral) or not isfinite(result):
            raise ValueError(f"{name} is not finite")
        return result

    a0 = coefficient(samples, "a0")
    cosine_coefficients = []
    sine_coefficients = []
    for harmonic in range(1, harmonic_count + 1):
        cosine_coefficients.append(coefficient(
            (value * cos(harmonic * omega * point)
             for point, value in zip(points, samples, strict=True)),
            f"cosine coefficient {harmonic}",
        ))
        sine_coefficients.append(coefficient(
            (value * sin(harmonic * omega * point)
             for point, value in zip(points, samples, strict=True)),
            f"sine coefficient {harmonic}",
        ))

    return FourierCoefficients(
        a0=a0,
        cosine_coefficients=tuple(cosine_coefficients),
        sine_coefficients=tuple(sine_coefficients),
        period=numeric_period,
        harmonics=harmonic_count,
        panels=panel_count,
    )


def _finite_fourier_value(
    x: Real,
    a0: Real,
    cosine_coefficients: Iterable[Real],
    sine_coefficients: Iterable[Real],
    period: Real,
    *,
    fejer: bool,
) -> FourierValue:
    numeric_x = _finite_real(x, "x")
    numeric_a0 = _finite_real(a0, "a0")
    numeric_period = _positive_period(period)
    cosine_values = _coefficient_tuple(cosine_coefficients, "cosine_coefficients")
    sine_values = _coefficient_tuple(sine_coefficients, "sine_coefficients")
    if len(cosine_values) != len(sine_values):
        raise ValueError("cosine and sine coefficient lengths must match")

    order = len(cosine_values)
    omega = 2.0 * pi / numeric_period
    terms = [numeric_a0 / 2.0]
    for harmonic, (a_n, b_n) in enumerate(
        zip(cosine_values, sine_values, strict=True), start=1
    ):
        phase = harmonic * omega * numeric_x
        if not isfinite(phase):
            raise ValueError(f"phase {harmonic} is not finite")
        term = a_n * cos(phase) + b_n * sin(phase)
        if fejer:
            term *= 1.0 - harmonic / (order + 1.0)
        if not isfinite(term):
            raise ValueError(f"term {harmonic} is not finite")
        terms.append(term)

    return FourierValue(
        value=_finite_sum(terms, "Fourier value"),
        order=order,
        period=numeric_period,
        method="fejer_mean" if fejer else "partial_sum",
    )


def fourier_partial_sum(
    x: Real,
    a0: Real,
    cosine_coefficients: Iterable[Real],
    sine_coefficients: Iterable[Real],
    period: Real,
) -> FourierValue:
    """Evaluate one finite real Fourier partial sum."""

    return _finite_fourier_value(
        x, a0, cosine_coefficients, sine_coefficients, period, fejer=False
    )


def fejer_mean(
    x: Real,
    a0: Real,
    cosine_coefficients: Iterable[Real],
    sine_coefficients: Iterable[Real],
    period: Real,
) -> FourierValue:
    """Evaluate the finite Fejér mean determined by the supplied coefficients."""

    return _finite_fourier_value(
        x, a0, cosine_coefficients, sine_coefficients, period, fejer=True
    )
