"""Circuit Breaker: memutus eksekusi komponen yang gagal berulang kali.

Implementasi state machine tiga status klasik:
CLOSED -> (gagal beruntun >= threshold) -> OPEN
OPEN -> (recovery_seconds terlampaui) -> HALF_OPEN
HALF_OPEN -> (sukses) -> CLOSED | (gagal) -> OPEN
"""
from __future__ import annotations

import time
from enum import Enum
from typing import Callable, TypeVar

from config.settings import CIRCUIT_FAILURE_THRESHOLD, CIRCUIT_RECOVERY_SECONDS
from config.error_codes import ERR_CIRCUIT_OPEN
from src.exceptions.execution_errors import ExecutionError

T = TypeVar("T")


class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitOpenError(ExecutionError):
    def __init__(self, name: str):
        super().__init__(
            f"Circuit breaker '{name}' sedang OPEN, permintaan ditolak.",
            error_code=ERR_CIRCUIT_OPEN,
        )
        self.name = name


class CircuitBreaker:
    """Circuit breaker sederhana yang bisa dipakai sebagai wrapper eksekusi."""

    def __init__(
        self,
        name: str = "default",
        failure_threshold: int = CIRCUIT_FAILURE_THRESHOLD,
        recovery_seconds: float = CIRCUIT_RECOVERY_SECONDS,
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_seconds = recovery_seconds

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._opened_at: float | None = None

    @property
    def state(self) -> CircuitState:
        if self._state == CircuitState.OPEN and self._opened_at is not None:
            elapsed = time.monotonic() - self._opened_at
            if elapsed >= self.recovery_seconds:
                self._state = CircuitState.HALF_OPEN
        return self._state

    def _record_success(self) -> None:
        self._failure_count = 0
        self._state = CircuitState.CLOSED
        self._opened_at = None

    def _record_failure(self) -> None:
        self._failure_count += 1
        if self._failure_count >= self.failure_threshold or self._state == CircuitState.HALF_OPEN:
            self._state = CircuitState.OPEN
            self._opened_at = time.monotonic()

    def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        current_state = self.state
        if current_state == CircuitState.OPEN:
            raise CircuitOpenError(self.name)

        try:
            result = func(*args, **kwargs)
        except Exception:
            self._record_failure()
            raise
        else:
            self._record_success()
            return result

    def reset(self) -> None:
        """Reset paksa circuit breaker ke kondisi CLOSED (untuk testing/admin)."""
        self._failure_count = 0
        self._state = CircuitState.CLOSED
        self._opened_at = None
