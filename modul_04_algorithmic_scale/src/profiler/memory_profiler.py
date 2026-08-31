"""
memory_profiler.py
Mengukur puncak konsumsi memori (Peak Memory Usage) selama eksekusi
sebuah fungsi target, menggunakan modul bawaan `tracemalloc`.
"""

import tracemalloc
from dataclasses import dataclass
from typing import Any, Callable, Optional

from config.settings import Settings


@dataclass
class MemoryProfileResult:
    """Hasil pengukuran memori untuk satu fungsi pada satu N."""
    n: int
    current_bytes: int = 0
    peak_bytes: int = 0
    exceeded_limit: bool = False

    @property
    def peak_mb(self) -> float:
        return self.peak_bytes / (1024 * 1024)

    @property
    def current_mb(self) -> float:
        return self.current_bytes / (1024 * 1024)


def profile_memory_usage(
    func: Callable,
    n: int,
    args: tuple = (),
    kwargs: Optional[dict] = None,
    max_memory_mb: Optional[float] = None,
) -> MemoryProfileResult:
    """
    Menjalankan `func(*args, **kwargs)` sekali sambil melacak alokasi
    memori Python secara rinci lewat tracemalloc, lalu mencatat
    puncak (peak) penggunaannya.
    """
    kwargs = kwargs or {}
    max_memory_mb = max_memory_mb if max_memory_mb is not None else Settings.MAX_MEMORY_MB

    was_tracing = tracemalloc.is_tracing()
    if not was_tracing:
        tracemalloc.start()
    else:
        tracemalloc.clear_traces()

    try:
        func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
    finally:
        if not was_tracing:
            tracemalloc.stop()

    result = MemoryProfileResult(n=n, current_bytes=current, peak_bytes=peak)
    result.exceeded_limit = result.peak_mb > max_memory_mb
    return result


def get_object_size_mb(obj: Any) -> float:
    """Estimasi ukuran satu objek Python (bytes -> MB) menggunakan sys.getsizeof."""
    import sys
    return sys.getsizeof(obj) / (1024 * 1024)
