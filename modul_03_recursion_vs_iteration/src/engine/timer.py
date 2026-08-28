"""
timer.py
---------
Microsecond precision timer menggunakan time.perf_counter().
"""

import time
from functools import wraps


class Timer:
    """Context manager untuk mengukur durasi eksekusi blok kode."""

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.elapsed_seconds = None

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        self.elapsed_seconds = self.end_time - self.start_time
        return False

    @property
    def elapsed_microseconds(self) -> float:
        """Mengembalikan durasi eksekusi dalam mikrodetik."""
        if self.elapsed_seconds is None:
            return 0.0
        return self.elapsed_seconds * 1_000_000


def measure_execution_time(func, *args, **kwargs):
    """
    Mengukur waktu eksekusi sebuah fungsi dalam mikrodetik.

    Args:
        func: fungsi yang akan diukur.
        *args, **kwargs: argumen yang diteruskan ke fungsi.

    Returns:
        Tuple (hasil_fungsi, waktu_eksekusi_mikrodetik).
    """
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    elapsed_us = (end - start) * 1_000_000
    return result, elapsed_us


def timed(func):
    """Decorator yang mencetak waktu eksekusi sebuah fungsi (µs)."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        result, elapsed_us = measure_execution_time(func, *args, **kwargs)
        print(f"[timer] {func.__name__} selesai dalam {elapsed_us:.3f} µs")
        return result

    return wrapper
