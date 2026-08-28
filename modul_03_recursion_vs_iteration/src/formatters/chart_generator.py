"""
chart_generator.py
---------------------
Menghasilkan grafik perbandingan performa berbasis karakter ASCII
di dalam jendela terminal.
"""

from typing import List
from config.constants import ASCII_BAR_CHAR, ASCII_CHART_MAX_WIDTH
from src.engine.runner import BenchmarkRow


def generate_ascii_bar_chart(rows: List[BenchmarkRow]) -> str:
    """
    Membuat grafik batang ASCII yang membandingkan waktu eksekusi
    rekursif vs iteratif untuk setiap ukuran input N.

    Args:
        rows: daftar BenchmarkRow hasil benchmark.

    Returns:
        String grafik ASCII siap cetak.
    """
    if not rows:
        return "(tidak ada data untuk divisualisasikan)"

    max_time = max(
        max(row.recursive_time_us, row.iterative_time_us) for row in rows
    )
    max_time = max(max_time, 1e-9)  # hindari pembagian dengan nol

    lines = ["Perbandingan Waktu Eksekusi (Rekursif vs Iteratif)", ""]

    for row in rows:
        rec_bar_len = int((row.recursive_time_us / max_time) * ASCII_CHART_MAX_WIDTH)
        iter_bar_len = int((row.iterative_time_us / max_time) * ASCII_CHART_MAX_WIDTH)

        rec_bar = ASCII_BAR_CHAR * max(rec_bar_len, 1)
        iter_bar = ASCII_BAR_CHAR * max(iter_bar_len, 1)

        lines.append(f"N={row.n:<4} Recursive | {rec_bar} {row.recursive_time_us:.2f} µs")
        lines.append(f"N={row.n:<4} Iterative | {iter_bar} {row.iterative_time_us:.2f} µs")
        lines.append("")

    return "\n".join(lines)


def print_ascii_bar_chart(rows: List[BenchmarkRow]) -> None:
    """Mencetak langsung grafik ASCII ke stdout."""
    print(generate_ascii_bar_chart(rows))
