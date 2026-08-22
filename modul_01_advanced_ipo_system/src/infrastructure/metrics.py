"""
metrics.py
Mengukur konsumsi memori serta waktu pemrosesan secara real-time
untuk keperluan audit performa sistem.
"""

import time
import tracemalloc
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Generator


@dataclass
class MetricSnapshot:
    """Hasil pengukuran satu blok eksekusi."""
    label: str
    duration_ms: float
    peak_memory_kb: float


@contextmanager
def measure(label: str = "operation") -> Generator[dict, None, None]:
    """
    Context manager untuk mengukur durasi eksekusi dan puncak penggunaan memori
    dari sebuah blok kode.

    Contoh:
        with measure("proses_dataset") as result:
            do_something()
        print(result["snapshot"])
    """
    tracemalloc.start()
    start_time = time.perf_counter()
    result_holder: dict = {}

    try:
        yield result_holder
    finally:
        duration_ms = (time.perf_counter() - start_time) * 1000
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        result_holder["snapshot"] = MetricSnapshot(
            label=label,
            duration_ms=duration_ms,
            peak_memory_kb=peak / 1024,
        )


class MetricsCollector:
    """Mengumpulkan beberapa MetricSnapshot sepanjang siklus hidup aplikasi."""

    def __init__(self):
        self._snapshots: list[MetricSnapshot] = []

    def record(self, snapshot: MetricSnapshot) -> None:
        self._snapshots.append(snapshot)

    def summary(self) -> dict:
        if not self._snapshots:
            return {"count": 0}
        total_duration = sum(s.duration_ms for s in self._snapshots)
        peak_memory = max(s.peak_memory_kb for s in self._snapshots)
        return {
            "count": len(self._snapshots),
            "total_duration_ms": total_duration,
            "peak_memory_kb": peak_memory,
        }
