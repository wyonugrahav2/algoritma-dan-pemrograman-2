"""
data_loader.py
Memuat data mentah dari berkas eksternal (CSV, JSON, atau list Python)
untuk diproses lebih lanjut oleh sorter.py dan index_builder.py.
"""

import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Union


class DataLoadError(Exception):
    """Dilempar ketika berkas sumber data tidak dapat dibaca atau diparse."""


def load_from_json(path: Union[str, Path]) -> List[Any]:
    """
    Memuat data dari berkas JSON. Mendukung dua format:
      - JSON array langsung: [1, 2, 3, ...]
      - JSON object dengan key "data": {"data": [...]}
    """
    file_path = Path(path)
    if not file_path.exists():
        raise DataLoadError(f"Berkas JSON tidak ditemukan: {file_path}")

    try:
        with file_path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
    except json.JSONDecodeError as exc:
        raise DataLoadError(f"Gagal parsing JSON '{file_path}': {exc}") from exc

    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict) and "data" in raw:
        return raw["data"]

    raise DataLoadError(
        f"Format JSON tidak didukung pada '{file_path}'. "
        "Harus berupa array atau object dengan key 'data'."
    )


def load_from_csv(path: Union[str, Path], column: str = "value") -> List[Dict[str, Any]]:
    """
    Memuat data dari berkas CSV sebagai list of dict (setiap baris menjadi
    satu record). Parameter `column` menunjukkan kolom mana yang akan
    dianggap sebagai nilai pencarian utama jika diperlukan validasi.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise DataLoadError(f"Berkas CSV tidak ditemukan: {file_path}")

    records: List[Dict[str, Any]] = []
    with file_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if column not in (reader.fieldnames or []):
            raise DataLoadError(
                f"Kolom '{column}' tidak ditemukan di header CSV: {reader.fieldnames}"
            )
        for row in reader:
            records.append(row)

    return records


def load_from_list(raw_values: List[Any]) -> List[Any]:
    """Wrapper sederhana untuk data yang sudah berupa list Python di memori."""
    if not isinstance(raw_values, list):
        raise DataLoadError("Input harus berupa list.")
    return list(raw_values)


def coerce_numeric(records: List[Any], field_name: str = "value") -> List[float]:
    """
    Mengubah kumpulan record (bisa berupa dict, str, atau angka mentah)
    menjadi list angka float, untuk keperluan algoritma pencarian yang
    membutuhkan perbandingan numerik (Binary/Interpolation/Exponential).
    """
    numeric_values: List[float] = []
    for i, record in enumerate(records):
        try:
            if isinstance(record, dict):
                numeric_values.append(float(record[field_name]))
            else:
                numeric_values.append(float(record))
        except (KeyError, TypeError, ValueError) as exc:
            raise DataLoadError(
                f"Gagal mengonversi record ke-{i} ('{record}') menjadi angka: {exc}"
            ) from exc
    return numeric_values
