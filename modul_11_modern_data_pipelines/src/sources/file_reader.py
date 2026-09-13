"""
file_reader.py
Pembaca berkas berbasis Generator/Yield yang memuat data baris demi baris
dari berkas CSV/JSON berukuran raksasa tanpa memuat seluruh isi ke RAM.
"""

import csv
import json
from typing import Iterator, Dict, Any

from config.settings import settings


def read_csv_lazy(path: str, delimiter: str = None) -> Iterator[Dict[str, Any]]:
    """
    Membaca berkas CSV baris demi baris menggunakan generator (Lazy Evaluation).
    Cocok untuk berkas berukuran raksasa karena hanya satu baris yang berada
    di memori pada satu waktu.
    """
    delimiter = delimiter or settings.CSV_DELIMITER
    with open(path, "r", encoding=settings.FILE_ENCODING, newline="") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            yield dict(row)


def read_json_lines_lazy(path: str) -> Iterator[Dict[str, Any]]:
    """
    Membaca berkas JSON Lines (.jsonl) — satu objek JSON per baris —
    secara streaming tanpa memuat seluruh berkas ke memori.
    """
    with open(path, "r", encoding=settings.FILE_ENCODING) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def read_json_array_lazy(path: str) -> Iterator[Dict[str, Any]]:
    """
    Membaca berkas JSON berformat array besar ([{...}, {...}, ...])
    menggunakan pendekatan streaming berbasis ijson jika tersedia, dengan
    fallback ke json.load standar (memuat penuh) bila ijson tidak terpasang.
    """
    try:
        import ijson  # streaming JSON parser (opsional)
        with open(path, "rb") as f:
            for obj in ijson.items(f, "item"):
                yield obj
    except ImportError:
        # Fallback: dataset kecil/menengah tanpa dependensi tambahan
        with open(path, "r", encoding=settings.FILE_ENCODING) as f:
            data = json.load(f)
        for obj in data:
            yield obj


def read_chunks(iterator: Iterator[Dict[str, Any]], chunk_size: int = None):
    """
    Mengelompokkan iterator baris menjadi potongan (chunk) berukuran tetap,
    berguna untuk operasi batch-write atau agregasi per kelompok.
    """
    chunk_size = chunk_size or settings.CHUNK_SIZE
    chunk = []
    for record in iterator:
        chunk.append(record)
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk
