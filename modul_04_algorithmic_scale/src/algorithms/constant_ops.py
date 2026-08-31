"""
constant_ops.py
Contoh algoritma dengan kompleksitas O(1) — waktu eksekusi konstan,
tidak bergantung pada ukuran input N.
"""

from typing import List, Any


def get_first_element(data: List[Any]) -> Any:
    """Mengambil elemen pertama list. O(1)."""
    if not data:
        raise IndexError("Data kosong")
    return data[0]


def get_element_at_index(data: List[Any], index: int) -> Any:
    """Mengambil elemen pada index tertentu. O(1)."""
    return data[index]


def is_empty(data: List[Any]) -> bool:
    """Mengecek apakah list kosong. O(1)."""
    return len(data) == 0


def swap_first_last(data: List[Any]) -> List[Any]:
    """Menukar elemen pertama dan terakhir. O(1) — tidak bergantung pada N."""
    if len(data) < 2:
        return data
    data[0], data[-1] = data[-1], data[0]
    return data


def peek_hashmap_value(mapping: dict, key: Any) -> Any:
    """Mengambil nilai dari dictionary berdasarkan key. Rata-rata O(1)."""
    return mapping.get(key)
