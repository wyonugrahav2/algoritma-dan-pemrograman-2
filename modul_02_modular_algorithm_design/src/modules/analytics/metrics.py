"""
Kumpulan fungsi perhitungan metrik statistik dasar.

Dipisah dari analyzer.py agar logika perhitungan murni (pure function)
dapat diuji tanpa perlu menginstansiasi seluruh modul.
"""

from __future__ import annotations

from typing import List, Sequence


def mean(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def variance(values: Sequence[float]) -> float:
    if len(values) < 2:
        return 0.0
    m = mean(values)
    return sum((x - m) ** 2 for x in values) / (len(values) - 1)


def std_dev(values: Sequence[float]) -> float:
    return variance(values) ** 0.5


def median(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    ordered: List[float] = sorted(values)
    n = len(ordered)
    mid = n // 2
    if n % 2 == 0:
        return (ordered[mid - 1] + ordered[mid]) / 2
    return ordered[mid]


def min_max(values: Sequence[float]) -> tuple[float, float]:
    if not values:
        return (0.0, 0.0)
    return (min(values), max(values))


def summary(values: Sequence[float]) -> dict:
    """Ringkasan statistik lengkap untuk satu kumpulan angka."""
    lo, hi = min_max(values)
    return {
        "count": len(values),
        "mean": mean(values),
        "median": median(values),
        "variance": variance(values),
        "std_dev": std_dev(values),
        "min": lo,
        "max": hi,
    }
