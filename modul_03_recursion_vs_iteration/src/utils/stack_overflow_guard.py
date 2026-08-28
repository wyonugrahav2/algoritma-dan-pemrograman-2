"""
stack_overflow_guard.py
--------------------------
Wrapper/Decorator yang menangkap RecursionError secara otomatis agar
sistem tidak mendadak runtuh (crash) saat mengeksekusi data besar.
"""

from functools import wraps
from typing import Any, Callable, Optional, Tuple


def stack_overflow_guard(func: Callable) -> Callable:
    """
    Decorator yang membungkus fungsi agar RecursionError tertangkap
    dengan aman, tanpa menghentikan keseluruhan program.

    Args:
        func: fungsi yang akan dilindungi.

    Returns:
        Fungsi wrapper yang mengembalikan None jika RecursionError
        terjadi (bersama pesan yang dicetak ke stderr).
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RecursionError as exc:
            print(f"[stack_overflow_guard] {func.__name__} mengalami "
                  f"RecursionError: {exc}")
            return None

    return wrapper


def guarded_call(func: Callable, *args, **kwargs) -> Tuple[Optional[Any], Optional[str]]:
    """
    Menjalankan sebuah fungsi dengan proteksi terhadap RecursionError
    maupun exception umum lainnya, mengembalikan hasil beserta pesan
    error (jika ada) tanpa menghentikan eksekusi program.

    Args:
        func: fungsi yang akan dijalankan.
        *args, **kwargs: argumen yang diteruskan ke fungsi.

    Returns:
        Tuple (hasil, pesan_error). Jika sukses, pesan_error bernilai None.
        Jika gagal, hasil bernilai None dan pesan_error berisi deskripsi.
    """
    try:
        result = func(*args, **kwargs)
        return result, None
    except RecursionError as exc:
        return None, f"RecursionError: {exc}"
    except Exception as exc:  # noqa: BLE001 - guard generik disengaja
        return None, f"{type(exc).__name__}: {exc}"
