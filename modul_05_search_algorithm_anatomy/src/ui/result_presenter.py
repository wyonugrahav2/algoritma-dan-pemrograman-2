"""
result_presenter.py
Menampilkan hasil pencarian dalam format tabel di terminal, lengkap
dengan sorotan (highlight) posisi data yang ditemukan.
"""

from typing import List, Sequence

from src.algorithms.linear_search import SearchResult
from src.analytics.search_profiler import ProfileReport, format_profile_report
from src.analytics.step_counter import ComparisonReport


HIGHLIGHT_START = "\033[92m\033[1m"  # hijau tebal
HIGHLIGHT_END = "\033[0m"


def present_result(result: SearchResult, data: Sequence) -> str:
    """
    Membangun representasi teks dari hasil pencarian tunggal, termasuk
    potongan data di sekitar posisi target (jika ditemukan) dengan
    highlight pada elemen yang cocok.
    """
    lines = []
    header = f"=== Hasil Pencarian [{result.algorithm.upper()}] ==="
    lines.append(header)

    if result.found:
        lines.append(f"Status         : DITEMUKAN pada index {result.index}")
        lines.append(f"Perbandingan   : {result.comparisons}")
        lines.append(_render_context_window(data, result.index))
    else:
        lines.append("Status         : TIDAK DITEMUKAN")
        lines.append(f"Perbandingan   : {result.comparisons}")

    return "\n".join(lines)


def _render_context_window(data: Sequence, index: int, window: int = 2) -> str:
    """Menampilkan beberapa elemen di sekitar `index` dengan highlight."""
    start = max(0, index - window)
    end = min(len(data), index + window + 1)

    parts = []
    for i in range(start, end):
        if i == index:
            parts.append(f"{HIGHLIGHT_START}[{data[i]}]{HIGHLIGHT_END}")
        else:
            parts.append(str(data[i]))

    return "Konteks Data   : " + " ".join(parts)


def present_comparison_table(reports: List[ComparisonReport]) -> str:
    """
    Menampilkan tabel perbandingan efisiensi antar algoritma
    (dipakai pada mode --benchmark di main.py).
    """
    header = (
        f"{'Algoritma':<15}{'N':>8}{'Aktual':>10}{'Teori (worst)':>16}"
        f"{'Rasio':>10}{'Status':>15}"
    )
    separator = "-" * len(header)
    rows = [header, separator]

    for r in reports:
        status = "DITEMUKAN" if r.found else "TIDAK ADA"
        rows.append(
            f"{r.algorithm:<15}{r.n:>8}{r.actual_comparisons:>10}"
            f"{r.theoretical_worst_case:>16.2f}{r.efficiency_ratio:>10.2f}{status:>15}"
        )

    return "\n".join(rows)


def present_profile_reports(reports: List[ProfileReport]) -> str:
    """Menampilkan hasil profiling latensi & memori untuk beberapa algoritma."""
    lines = ["=== Profil Performa (Latensi & Memori) ==="]
    for report in sorted(reports, key=lambda r: r.elapsed_ms):
        lines.append(format_profile_report(report))
    return "\n".join(lines)
