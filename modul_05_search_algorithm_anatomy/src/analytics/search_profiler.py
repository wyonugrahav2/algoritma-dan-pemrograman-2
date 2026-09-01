"""
search_profiler.py
Mengukur latensi eksekusi dan estimasi konsumsi memori saat proses
pencarian berlangsung, untuk melengkapi metrik "jumlah perbandingan"
dari step_counter.py dengan data performa dunia nyata.
"""

import sys
import time
import tracemalloc
from dataclasses import dataclass
from typing import Any, Callable, Sequence

from src.algorithms.linear_search import SearchResult


@dataclass
class ProfileReport:
    """Hasil pengukuran performa satu eksekusi algoritma pencarian."""

    algorithm: str
    elapsed_ms: float
    peak_memory_bytes: int
    comparisons: int
    found: bool


def profile_search(
    search_fn: Callable[[Sequence[Any], Any], SearchResult],
    data: Sequence[Any],
    target: Any,
) -> ProfileReport:
    """
    Menjalankan `search_fn(data, target)` sambil mengukur:
      - latensi eksekusi (dalam milidetik, memakai time.perf_counter)
      - puncak konsumsi memori tambahan selama eksekusi (via tracemalloc)

    Mengembalikan ProfileReport yang dapat ditampilkan oleh
    src/ui/result_presenter.py.
    """
    tracemalloc.start()
    start_time = time.perf_counter()

    result: SearchResult = search_fn(data, target)

    elapsed_seconds = time.perf_counter() - start_time
    _current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return ProfileReport(
        algorithm=result.algorithm,
        elapsed_ms=round(elapsed_seconds * 1000, 4),
        peak_memory_bytes=peak,
        comparisons=result.comparisons,
        found=result.found,
    )


def estimate_data_footprint(data: Sequence[Any]) -> int:
    """
    Mengestimasi ukuran memori (bytes) yang ditempati oleh struktur data
    input, berguna untuk membandingkan overhead memori antar strategi
    (misalnya Hash Lookup membutuhkan indeks tambahan, sedangkan Binary
    Search tidak membutuhkan struktur tambahan selain data terurut).
    """
    return sys.getsizeof(data) + sum(sys.getsizeof(item) for item in data)


def format_profile_report(report: ProfileReport) -> str:
    """Memformat ProfileReport menjadi satu baris teks ringkas untuk CLI."""
    status = "DITEMUKAN" if report.found else "TIDAK DITEMUKAN"
    return (
        f"[{report.algorithm.upper():^13}] {status:15} | "
        f"{report.comparisons:>5} perbandingan | "
        f"{report.elapsed_ms:>8.4f} ms | "
        f"peak mem: {report.peak_memory_bytes:>8} bytes"
    )
