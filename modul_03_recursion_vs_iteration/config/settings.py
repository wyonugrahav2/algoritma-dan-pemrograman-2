"""
settings.py
------------
Konfigurasi batas maksimum kedalaman rekursi (recursion limit),
batasan waktu pemrosesan (timeout), dan parameter eksekusi lainnya.
"""

import os
import sys

# Batas maksimum kedalaman rekursi Python (default interpreter ~1000).
# Bisa dioverride lewat environment variable MAX_RECURSION_DEPTH.
MAX_RECURSION_DEPTH = int(os.getenv("MAX_RECURSION_DEPTH", 3000))

# Batas waktu eksekusi per pengujian (dalam detik) sebelum dianggap timeout.
EXECUTION_TIMEOUT_SECONDS = float(os.getenv("EXECUTION_TIMEOUT_SECONDS", 5.0))

# Jumlah pengulangan (repeat) setiap benchmark untuk hasil yang lebih stabil.
BENCHMARK_REPEAT_COUNT = int(os.getenv("BENCHMARK_REPEAT_COUNT", 5))

# Apakah stack overflow guard aktif secara default.
ENABLE_STACK_OVERFLOW_GUARD = True


def apply_recursion_limit():
    """Menerapkan batas rekursi ke Python interpreter."""
    sys.setrecursionlimit(MAX_RECURSION_DEPTH)


def get_settings_summary() -> dict:
    """Mengembalikan ringkasan konfigurasi aktif saat ini."""
    return {
        "max_recursion_depth": MAX_RECURSION_DEPTH,
        "execution_timeout_seconds": EXECUTION_TIMEOUT_SECONDS,
        "benchmark_repeat_count": BENCHMARK_REPEAT_COUNT,
        "stack_overflow_guard_enabled": ENABLE_STACK_OVERFLOW_GUARD,
    }
