"""
Modul Transformasi Data (Transformation Module).

Modul mandiri untuk melakukan pembersihan (cleansing) dan konversi
format data. Bersifat stateless per-eksekusi sehingga aman dipanggil
berulang kali secara paralel oleh dispatcher.
"""

from __future__ import annotations

from typing import Any, Dict, List

from src.interfaces.base_module import BaseModule


def strip_whitespace(value: Any) -> Any:
    return value.strip() if isinstance(value, str) else value


def remove_empty(values: List[Any]) -> List[Any]:
    return [v for v in values if v not in (None, "", [], {})]


def normalize_keys(row: Dict[str, Any]) -> Dict[str, Any]:
    """Ubah semua key dict menjadi lowercase + strip, agar konsisten."""
    return {str(k).strip().lower(): v for k, v in row.items()}


class TransformationModule(BaseModule):
    """Membersihkan dan menormalisasi data mentah sebelum diproses lebih lanjut."""

    name = "transformation"

    def initialize(self) -> None:
        self._ready = True

    def execute(self, payload: Any) -> Any:
        """
        payload yang diharapkan salah satu dari:
            {"rows": [ {...}, {...} ]}   -> data tabular
            {"values": [...]}            -> list sederhana
        """
        if isinstance(payload, dict) and "rows" in payload:
            rows = payload["rows"]
            cleaned = [
                normalize_keys({k: strip_whitespace(v) for k, v in row.items()})
                for row in rows
            ]
            return {"rows": cleaned}

        if isinstance(payload, dict) and "values" in payload:
            cleaned_values = remove_empty(
                [strip_whitespace(v) for v in payload["values"]]
            )
            return {"values": cleaned_values}

        return payload

    def cleanup(self) -> None:
        self._ready = False
