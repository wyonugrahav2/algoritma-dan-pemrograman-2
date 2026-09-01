"""
step_counter.py
Menghitung secara presisi berapa kali operasi perbandingan (comparison)
dilakukan sebelum data ditemukan atau dinyatakan hilang, dan menyediakan
analisis ringkas atas hasil pencarian (SearchResult).
"""

from dataclasses import dataclass
from math import log2
from typing import List

from src.algorithms.linear_search import SearchResult


@dataclass
class ComparisonReport:
    """Ringkasan efisiensi satu eksekusi pencarian, dibandingkan teori."""

    algorithm: str
    n: int
    actual_comparisons: int
    theoretical_worst_case: float
    efficiency_ratio: float  # actual / theoretical (semakin kecil semakin baik)
    found: bool


_THEORETICAL_WORST_CASE = {
    "linear": lambda n: float(n) if n > 0 else 1.0,
    "binary": lambda n: (log2(n) + 1) if n > 0 else 1.0,
    "interpolation": lambda n: (log2(log2(n)) + 1) if n > 3 else 2.0,
    "exponential": lambda n: (2 * log2(n) + 1) if n > 0 else 1.0,
    "hash": lambda n: 1.0,
}


def count_comparisons(result: SearchResult) -> int:
    """Mengembalikan jumlah perbandingan aktual dari sebuah SearchResult."""
    return result.comparisons


def build_comparison_report(result: SearchResult, n: int) -> ComparisonReport:
    """
    Membangun laporan yang membandingkan jumlah perbandingan aktual
    terhadap perkiraan kompleksitas teoritis kasus terburuk algoritma
    yang bersangkutan (lihat docs/search_space_reduction.md).
    """
    worst_case_fn = _THEORETICAL_WORST_CASE.get(result.algorithm, lambda n: float(n))
    theoretical = max(worst_case_fn(n), 1.0)
    ratio = result.comparisons / theoretical if theoretical else 0.0

    return ComparisonReport(
        algorithm=result.algorithm,
        n=n,
        actual_comparisons=result.comparisons,
        theoretical_worst_case=round(theoretical, 2),
        efficiency_ratio=round(ratio, 2),
        found=result.found,
    )


def compare_algorithms(results: List[SearchResult], n: int) -> List[ComparisonReport]:
    """
    Membangun laporan perbandingan untuk beberapa hasil algoritma
    sekaligus (misalnya saat CLI dijalankan dengan mode --benchmark).
    Diurutkan dari yang paling sedikit perbandingan.
    """
    reports = [build_comparison_report(r, n) for r in results]
    return sorted(reports, key=lambda r: r.actual_comparisons)
