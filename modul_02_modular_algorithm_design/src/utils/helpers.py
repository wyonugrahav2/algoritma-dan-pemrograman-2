"""
Helper umum yang dipakai lintas modul, tetapi tetap terisolasi
(tidak bergantung pada logika bisnis modul manapun).
"""

from __future__ import annotations

import time
import uuid
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def generate_id() -> str:
    """Buat ID unik, misalnya untuk melacak satu eksekusi pipeline."""
    return str(uuid.uuid4())


def timed(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator sederhana untuk mengukur waktu eksekusi sebuah fungsi."""

    def wrapper(*args: Any, **kwargs: Any) -> T:
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            print(f"[timed] {func.__name__} selesai dalam {elapsed:.4f} detik")

    return wrapper


def chunk_list(items: list, size: int) -> list[list]:
    """Pecah list menjadi beberapa list kecil berukuran `size`."""
    if size <= 0:
        raise ValueError("size harus lebih besar dari 0")
    return [items[i:i + size] for i in range(0, len(items), size)]


def deep_get(data: dict, dotted_key: str, default: Any = None) -> Any:
    """Ambil nilai bersarang dari dict lewat key ber-titik, mis. 'a.b.c'."""
    keys = dotted_key.split(".")
    current: Any = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current
