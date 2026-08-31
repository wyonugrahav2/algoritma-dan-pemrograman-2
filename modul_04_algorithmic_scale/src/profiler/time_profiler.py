"""
time_profiler.py
Mengukur waktu eksekusi real-time sebuah fungsi target, dengan
dukungan multi-repeat untuk mengurangi noise, serta deteksi timeout.
"""

import time
import signal
import statistics
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional

from config.settings import Settings


class ExecutionTimeoutError(Exception):
    """Dilempar ketika eksekusi fungsi melebihi batas waktu yang diizinkan."""
    pass


@dataclass
class TimeProfileResult:
    """Hasil pengukuran waktu eksekusi untuk satu fungsi pada satu N."""
    n: int
    durations_seconds: List[float] = field(default_factory=list)
    timed_out: bool = False

    @property
    def mean_seconds(self) -> float:
        if not self.durations_seconds:
            return float("inf")
        return statistics.mean(self.durations_seconds)

    @property
    def min_seconds(self) -> float:
        if not self.durations_seconds:
            return float("inf")
        return min(self.durations_seconds)

    @property
    def stdev_seconds(self) -> float:
        if len(self.durations_seconds) < 2:
            return 0.0
        return statistics.stdev(self.durations_seconds)


def _with_timeout(func: Callable, args: tuple, kwargs: dict, timeout_seconds: float) -> Any:
    """
    Menjalankan fungsi dengan batas waktu menggunakan SIGALRM (Unix only).
    Jika platform tidak mendukung SIGALRM, jalankan tanpa timeout keras.
    """
    def _handler(signum, frame):
        raise ExecutionTimeoutError(f"Eksekusi melebihi {timeout_seconds} detik")

    has_alarm = hasattr(signal, "SIGALRM")
    if has_alarm:
        old_handler = signal.signal(signal.SIGALRM, _handler)
        signal.setitimer(signal.ITIMER_REAL, timeout_seconds)
    try:
        return func(*args, **kwargs)
    finally:
        if has_alarm:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, old_handler)


def profile_execution_time(
    func: Callable,
    n: int,
    args: tuple = (),
    kwargs: Optional[dict] = None,
    repeats: Optional[int] = None,
    timeout_seconds: Optional[float] = None,
) -> TimeProfileResult:
    """
    Menjalankan `func(*args, **kwargs)` sebanyak `repeats` kali dan
    mencatat durasi tiap eksekusi. Jika salah satu eksekusi melebihi
    `timeout_seconds`, hasil ditandai timed_out=True dan pengukuran
    dihentikan.
    """
    kwargs = kwargs or {}
    repeats = repeats if repeats is not None else Settings.REPEATS_PER_MEASUREMENT
    timeout_seconds = timeout_seconds if timeout_seconds is not None else Settings.EXECUTION_TIMEOUT_SECONDS

    result = TimeProfileResult(n=n)

    for _ in range(repeats):
        start = time.perf_counter()
        try:
            _with_timeout(func, args, kwargs, timeout_seconds)
        except ExecutionTimeoutError:
            result.timed_out = True
            break
        end = time.perf_counter()
        result.durations_seconds.append(end - start)

    return result
