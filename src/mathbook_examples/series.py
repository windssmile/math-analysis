"""Certified truncation helpers for the Chapter 23 examples."""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class SeriesCertificate:
    """A finite approximation together with a proved analytic tail bound."""

    approximation: float
    error_bound: float
    terms_used: int
    status: str
    assumptions: tuple[str, ...]


def _positive_finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be positive and finite")
    return value


def _positive_integer(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def geometric_series_certificate(
    first_term: float,
    ratio: float,
    tolerance: float,
    max_terms: int,
) -> SeriesCertificate:
    """Approximate a convergent geometric series with its exact tail bound."""

    first_term = float(first_term)
    ratio = float(ratio)
    tolerance = _positive_finite(tolerance, "tolerance")
    max_terms = _positive_integer(max_terms, "max_terms")
    if not math.isfinite(first_term):
        raise ValueError("first_term must be finite")
    if not math.isfinite(ratio) or abs(ratio) >= 1.0:
        raise ValueError("ratio must be finite with absolute value below 1")

    partial = 0.0
    term = first_term
    error_bound = abs(first_term) / (1.0 - abs(ratio))
    terms_used = 0
    while terms_used < max_terms:
        partial += term
        terms_used += 1
        term *= ratio
        error_bound = abs(term) / (1.0 - abs(ratio))
        if error_bound <= tolerance:
            return SeriesCertificate(
                partial,
                error_bound,
                terms_used,
                "certified",
                ("|r| < 1", "geometric tail formula"),
            )
    return SeriesCertificate(
        partial,
        error_bound,
        terms_used,
        "budget_unmet",
        ("|r| < 1", "geometric tail formula"),
    )


def p_series_integral_certificate(
    exponent: float,
    tolerance: float,
    max_terms: int,
) -> SeriesCertificate:
    """Approximate sum(n**-p) using the integral-test upper tail bound."""

    exponent = float(exponent)
    tolerance = _positive_finite(tolerance, "tolerance")
    max_terms = _positive_integer(max_terms, "max_terms")
    if not math.isfinite(exponent) or exponent <= 1.0:
        raise ValueError("exponent must be finite and greater than 1")

    raw_required = ((exponent - 1.0) * tolerance) ** (
        -1.0 / (exponent - 1.0)
    )
    if not math.isfinite(raw_required):
        required = max_terms + 1
    else:
        required = max(1, math.ceil(raw_required))
        while (
            required ** (1.0 - exponent) / (exponent - 1.0)
            > tolerance
        ):
            required += 1

    terms_used = min(required, max_terms)
    approximation = math.fsum(
        1.0 / (n**exponent) for n in range(1, terms_used + 1)
    )
    error_bound = terms_used ** (1.0 - exponent) / (exponent - 1.0)
    status = "certified" if error_bound <= tolerance else "budget_unmet"
    return SeriesCertificate(
        approximation,
        error_bound,
        terms_used,
        status,
        (
            "p > 1",
            "x^-p is positive and decreasing on [1, infinity)",
            "integral-test tail upper bound",
        ),
    )
