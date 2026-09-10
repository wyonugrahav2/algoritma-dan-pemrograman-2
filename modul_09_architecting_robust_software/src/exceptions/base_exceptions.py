"""Kelas dasar exception aplikasi yang menjadi induk seluruh galat kustom."""
from __future__ import annotations

from datetime import datetime, timezone


class AppException(Exception):
    """Base exception untuk seluruh error kustom dalam sistem.

    Setiap exception turunan wajib membawa `error_code` agar dapat
    dilacak secara konsisten pada log audit dan laporan crash.
    """

    def __init__(self, message: str, error_code: str = "SYS-000", *, cause: Exception | None = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.cause = cause
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        return {
            "error_code": self.error_code,
            "message": self.message,
            "timestamp": self.timestamp,
            "cause": repr(self.cause) if self.cause else None,
            "exception_type": type(self).__name__,
        }

    def __str__(self) -> str:
        return f"[{self.error_code}] {self.message}"
