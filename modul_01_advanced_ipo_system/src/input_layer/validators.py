"""
validators.py
Sanitasi data, range checking, dan pemastian integritas data masukan
sebelum diteruskan ke process layer.
"""

from typing import Any

from config.constants import MIN_VALUE_THRESHOLD, MAX_VALUE_THRESHOLD
from src.domain.exceptions import (
    EmptyInputError,
    ValueOutOfRangeError,
    InputValidationError,
)
from src.domain.models import RawInput


def sanitize_raw_string(value: str) -> str:
    """Membersihkan whitespace berlebih dan karakter kontrol dari input."""
    if value is None:
        raise EmptyInputError()
    cleaned = value.strip()
    if not cleaned:
        raise EmptyInputError()
    return cleaned


def validate_not_empty(raw_input: RawInput) -> RawInput:
    """Memastikan RawInput tidak kosong setelah sanitasi."""
    sanitize_raw_string(raw_input.raw_value)
    return raw_input


def validate_numeric_range(
    value: float,
    min_value: float = MIN_VALUE_THRESHOLD,
    max_value: float = MAX_VALUE_THRESHOLD,
) -> float:
    """Memastikan nilai numerik berada dalam batas ambang batas yang diizinkan."""
    if value < min_value or value > max_value:
        raise ValueOutOfRangeError(
            f"Nilai {value} berada di luar batas [{min_value}, {max_value}]."
        )
    return value


def validate_type(value: Any, expected_type: type) -> Any:
    """Memvalidasi bahwa nilai sesuai dengan tipe data yang diharapkan."""
    if not isinstance(value, expected_type):
        raise InputValidationError(
            f"Tipe data tidak sesuai. Diharapkan {expected_type.__name__}, "
            f"diterima {type(value).__name__}."
        )
    return value


def validate_max_length(value: str, max_length: int) -> str:
    """Memvalidasi panjang string tidak melebihi batas maksimum."""
    if len(value) > max_length:
        raise InputValidationError(
            f"Panjang input ({len(value)}) melebihi batas maksimum ({max_length})."
        )
    return value
