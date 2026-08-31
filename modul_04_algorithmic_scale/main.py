#!/usr/bin/env python3
"""
main.py
Entry Point: Interactive Stress Test CLI.

Menjalankan alur lengkap stress testing engine:
  1. Pilih algoritma target dari library.
  2. Pilih tingkatan skala N yang ingin diuji.
  3. Bangkitkan data sintetis (best/average/worst case bila relevan).
  4. Jalankan profiler waktu & memori pada tiap level skala.
  5. Estimasi kelas Big-O otomatis.
  6. Tampilkan grafik ASCII & ekspor laporan.
"""

import sys

from config.scale_levels import SCALE_LEVELS, levels_up_to
from config.settings import Settings

from src.datasets.generators import generate_random_integers, generate_sorted_integers, generate_reversed_integers

from src.algorithms.constant_ops import get_first_element
from src.algorithms.logarithmic_ops import binary_search
from src.algorithms.linear_ops import linear_search, sum_all
from src.algorithms.linearithmic_ops import merge_sort
from src.algorithms.quadratic_ops import bubble_sort, has_duplicate_naive

from src.profiler.time_profiler import profile_execution_time
from src.profiler.memory_profiler import profile_memory_usage
from src.profiler.complexity_analyzer import classify_series

from src.visualizers.ascii_plotter import plot_growth_curve, plot_bar_comparison
from src.visualizers.report_exporter import export_to_json, export_to_markdown


# Registry algoritma target yang tersedia untuk diuji.
# Tiap entri: (nama tampilan, fungsi, pembuat argumen berdasarkan N, label kelas teoretis)
def _make_algorithm_registry():
    return {
        "1": (
            "get_first_element - O(1)",
            lambda data: get_first_element(data),
            lambda n: (generate_random_integers(n),),
        ),
        "2": (
            "binary_search - O(log N)",
            lambda data, target: binary_search(data, target),
            lambda n: (generate_sorted_integers(n), n // 2),
        ),
        "3": (
            "linear_search - O(N)",
            lambda data, target: linear_search(data, target),
            lambda n: (generate_random_integers(n), -1),  # -1 -> tidak ditemukan, worst case pencarian
        ),
        "4": (
            "sum_all - O(N)",
            lambda data: sum_all(data),
            lambda n: (generate_random_integers(n),),
        ),
        "5": (
            "merge_sort - O(N log N)",
            lambda data: merge_sort(data),
            lambda n: (generate_random_integers(n),),
        ),
        "6": (
            "bubble_sort - O(N^2)",
            lambda data: bubble_sort(data),
            lambda n: (generate_reversed_integers(n),),  # worst case untuk bubble sort
        ),
        "7": (
            "has_duplicate_naive - O(N^2)",
            lambda data: has_duplicate_naive(data),
            lambda n: (generate_random_integers(n),),
        ),
    }


def _print_header():
    print("=" * 60)
    print("  ALGORITHMIC SCALE - Stress Testing Engine")
    print("  Modul 04: Skalabilitas Algoritma & Analisis Big-O")
    print("=" * 60)


def _select_algorithm(registry):
    print("\nPilih algoritma target untuk diuji:")
    for key, (name, _, _) in registry.items():
        print(f"  [{key}] {name}")
    choice = input("Masukkan pilihan (nomor): ").strip()
    if choice not in registry:
        print("Pilihan tidak valid, menggunakan default: linear_search")
        choice = "3"
    return registry[choice]


def _select_max_scale():
    print("\nPilih skala maksimum untuk diuji:")
    for i, level in enumerate(SCALE_LEVELS, start=1):
        print(f"  [{i}] {level}")
    choice = input("Masukkan pilihan (nomor, default=Medium): ").strip()
    try:
        idx = int(choice) - 1
        level_name = SCALE_LEVELS[idx].name
    except (ValueError, IndexError):
        level_name = "Medium"
    return levels_up_to(level_name)


def run_stress_test(algo_name, func, arg_builder, levels):
    """Menjalankan seluruh pipeline stress test untuk satu algoritma di semua level yang dipilih."""
    print(f"\nMenjalankan stress test untuk: {algo_name}")
    print(f"Timeout: {Settings.EXECUTION_TIMEOUT_SECONDS}s | Batas RAM: {Settings.MAX_MEMORY_MB}MB\n")

    measurements = []
    time_points = []
    bottlenecks = []

    for level in levels:
        args = arg_builder(level.n)
        print(f"  -> {level} ...", end=" ", flush=True)

        time_result = profile_execution_time(func, n=level.n, args=args)
        mem_result = profile_memory_usage(func, n=level.n, args=args)

        status_flags = []
        if time_result.timed_out:
            status_flags.append("TIMEOUT")
        if mem_result.exceeded_limit:
            status_flags.append("MEMORY EXCEEDED")

        status = ", ".join(status_flags) if status_flags else "OK"
        print(f"waktu={time_result.mean_seconds:.6f}s peak_mem={mem_result.peak_mb:.3f}MB [{status}]")

        measurements.append({
            "level": level.name,
            "n": level.n,
            "mean_seconds": time_result.mean_seconds,
            "peak_mb": mem_result.peak_mb,
            "timed_out": time_result.timed_out,
            "exceeded_memory": mem_result.exceeded_limit,
        })

        if not time_result.timed_out:
            time_points.append((level.n, time_result.mean_seconds))

        if time_result.timed_out:
            bottlenecks.append(f"Timeout terdeteksi pada level {level.name} (N={level.n:,})")
            break
        if mem_result.exceeded_limit:
            bottlenecks.append(f"Batas memori terlampaui pada level {level.name} (N={level.n:,})")
            break

    estimate = classify_series(time_points)

    print("\n" + plot_growth_curve(time_points, title=f"Growth Curve: {algo_name}"))
    print(f"\nEstimasi kompleksitas: {estimate.predicted_class.value} (confidence={estimate.confidence})")
    print(f"Detail: {estimate.detail}")

    report = {
        "algorithm_name": algo_name,
        "estimated_complexity": estimate.predicted_class.value,
        "confidence": estimate.confidence,
        "measurements": measurements,
        "bottlenecks": bottlenecks,
    }

    return report


def main():
    _print_header()
    registry = _make_algorithm_registry()

    try:
        algo_name, func, arg_builder = _select_algorithm(registry)
        levels = _select_max_scale()
    except (EOFError, KeyboardInterrupt):
        print("\nDibatalkan oleh pengguna.")
        sys.exit(0)

    report = run_stress_test(algo_name, func, arg_builder, levels)

    export_choice = input("\nEkspor laporan? [m]arkdown / [j]son / [t]idak (default=t): ").strip().lower()
    if export_choice == "m":
        path = export_to_markdown(report)
        print(f"Laporan Markdown disimpan di: {path}")
    elif export_choice == "j":
        path = export_to_json(report)
        print(f"Laporan JSON disimpan di: {path}")
    else:
        print("Laporan tidak diekspor.")

    print("\nSelesai. Terima kasih telah menggunakan Algorithmic Scale Stress Testing Engine.")


if __name__ == "__main__":
    main()
