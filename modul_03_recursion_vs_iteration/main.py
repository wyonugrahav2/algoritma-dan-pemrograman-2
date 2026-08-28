"""
main.py
--------
Entry Point (CLI Runner & Interactive Benchmark) untuk Modul 03:
Rekursi versus Iterasi.

Menjalankan benchmark perbandingan antara implementasi rekursif dan
iteratif untuk Fibonacci dan Tree Traversal, lalu menampilkan hasilnya
dalam bentuk tabel dan grafik ASCII di terminal.
"""

import sys

from config.settings import apply_recursion_limit, get_settings_summary
from config.constants import FIBONACCI_TEST_SIZES

from src.algorithms.recursive.fibonacci import fibonacci_recursive
from src.algorithms.iterative.fibonacci import fibonacci_recursive as fibonacci_iterative

from src.engine.runner import run_benchmark_suite
from src.formatters.table_presenter import print_comparison_table
from src.formatters.chart_generator import print_ascii_bar_chart


def print_banner():
    print("=" * 60)
    print(" MODUL 03: REKURSI VERSUS ITERASI")
    print(" Execution & Benchmarking Engine")
    print("=" * 60)


def print_settings():
    settings = get_settings_summary()
    print("\nKonfigurasi aktif:")
    for key, value in settings.items():
        print(f"  - {key}: {value}")
    print()


def run_fibonacci_benchmark():
    print("\n>> Menjalankan benchmark Fibonacci (Rekursif vs Iteratif)...\n")
    rows = run_benchmark_suite(
        test_sizes=FIBONACCI_TEST_SIZES,
        recursive_func=fibonacci_recursive,
        iterative_func=fibonacci_iterative,
    )
    print_comparison_table(rows)
    print()
    print_ascii_bar_chart(rows)


def main():
    apply_recursion_limit()
    print_banner()
    print_settings()

    try:
        run_fibonacci_benchmark()
    except KeyboardInterrupt:
        print("\nDibatalkan oleh pengguna.")
        sys.exit(1)

    print("\nBenchmark selesai.")


if __name__ == "__main__":
    main()
