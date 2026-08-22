"""
parsers.py
Menerjemahkan argumen perintah teks dari CLI menjadi objek tipe data
terstruktur yang siap diolah oleh core engine.
"""

from typing import List

from src.domain.exceptions import ParsingError
from src.domain.models import InputDataType, RawInput, ValidatedInput
from src.input_layer.validators import sanitize_raw_string, validate_numeric_range


def parse_to_int(raw_input: RawInput) -> ValidatedInput:
    """Mengonversi RawInput menjadi integer yang tervalidasi."""
    cleaned = sanitize_raw_string(raw_input.raw_value)
    try:
        value = int(cleaned)
    except ValueError as exc:
        raise ParsingError(f"Gagal mengonversi '{cleaned}' menjadi integer.") from exc
    validate_numeric_range(value)
    return ValidatedInput(value=value, data_type=InputDataType.INTEGER, original=raw_input)


def parse_to_float(raw_input: RawInput) -> ValidatedInput:
    """Mengonversi RawInput menjadi float yang tervalidasi."""
    cleaned = sanitize_raw_string(raw_input.raw_value)
    try:
        value = float(cleaned)
    except ValueError as exc:
        raise ParsingError(f"Gagal mengonversi '{cleaned}' menjadi float.") from exc
    validate_numeric_range(value)
    return ValidatedInput(value=value, data_type=InputDataType.FLOAT, original=raw_input)


def parse_to_string(raw_input: RawInput) -> ValidatedInput:
    """Mengonversi RawInput menjadi string bersih."""
    cleaned = sanitize_raw_string(raw_input.raw_value)
    return ValidatedInput(value=cleaned, data_type=InputDataType.STRING, original=raw_input)


def parse_to_list(raw_input: RawInput, delimiter: str = ",") -> ValidatedInput:
    """Mengonversi RawInput yang dipisahkan delimiter menjadi list of float."""
    cleaned = sanitize_raw_string(raw_input.raw_value)
    parts = [p.strip() for p in cleaned.split(delimiter) if p.strip()]
    if not parts:
        raise ParsingError("Tidak ada elemen valid yang dapat diparsing menjadi list.")

    result: List[float] = []
    for part in parts:
        try:
            result.append(float(part))
        except ValueError as exc:
            raise ParsingError(f"Elemen '{part}' bukan angka yang valid.") from exc

    return ValidatedInput(value=result, data_type=InputDataType.LIST, original=raw_input)


# Registry parser agar mudah diperluas tanpa mengubah pemanggil (open-closed principle)
PARSER_REGISTRY = {
    InputDataType.INTEGER: parse_to_int,
    InputDataType.FLOAT: parse_to_float,
    InputDataType.STRING: parse_to_string,
    InputDataType.LIST: parse_to_list,
}


def parse(raw_input: RawInput, target_type: InputDataType) -> ValidatedInput:
    """Dispatcher utama: memilih parser yang sesuai berdasarkan target_type."""
    parser_fn = PARSER_REGISTRY.get(target_type)
    if parser_fn is None:
        raise ParsingError(f"Tidak ada parser terdaftar untuk tipe {target_type}.")
    return parser_fn(raw_input)
