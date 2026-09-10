"""Uji fungsi pemutus sirkuit (circuit breaker) saat kegagalan beruntun."""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from src.resilience.circuit_breaker import CircuitBreaker, CircuitOpenError, CircuitState


def test_circuit_opens_after_threshold_failures():
    breaker = CircuitBreaker(name="test", failure_threshold=3, recovery_seconds=100)

    def failing():
        raise RuntimeError("gagal terus")

    for _ in range(3):
        with pytest.raises(RuntimeError):
            breaker.call(failing)

    assert breaker.state == CircuitState.OPEN

    with pytest.raises(CircuitOpenError):
        breaker.call(failing)


def test_circuit_transitions_to_half_open_after_recovery():
    breaker = CircuitBreaker(name="test2", failure_threshold=1, recovery_seconds=0.05)

    def failing():
        raise RuntimeError("gagal")

    with pytest.raises(RuntimeError):
        breaker.call(failing)
    assert breaker.state == CircuitState.OPEN

    time.sleep(0.1)
    assert breaker.state == CircuitState.HALF_OPEN


def test_circuit_closes_after_success():
    breaker = CircuitBreaker(name="test3", failure_threshold=1, recovery_seconds=100)
    breaker.call(lambda: "ok")
    assert breaker.state == CircuitState.CLOSED
