#!/usr/bin/env python3
"""
main.py
-------
Entry Point (CLI Sorting Animator & Profiler) untuk Modul 06 -
Basic Sorting Blueprints.

Contoh pemakaian:
    python main.py                                  # jalankan semua algoritma, data random N=15
    python main.py -a quick -n 30 -c reversed        # quick sort saja, data terbalik N=30
    python main.py -a insertion -n 25 -c nearly_sorted --animate
    python main.py -a bubble --descending
"""

import time

from config.sort_strategies import get_strategy, list_strategies, SORT_STRATEGIES
from src.data_prep.array_factory import generate_array
from src.data_prep.state_snapshot import StateSnapshot
from src.metrics.swap_counter import SwapCounter
from src.metrics.compare_counter import CompareCounter
from src.metrics.memory_tracker import MemoryTracker
from src.ui.bar_chart_renderer import play_animation
from src.ui.telemetry_presenter import present_single_result, present_comparison_table
from src.ui.cli_args import parse_args


def run_single_algorithm(name: str, base_array: list[int], animate: bool, descending: bool) -> dict:
    """Menjalankan satu algoritma sorting dan mengumpulkan telemetry-nya."""
    strategy = get_strategy(name)
    fn = strategy["function"]

    swap_counter = SwapCounter()
    compare_counter = CompareCounter()
    snapshot = StateSnapshot() if animate else None
    memory_tracker = MemoryTracker()

    start = time.perf_counter()
    with memory_tracker.track():
        result = fn(base_array, swap_counter, compare_counter, snapshot)
    elapsed_ms = (time.perf_counter() - start) * 1000

    if descending:
        result.reverse()

    if animate and snapshot:
        play_animation(snapshot)

    return {
        "label": strategy["label"],
        "result": result,
        "comparisons": compare_counter.count,
        "swaps": swap_counter.count,
        "elapsed_ms": elapsed_ms,
        "peak_kb": memory_tracker.peak_kb,
    }


def main() -> None:
    args = parse_args()

    print(f"Menghasilkan data uji: size={args.size}, case={args.case}")
    base_array = generate_array(args.size, args.case)
    print(f"Data awal: {base_array}\n")

    if args.algorithm == "all":
        results = []
        for name in list_strategies():
            r = run_single_algorithm(name, base_array, args.animate, args.descending)
            results.append(r)
        present_comparison_table(results)
        # Tampilkan hasil urut dari salah satu (semua harus identik)
        print(f"\nHasil terurut ({'descending' if args.descending else 'ascending'}):")
        print(results[0]["result"])
    else:
        r = run_single_algorithm(args.algorithm, base_array, args.animate, args.descending)
        present_single_result(r["label"], r["swaps"], r["comparisons"], r["elapsed_ms"], r["peak_kb"])
        print(f"\nHasil terurut: {r['result']}")


if __name__ == "__main__":
    main()
