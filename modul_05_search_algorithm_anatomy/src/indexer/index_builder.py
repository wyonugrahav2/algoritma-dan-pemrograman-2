"""
index_builder.py
Membangun Inverted Index dan struktur Hash Map untuk mendukung
mekanisme pencarian instan O(1) pada src/algorithms/hash_search.py.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Sequence


@dataclass
class HashIndex:
    """
    Struktur hash map sederhana: key -> list posisi (mendukung duplikat).
    Menyimpan juga metadata load factor untuk keperluan validasi
    integritas (lihat tests/test_index_integrity.py).
    """

    table: Dict[Any, List[int]] = field(default_factory=lambda: defaultdict(list))
    bucket_count: int = 16
    total_keys_inserted: int = 0

    def load_factor(self) -> float:
        unique_keys = len(self.table)
        return unique_keys / self.bucket_count if self.bucket_count else 0.0

    def get(self, key: Any) -> List[int]:
        """Mengembalikan seluruh posisi (indeks) di mana `key` muncul."""
        return self.table.get(key, [])

    def contains(self, key: Any) -> bool:
        return key in self.table


@dataclass
class InvertedIndex:
    """
    Inverted index generik: memetakan nilai/token -> list ID record
    yang mengandung nilai tersebut. Berguna untuk dataset terstruktur
    (list of dict) dengan beberapa field yang bisa dicari.
    """

    index: Dict[str, Dict[Any, List[int]]] = field(default_factory=dict)


def build_hash_index(data: Sequence[Any], initial_buckets: int = 16) -> HashIndex:
    """
    Membangun HashIndex dari sequence data mentah (list nilai tunggal).
    Setiap nilai dipetakan ke seluruh posisi kemunculannya di `data`.
    """
    # Buckets disesuaikan agar load factor awal tidak melebihi 0.75
    # sesuai IndexConfig.hash_max_load_factor di config/settings.py.
    bucket_count = max(initial_buckets, int(len(data) / 0.75) or initial_buckets)

    hash_index = HashIndex(bucket_count=bucket_count)
    for position, value in enumerate(data):
        hash_index.table[value].append(position)
        hash_index.total_keys_inserted += 1

    return hash_index


def build_inverted_index(
    records: Sequence[Dict[str, Any]], fields: List[str]
) -> InvertedIndex:
    """
    Membangun inverted index dari list of dict (dataset terstruktur),
    untuk field-field yang ditentukan pada
    IndexConfig.default_search_fields.

    Struktur hasil: index[field][value] = [id_record, ...]
    """
    inverted = InvertedIndex()
    for field_name in fields:
        inverted.index[field_name] = defaultdict(list)

    for record_id, record in enumerate(records):
        for field_name in fields:
            if field_name in record:
                value = record[field_name]
                inverted.index[field_name][value].append(record_id)

    return inverted


def validate_index_integrity(hash_index: HashIndex, original_data: Sequence[Any]) -> bool:
    """
    Memverifikasi bahwa setiap posisi yang tercatat pada HashIndex
    benar-benar menunjuk ke nilai yang sesuai pada data asli.
    Digunakan oleh tests/test_index_integrity.py.
    """
    for key, positions in hash_index.table.items():
        for pos in positions:
            if pos >= len(original_data) or original_data[pos] != key:
                return False
    return True
