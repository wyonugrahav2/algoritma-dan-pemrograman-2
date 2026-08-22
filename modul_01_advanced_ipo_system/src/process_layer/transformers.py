"""
transformers.py
Melakukan pemetaan dan pengubahan bentuk data sesuai kebutuhan logika sistem.
Fungsi-fungsi di sini bersifat murni (pure function) agar mudah diuji.
"""

import statistics
from typing import List


def normalize_values(values: List[float]) -> List[float]:
    """Menormalisasi daftar nilai ke rentang [0, 1] menggunakan min-max scaling."""
    if not values:
        return []
    minimum, maximum = min(values), max(values)
    if minimum == maximum:
        return [0.0 for _ in values]
    return [(v - minimum) / (maximum - minimum) for v in values]


def compute_statistics(values: List[float]) -> dict:
    """Menghitung statistik deskriptif dasar dari daftar nilai numerik."""
    if not values:
        return {"count": 0, "mean": 0.0, "median": 0.0, "stdev": 0.0, "min": 0.0, "max": 0.0}

    return {
        "count": len(values),
        "mean": statistics.fmean(values),
        "median": statistics.median(values),
        "stdev": statistics.stdev(values) if len(values) > 1 else 0.0,
        "min": min(values),
        "max": max(values),
    }


def sort_values(values: List[float], descending: bool = False) -> List[float]:
    """Mengurutkan daftar nilai numerik."""
    return sorted(values, reverse=descending)


def filter_outliers(values: List[float], threshold_stdev: float = 2.0) -> List[float]:
    """Menyaring nilai yang menyimpang lebih dari `threshold_stdev` standar deviasi."""
    if len(values) < 2:
        return list(values)
    mean = statistics.fmean(values)
    stdev = statistics.stdev(values)
    if stdev == 0:
        return list(values)
    return [v for v in values if abs(v - mean) <= threshold_stdev * stdev]


def scale_values(values: List[float], factor: float) -> List[float]:
    """Mengalikan setiap nilai dalam daftar dengan faktor skala tertentu."""
    return [v * factor for v in values]
