"""
table_presenter.py
---------------------
Merender tabel perbandingan statistik eksekusi secara rapi di layar
terminal CLI.
"""

from typing import List
from src.engine.runner import BenchmarkRow
from src.engine.profiler import format_bytes


def render_comparison_table(rows: List[BenchmarkRow]) -> str:
    """
    Membangun representasi string tabel perbandingan hasil benchmark.

    Args:
        rows: daftar BenchmarkRow hasil dari run_benchmark_suite().

    Returns:
        String tabel yang siap dicetak ke terminal.
    """
    headers = [
        "N",
        "Recursive (µs)",
        "Iterative (µs)",
        "Stack Depth",
        "Iter. Memory",
        "Match",
    ]

    col_widths = [max(len(h), 12) for h in headers]

    lines = []
    header_line = " | ".join(h.ljust(w) for h, w in zip(headers, col_widths))
    lines.append(header_line)
    lines.append("-" * len(header_line))

    for row in rows:
        values = [
            str(row.n),
            f"{row.recursive_time_us:.2f}",
            f"{row.iterative_time_us:.2f}",
            str(row.recursive_stack_depth),
            format_bytes(row.iterative_memory_bytes),
            "OK" if row.result_match else "MISMATCH",
        ]
        line = " | ".join(v.ljust(w) for v, w in zip(values, col_widths))
        lines.append(line)

        if row.recursive_error:
            lines.append(f"  ! Recursive error (N={row.n}): {row.recursive_error}")
        if row.iterative_error:
            lines.append(f"  ! Iterative error (N={row.n}): {row.iterative_error}")

    return "\n".join(lines)


def print_comparison_table(rows: List[BenchmarkRow]) -> None:
    """Mencetak langsung tabel perbandingan ke stdout."""
    print(render_comparison_table(rows))
