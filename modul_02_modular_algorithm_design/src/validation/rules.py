"""
Modul Validasi (Validation Module).

Modul independen berisi aturan-aturan validasi (validation rules) yang
bisa dipasang atau dilepas secara fleksibel. Setiap rule adalah fungsi
kecil dan mandiri, dikumpulkan lalu dijalankan berurutan terhadap data.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List

from src.interfaces.base_module import BaseModule

# Tipe untuk sebuah rule: menerima data, mengembalikan (valid, pesan_error)
Rule = Callable[[Any], tuple[bool, str]]


def rule_not_empty(value: Any) -> tuple[bool, str]:
    is_valid = value not in (None, "", [], {})
    return is_valid, "" if is_valid else "Nilai tidak boleh kosong."


def rule_is_numeric(value: Any) -> tuple[bool, str]:
    is_valid = isinstance(value, (int, float)) and not isinstance(value, bool)
    return is_valid, "" if is_valid else "Nilai harus berupa angka."


def rule_positive(value: Any) -> tuple[bool, str]:
    is_valid = isinstance(value, (int, float)) and value > 0
    return is_valid, "" if is_valid else "Nilai harus lebih besar dari nol."


def rule_max_length(max_len: int) -> Rule:
    """Rule generator: batasi panjang string/list."""

    def _rule(value: Any) -> tuple[bool, str]:
        is_valid = hasattr(value, "__len__") and len(value) <= max_len
        return is_valid, "" if is_valid else f"Panjang maksimal adalah {max_len}."

    return _rule


DEFAULT_RULES: List[Rule] = [rule_not_empty]


class ValidationModule(BaseModule):
    """Menjalankan sekumpulan validation rules terhadap data yang masuk."""

    name = "validation"

    def initialize(self) -> None:
        # Ambil rules dari config jika ada, kalau tidak pakai default.
        self.rules: List[Rule] = self.config.get("rules", DEFAULT_RULES)

    def execute(self, payload: Any) -> Dict[str, Any]:
        """
        payload yang diharapkan:
            {"data": <nilai_yang_divalidasi>}
        """
        value = payload.get("data") if isinstance(payload, dict) else payload

        errors: List[str] = []
        for rule in self.rules:
            is_valid, message = rule(value)
            if not is_valid:
                errors.append(message)

        return {"valid": len(errors) == 0, "errors": errors}

    def cleanup(self) -> None:
        self.rules = []
