"""
memory_tracker.py
------------------
Melacak alokasi memori tambahan (auxiliary memory) yang digunakan oleh
sebuah algoritma sorting, memakai modul bawaan `tracemalloc`.

Ini memungkinkan kita membandingkan klaim teoritis "In-Place O(1)" vs
"Auxiliary O(N)" dengan angka pengukuran nyata dalam satuan byte.
"""

import tracemalloc
from contextlib import contextmanager


class MemoryTracker:
    """Mengukur puncak penggunaan memori selama sebuah blok kode dieksekusi."""

    def __init__(self):
        self.peak_bytes = 0
        self.current_bytes = 0

    @contextmanager
    def track(self):
        """Context manager: pakai dengan `with memory_tracker.track():`."""
        tracemalloc.start()
        try:
            yield self
        finally:
            current, peak = tracemalloc.get_traced_memory()
            self.current_bytes = current
            self.peak_bytes = peak
            tracemalloc.stop()

    @property
    def peak_kb(self) -> float:
        return round(self.peak_bytes / 1024, 3)

    def __repr__(self) -> str:
        return f"MemoryTracker(peak_kb={self.peak_kb})"
