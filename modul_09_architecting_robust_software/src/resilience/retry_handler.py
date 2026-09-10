"""Mengeksekusi percobaan ulang otomatis dengan strategi Exponential Backoff."""
from __future__ import annotations

import random
import time
from typing import Callable, Iterable, Type, TypeVar

from config.settings import (
    BASE_BACKOFF_SECONDS,
    MAX_BACKOFF_SECONDS,
    MAX_RETRY_ATTEMPTS,
)
from config.error_codes import ERR_RETRY_EXHAUSTED
from src.exceptions.execution_errors import ExecutionError

T = TypeVar("T")


class RetryExhaustedError(ExecutionError):
    def __init__(self, attempts: int, last_error: Exception):
        super().__init__(
            f"Seluruh {attempts} percobaan gagal. Error terakhir: {last_error!r}",
            error_code=ERR_RETRY_EXHAUSTED,
            cause=last_error,
        )
        self.attempts = attempts
        self.last_error = last_error


def _compute_backoff(attempt: int, base: float, cap: float) -> float:
    """Exponential backoff dengan sedikit jitter agar tidak thundering herd."""
    delay = min(cap, base * (2 ** (attempt - 1)))
    jitter = random.uniform(0, delay * 0.1)
    return delay + jitter


def retry_call(
    func: Callable[..., T],
    *args,
    max_attempts: int = MAX_RETRY_ATTEMPTS,
    base_backoff: float = BASE_BACKOFF_SECONDS,
    max_backoff: float = MAX_BACKOFF_SECONDS,
    retry_on: Iterable[Type[BaseException]] = (Exception,),
    on_retry: Callable[[int, BaseException], None] | None = None,
    sleep_fn: Callable[[float], None] = time.sleep,
    **kwargs,
) -> T:
    """Menjalankan `func` dengan retry otomatis + exponential backoff.

    on_retry(attempt_number, exception) dipanggil setiap kali retry terjadi,
    berguna untuk logging tanpa membuat fungsi ini terikat pada logger tertentu.
    """
    last_error: BaseException | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            return func(*args, **kwargs)
        except tuple(retry_on) as exc:  # type: ignore[misc]
            last_error = exc
            if attempt == max_attempts:
                break
            if on_retry:
                on_retry(attempt, exc)
            sleep_fn(_compute_backoff(attempt, base_backoff, max_backoff))

    assert last_error is not None
    raise RetryExhaustedError(max_attempts, last_error)
