"""
runner.py
----------
Eksekutor otomatis yang menjalankan versi rekursif dan iteratif secara
berdampingan (side-by-side) menggunakan sampel masukan yang sama, lalu
mengumpulkan hasil benchmarking untuk dianalisis dan divisualisasikan.
"""

from dataclasses import dataclass
from typing import Any, Callable, List

from config.settings import BENCHMARK_REPEAT_COUNT, apply_recursion_limit
from src.engine.timer import measure_execution_time
from src.engine.profiler import profile_execution
from src.utils.stack_overflow_guard import guarded_call


@dataclass
class BenchmarkRow:
    """Satu baris hasil perbandingan rekursif vs iteratif untuk input N."""
    n: int
    recursive_time_us: float
    iterative_time_us: float
    recursive_stack_depth: int
    iterative_memory_bytes: int
    result_match: bool
    recursive_error: str = ""
    iterative_error: str = ""


def run_single_comparison(n: int, recursive_func: Callable,
                           iterative_func: Callable) -> BenchmarkRow:
    """
    Menjalankan satu perbandingan antara fungsi rekursif dan iteratif
    untuk nilai input N yang sama.

    Args:
        n: nilai input yang diuji.
        recursive_func: fungsi versi rekursif.
        iterative_func: fungsi versi iteratif (signature isomorfis).

    Returns:
        BenchmarkRow berisi hasil perbandingan lengkap.
    """
    apply_recursion_limit()

    recursive_result, recursive_error = guarded_call(recursive_func, n)
    recursive_time_us = 0.0
    recursive_depth = 0
    if recursive_error is None:
        _, recursive_time_us = measure_execution_time(recursive_func, n)
        profile = profile_execution(recursive_func, n)
        recursive_depth = profile.stack_depth_estimate

    iterative_result, iterative_error = guarded_call(iterative_func, n)
    iterative_time_us = 0.0
    iterative_memory = 0
    if iterative_error is None:
        _, iterative_time_us = measure_execution_time(iterative_func, n)
        profile = profile_execution(iterative_func, n)
        iterative_memory = profile.peak_memory_bytes

    match = (
        recursive_error is None
        and iterative_error is None
        and recursive_result == iterative_result
    )

    return BenchmarkRow(
        n=n,
        recursive_time_us=recursive_time_us,
        iterative_time_us=iterative_time_us,
        recursive_stack_depth=recursive_depth,
        iterative_memory_bytes=iterative_memory,
        result_match=match,
        recursive_error=recursive_error or "",
        iterative_error=iterative_error or "",
    )


def run_benchmark_suite(test_sizes: List[int], recursive_func: Callable,
                         iterative_func: Callable,
                         repeat: int = BENCHMARK_REPEAT_COUNT) -> List[BenchmarkRow]:
    """
    Menjalankan serangkaian benchmark untuk beberapa ukuran input,
    masing-masing diulang beberapa kali untuk stabilitas hasil.

    Args:
        test_sizes: daftar nilai N yang akan diuji.
        recursive_func: fungsi versi rekursif.
        iterative_func: fungsi versi iteratif.
        repeat: jumlah pengulangan per ukuran input.

    Returns:
        List BenchmarkRow, satu per ukuran input (hasil rata-rata waktu).
    """
    rows: List[BenchmarkRow] = []

    for n in test_sizes:
        aggregated: List[BenchmarkRow] = []
        for _ in range(repeat):
            aggregated.append(run_single_comparison(n, recursive_func, iterative_func))

        avg_recursive_time = sum(r.recursive_time_us for r in aggregated) / repeat
        avg_iterative_time = sum(r.iterative_time_us for r in aggregated) / repeat

        rows.append(BenchmarkRow(
            n=n,
            recursive_time_us=avg_recursive_time,
            iterative_time_us=avg_iterative_time,
            recursive_stack_depth=aggregated[-1].recursive_stack_depth,
            iterative_memory_bytes=aggregated[-1].iterative_memory_bytes,
            result_match=all(r.result_match for r in aggregated),
            recursive_error=aggregated[-1].recursive_error,
            iterative_error=aggregated[-1].iterative_error,
        ))

    return rows
