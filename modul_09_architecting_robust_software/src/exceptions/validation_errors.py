"""Menangani kesalahan spesifik pada masukan pengguna."""
from __future__ import annotations

from config.error_codes import ERR_INVALID_INPUT, ERR_MISSING_FIELD, ERR_OUT_OF_RANGE
from src.exceptions.base_exceptions import AppException


class ValidationError(AppException):
    """Kelas dasar untuk seluruh error validasi input."""

    def __init__(self, message: str, error_code: str = ERR_INVALID_INPUT, **kwargs):
        super().__init__(message, error_code, **kwargs)


class InvalidInputError(ValidationError):
    def __init__(self, field: str, value):
        super().__init__(
            f"Nilai tidak valid pada field '{field}': {value!r}",
            error_code=ERR_INVALID_INPUT,
        )
        self.field = field
        self.value = value


class MissingFieldError(ValidationError):
    def __init__(self, field: str):
        super().__init__(
            f"Field wajib '{field}' tidak ditemukan.",
            error_code=ERR_MISSING_FIELD,
        )
        self.field = field


class OutOfRangeError(ValidationError):
    def __init__(self, field: str, value, minimum=None, maximum=None):
        super().__init__(
            f"Nilai '{field}'={value!r} berada di luar batas "
            f"[{minimum}, {maximum}].",
            error_code=ERR_OUT_OF_RANGE,
        )
        self.field = field
        self.value = value
        self.minimum = minimum
        self.maximum = maximum
