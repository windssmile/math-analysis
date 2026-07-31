"""Finite illustrations for Part XI; no function here certifies outer measure."""

from dataclasses import dataclass
from math import fsum, isfinite
from numbers import Real
from typing import Iterable, Sequence


@dataclass(frozen=True)
class FiniteCoverResult:
    """Length of one finite interval union, not an outer-measure infimum."""

    upper_bound: float
    merged_intervals: tuple[tuple[float, float], ...]
    input_count: int
    merged_count: int
    status: str = "finite_cover_only"


def _finite_real(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number, not bool")
    converted = float(value)
    if not isfinite(converted):
        raise ValueError(f"{name} must be finite")
    return converted


def simple_integral(values: Sequence[Real], measures: Sequence[Real]) -> float:
    """Integrate declared disjoint measurable pieces with finite measures.

    Measurability and disjointness are caller-provided mathematical premises;
    this finite arithmetic helper cannot verify them.
    """

    if isinstance(values, (str, bytes)) or isinstance(measures, (str, bytes)):
        raise TypeError("values and measures must be finite sequences")
    try:
        raw_values = list(values)
        raw_measures = list(measures)
    except TypeError as exc:
        raise TypeError("values and measures must be finite sequences") from exc
    if not raw_values:
        raise ValueError("values and measures must be nonempty")
    if len(raw_values) != len(raw_measures):
        raise ValueError("values and measures must have equal length")

    terms = []
    for index, (value, measure) in enumerate(zip(raw_values, raw_measures, strict=True)):
        numeric_value = _finite_real(value, f"values[{index}]")
        numeric_measure = _finite_real(measure, f"measures[{index}]")
        if numeric_measure < 0:
            raise ValueError(f"measures[{index}] must be nonnegative")
        term = numeric_value * numeric_measure
        if not isfinite(term):
            raise ValueError(f"term {index} is not finite")
        terms.append(term)
    try:
        total = fsum(terms)
    except OverflowError as exc:
        raise ValueError("simple integral sum is not finite") from exc
    if not isfinite(total):
        raise ValueError("simple integral sum is not finite")
    return total


def finite_cover_upper_bound(intervals: Iterable[Sequence[Real]]) -> FiniteCoverResult:
    """Return the union length of a finite interval family as an upper bound only."""

    if isinstance(intervals, (str, bytes)):
        raise TypeError("intervals must be a finite iterable of endpoint pairs")
    try:
        raw_intervals = list(intervals)
    except TypeError as exc:
        raise TypeError("intervals must be a finite iterable of endpoint pairs") from exc
    if not raw_intervals:
        raise ValueError("intervals must be nonempty")

    normalized = []
    for index, interval in enumerate(raw_intervals):
        if isinstance(interval, (str, bytes)):
            raise TypeError(f"intervals[{index}] must be an endpoint pair")
        try:
            endpoints = list(interval)
        except TypeError as exc:
            raise TypeError(f"intervals[{index}] must be an endpoint pair") from exc
        if len(endpoints) != 2:
            raise ValueError(f"intervals[{index}] must contain two endpoints")
        left = _finite_real(endpoints[0], f"intervals[{index}][0]")
        right = _finite_real(endpoints[1], f"intervals[{index}][1]")
        if right < left:
            raise ValueError(f"intervals[{index}] has right endpoint below left endpoint")
        normalized.append((left, right))

    normalized.sort()
    merged: list[list[float]] = []
    for left, right in normalized:
        if not merged or left > merged[-1][1]:
            merged.append([left, right])
        else:
            merged[-1][1] = max(merged[-1][1], right)

    lengths = []
    for left, right in merged:
        length = right - left
        if not isfinite(length):
            raise ValueError("merged interval length is not finite")
        lengths.append(length)
    try:
        upper_bound = fsum(lengths)
    except OverflowError as exc:
        raise ValueError("finite cover upper bound is not finite") from exc
    if not isfinite(upper_bound):
        raise ValueError("finite cover upper bound is not finite")

    frozen_intervals = tuple((left, right) for left, right in merged)
    return FiniteCoverResult(
        upper_bound=upper_bound,
        merged_intervals=frozen_intervals,
        input_count=len(normalized),
        merged_count=len(frozen_intervals),
    )
