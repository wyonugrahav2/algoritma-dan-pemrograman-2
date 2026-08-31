"""
complexity_analyzer.py
Estimator otomatis kelas Big-O dari hasil profiling waktu eksekusi,
dengan membandingkan rasio pertumbuhan waktu terhadap pertumbuhan N
di antara titik-titik skala yang berurutan.
"""

import math
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


class ComplexityClass(str, Enum):
    CONSTANT = "O(1)"
    LOGARITHMIC = "O(log N)"
    LINEAR = "O(N)"
    LINEARITHMIC = "O(N log N)"
    QUADRATIC = "O(N^2)"
    UNKNOWN = "Unknown"


@dataclass
class ComplexityEstimate:
    """Hasil akhir estimasi kompleksitas untuk satu rangkaian pengujian."""
    predicted_class: ComplexityClass
    confidence: float  # 0.0 - 1.0, makin dekat ke 1 makin yakin
    ratios_observed: List[float]
    detail: str = ""


def _expected_ratio(complexity: ComplexityClass, n1: int, n2: int) -> float:
    """Menghitung rasio waktu teoretis yang diharapkan untuk kelas kompleksitas tertentu."""
    if n1 <= 0:
        n1 = 1
    if complexity == ComplexityClass.CONSTANT:
        return 1.0
    if complexity == ComplexityClass.LOGARITHMIC:
        return math.log(max(n2, 2)) / math.log(max(n1, 2))
    if complexity == ComplexityClass.LINEAR:
        return n2 / n1
    if complexity == ComplexityClass.LINEARITHMIC:
        return (n2 * math.log(max(n2, 2))) / (n1 * math.log(max(n1, 2)))
    if complexity == ComplexityClass.QUADRATIC:
        return (n2 / n1) ** 2
    raise ValueError(f"Kompleksitas tidak dikenal: {complexity}")


def estimate_growth_ratio(n1: int, t1: float, n2: int, t2: float) -> float:
    """Menghitung rasio pertumbuhan waktu aktual antara dua titik pengukuran (t2/t1)."""
    if t1 <= 0:
        t1 = 1e-9  # hindari pembagian dengan nol untuk N kecil yang eksekusinya < resolusi timer
    return t2 / t1


def classify_pair(n1: int, t1: float, n2: int, t2: float) -> ComplexityEstimate:
    """
    Membandingkan rasio pertumbuhan aktual terhadap rasio teoretis
    tiap kelas kompleksitas, lalu memilih kelas dengan error terkecil.
    """
    actual_ratio = estimate_growth_ratio(n1, t1, n2, t2)

    candidates = [
        ComplexityClass.CONSTANT,
        ComplexityClass.LOGARITHMIC,
        ComplexityClass.LINEAR,
        ComplexityClass.LINEARITHMIC,
        ComplexityClass.QUADRATIC,
    ]

    errors = {}
    for candidate in candidates:
        expected = _expected_ratio(candidate, n1, n2)
        # Error relatif dalam skala logaritmik agar adil di semua rentang.
        errors[candidate] = abs(math.log(max(actual_ratio, 1e-9)) - math.log(max(expected, 1e-9)))

    best_class = min(errors, key=errors.get)
    best_error = errors[best_class]

    # Confidence: makin kecil error, makin tinggi confidence (dinormalisasi kasar).
    confidence = max(0.0, 1.0 - min(best_error / 2.0, 1.0))

    detail = (
        f"N: {n1} -> {n2}, rasio waktu aktual = {actual_ratio:.3f}, "
        f"rasio teoretis {best_class.value} = {_expected_ratio(best_class, n1, n2):.3f}"
    )

    return ComplexityEstimate(
        predicted_class=best_class,
        confidence=confidence,
        ratios_observed=[actual_ratio],
        detail=detail,
    )


def classify_series(measurements: List[Tuple[int, float]]) -> ComplexityEstimate:
    """
    Menerima daftar (n, mean_waktu) berurutan dari skala kecil ke besar,
    lalu mengagregasi estimasi Big-O dari tiap pasangan titik berurutan
    menjadi satu estimasi akhir (voting berbobot confidence).
    """
    valid_points = [(n, t) for n, t in measurements if t > 0 and n > 0]
    if len(valid_points) < 2:
        return ComplexityEstimate(
            predicted_class=ComplexityClass.UNKNOWN,
            confidence=0.0,
            ratios_observed=[],
            detail="Data pengukuran tidak cukup untuk estimasi (minimal 2 titik valid).",
        )

    votes = {}
    ratios = []
    for i in range(len(valid_points) - 1):
        n1, t1 = valid_points[i]
        n2, t2 = valid_points[i + 1]
        pair_estimate = classify_pair(n1, t1, n2, t2)
        ratios.extend(pair_estimate.ratios_observed)
        votes[pair_estimate.predicted_class] = votes.get(pair_estimate.predicted_class, 0.0) + pair_estimate.confidence

    best_class = max(votes, key=votes.get)
    total_confidence = votes[best_class] / max(len(valid_points) - 1, 1)

    return ComplexityEstimate(
        predicted_class=best_class,
        confidence=round(total_confidence, 3),
        ratios_observed=ratios,
        detail=f"Estimasi diagregasi dari {len(valid_points) - 1} pasang titik pengukuran berurutan.",
    )
