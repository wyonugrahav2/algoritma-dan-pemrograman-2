"""
lookup_benchmarker.py
Uji banding waktu akses O(1) Dict/Set vs O(N) List untuk berbagai ukuran
data, membuktikan secara empiris keunggulan hash-based lookup pada skala
besar.
"""

from __future__ import annotations
import time
from dataclasses import dataclass
from typing import List


@dataclass
class BenchmarkResult:
    n: int
    list_lookup_seconds: float
    dict_lookup_seconds: float
    speedup: float


def _time_lookup(container, key, repeat: int) -> float:
    start = time.perf_counter()
    for _ in range(repeat):
        _ = key in container
    return time.perf_counter() - start


def benchmark_lookup(n: int, repeat: int = 1000) -> BenchmarkResult:
    """
    Bandingkan waktu `key in list` (O(N)) vs `key in dict` (O(1) amortized)
    saat mencari elemen yang berada di posisi TERAKHIR (worst case untuk list).
    """
    data_list: List[int] = list(range(n))
    data_dict = {i: True for i in range(n)}
    target = n - 1  # worst case list lookup

    list_time = _time_lookup(data_list, target, repeat)
    dict_time = _time_lookup(data_dict, target, repeat)

    speedup = (list_time / dict_time) if dict_time > 0 else float("inf")
    return BenchmarkResult(n=n, list_lookup_seconds=list_time,
                            dict_lookup_seconds=dict_time, speedup=speedup)


def run_suite(sizes: List[int], repeat: int = 1000) -> List[BenchmarkResult]:
    return [benchmark_lookup(n, repeat) for n in sizes]


def print_suite(results: List[BenchmarkResult]) -> None:
    header = f"{'N':>10} | {'List (s)':>12} | {'Dict (s)':>12} | {'Speedup':>10}"
    print(header)
    print("-" * len(header))
    for r in results:
        print(f"{r.n:>10} | {r.list_lookup_seconds:>12.6f} | "
              f"{r.dict_lookup_seconds:>12.6f} | {r.speedup:>9.1f}x")


if __name__ == "__main__":
    sizes = [100, 1_000, 10_000, 100_000]
    results = run_suite(sizes, repeat=500)
    print_suite(results)
