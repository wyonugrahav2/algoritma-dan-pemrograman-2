"""Sengaja menyuntikkan error untuk menguji ketahanan sistem (Chaos Engineering)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from src.resilience.retry_handler import retry_call, RetryExhaustedError
from src.resilience.fallback_manager import with_fallback


def test_retry_recovers_after_transient_failures():
    calls = {"count": 0}

    def flaky():
        calls["count"] += 1
        if calls["count"] < 3:
            raise ConnectionError("simulasi gangguan jaringan")
        return "sukses"

    result = retry_call(flaky, max_attempts=5, base_backoff=0.001, sleep_fn=lambda s: None)
    assert result == "sukses"
    assert calls["count"] == 3


def test_retry_exhausted_raises_custom_error():
    def always_fails():
        raise ValueError("selalu gagal")

    with pytest.raises(RetryExhaustedError):
        retry_call(always_fails, max_attempts=3, base_backoff=0.001, sleep_fn=lambda s: None)


def test_fallback_triggered_when_primary_fails():
    def primary():
        raise RuntimeError("komponen utama down")

    def backup():
        return "data-cadangan"

    result = with_fallback(primary, backup, enabled=True)
    assert result == "data-cadangan"
