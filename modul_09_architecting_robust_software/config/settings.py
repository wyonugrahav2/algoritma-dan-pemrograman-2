"""Konfigurasi global sistem: threshold retry, timeout, dan fallback options.

Semua nilai dapat dioverride lewat environment variable agar tidak ada
konfigurasi yang hardcoded secara tersembunyi.
"""
import os


def _get_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


def _get_float(name: str, default: float) -> float:
    try:
        return float(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


# --- Retry / Exponential Backoff ---
MAX_RETRY_ATTEMPTS: int = _get_int("MAX_RETRY_ATTEMPTS", 3)
BASE_BACKOFF_SECONDS: float = _get_float("BASE_BACKOFF_SECONDS", 0.5)
MAX_BACKOFF_SECONDS: float = _get_float("MAX_BACKOFF_SECONDS", 8.0)

# --- Timeout ---
DEFAULT_TIMEOUT_SECONDS: float = _get_float("DEFAULT_TIMEOUT_SECONDS", 5.0)

# --- Circuit Breaker ---
CIRCUIT_FAILURE_THRESHOLD: int = _get_int("CIRCUIT_FAILURE_THRESHOLD", 5)
CIRCUIT_RECOVERY_SECONDS: float = _get_float("CIRCUIT_RECOVERY_SECONDS", 10.0)
CIRCUIT_HALF_OPEN_MAX_CALLS: int = _get_int("CIRCUIT_HALF_OPEN_MAX_CALLS", 1)

# --- Fallback ---
FALLBACK_ENABLED: bool = os.environ.get("FALLBACK_ENABLED", "true").lower() == "true"

# --- Health Check ---
HEALTH_CHECK_MIN_DISK_MB: int = _get_int("HEALTH_CHECK_MIN_DISK_MB", 50)

# --- Logging / Crash reports ---
CRASH_LOG_DIR: str = os.environ.get("CRASH_LOG_DIR", "logs")
