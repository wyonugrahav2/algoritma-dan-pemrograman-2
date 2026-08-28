"""
profiler.py
------------
Profiler untuk melacak Call Stack Depth dan konsumsi memori puncak
(peak memory usage) selama eksekusi fungsi rekursif maupun iteratif.
"""

import sys
import tracemalloc
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class ProfileResult:
    """Menyimpan hasil profiling satu eksekusi fungsi."""
    result: Any
    peak_memory_bytes: int
    stack_depth_estimate: int


def profile_execution(func: Callable, *args, **kwargs) -> ProfileResult:
    """
    Menjalankan sebuah fungsi sambil melacak penggunaan memori puncak
    (menggunakan tracemalloc) dan estimasi kedalaman stack sebelum dan
    sesudah eksekusi.

    Args:
        func: fungsi yang akan diprofilkan.
        *args, **kwargs: argumen yang diteruskan ke fungsi.

    Returns:
        ProfileResult berisi hasil eksekusi, memori puncak (bytes), dan
        estimasi kedalaman stack tambahan yang digunakan.
    """
    depth_before = _current_stack_depth()

    tracemalloc.start()
    try:
        result = func(*args, **kwargs)
        _, peak_memory = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    depth_after = _current_stack_depth()

    return ProfileResult(
        result=result,
        peak_memory_bytes=peak_memory,
        stack_depth_estimate=max(depth_after - depth_before, 0),
    )


def _current_stack_depth() -> int:
    """Mengembalikan kedalaman call stack Python saat ini."""
    frame = sys._getframe()
    depth = 0
    while frame is not None:
        depth += 1
        frame = frame.f_back
    return depth


def format_bytes(num_bytes: int) -> str:
    """Memformat ukuran byte menjadi representasi yang mudah dibaca."""
    value = float(num_bytes)
    for unit in ["B", "KB", "MB", "GB"]:
        if value < 1024.0:
            return f"{value:.2f} {unit}"
        value /= 1024.0
    return f"{value:.2f} TB"
