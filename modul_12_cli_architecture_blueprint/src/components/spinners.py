"""
spinners.py
Indikator pemuatan (loading spinner) untuk proses yang berjalan
lebih dari sekejap. run_with_spinner menjalankan sebuah callable
sambil menampilkan animasi spinner di terminal (dinonaktifkan
otomatis jika output bukan TTY, misalnya saat dipipe ke berkas).
"""

import itertools
import sys
import threading
import time
from typing import Any, Callable


_FRAMES = ["|", "/", "-", "\\"]


def run_with_spinner(message: str, task: Callable[[], Any], interval: float = 0.08) -> Any:
    """
    Menjalankan `task()` di thread terpisah sambil menampilkan spinner
    berlabel `message`. Mengembalikan hasil dari task().
    """
    if not sys.stdout.isatty():
        # Non-interaktif (pipe/redirect): jangan cetak animasi, cukup jalankan.
        return task()

    result_holder = {}
    error_holder = {}

    def _runner():
        try:
            result_holder["value"] = task()
        except Exception as exc:  # noqa: BLE001
            error_holder["error"] = exc

    thread = threading.Thread(target=_runner)
    thread.start()

    for frame in itertools.cycle(_FRAMES):
        if not thread.is_alive():
            break
        sys.stdout.write(f"\r{frame} {message}")
        sys.stdout.flush()
        time.sleep(interval)

    thread.join()
    sys.stdout.write("\r" + " " * (len(message) + 2) + "\r")
    sys.stdout.flush()

    if "error" in error_holder:
        raise error_holder["error"]
    return result_holder.get("value")
