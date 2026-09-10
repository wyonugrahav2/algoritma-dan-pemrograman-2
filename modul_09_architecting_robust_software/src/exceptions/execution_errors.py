"""Menangani kesalahan alokasi/sumber daya sistem saat eksekusi."""
from __future__ import annotations

from config.error_codes import (
    ERR_RESOURCE_UNAVAILABLE,
    ERR_TIMEOUT,
    ERR_UNEXPECTED_FAILURE,
)
from src.exceptions.base_exceptions import AppException


class ExecutionError(AppException):
    """Kelas dasar untuk seluruh error saat eksekusi proses bisnis."""

    def __init__(self, message: str, error_code: str = ERR_UNEXPECTED_FAILURE, **kwargs):
        super().__init__(message, error_code, **kwargs)


class OperationTimeoutError(ExecutionError):
    def __init__(self, operation: str, timeout_seconds: float):
        super().__init__(
            f"Operasi '{operation}' melebihi batas waktu {timeout_seconds}s.",
            error_code=ERR_TIMEOUT,
        )
        self.operation = operation
        self.timeout_seconds = timeout_seconds


class ResourceUnavailableError(ExecutionError):
    def __init__(self, resource: str, reason: str = ""):
        detail = f" ({reason})" if reason else ""
        super().__init__(
            f"Sumber daya '{resource}' tidak tersedia{detail}.",
            error_code=ERR_RESOURCE_UNAVAILABLE,
        )
        self.resource = resource


class UnexpectedFailureError(ExecutionError):
    def __init__(self, message: str, cause: Exception | None = None):
        super().__init__(message, error_code=ERR_UNEXPECTED_FAILURE, cause=cause)
