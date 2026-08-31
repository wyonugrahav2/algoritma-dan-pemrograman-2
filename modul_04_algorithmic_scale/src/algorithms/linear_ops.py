"""
linear_ops.py
Contoh algoritma dengan kompleksitas O(N) — waktu eksekusi bertambah
secara proporsional (linear) dengan ukuran input N.
"""

from typing import List, Optional


def linear_search(data: List[int], target: int) -> Optional[int]:
    """Mencari index target dengan menelusuri seluruh elemen satu per satu. O(N)."""
    for i, value in enumerate(data):
        if value == target:
            return i
    return None


def find_max(data: List[int]) -> int:
    """Mencari nilai maksimum dalam list. O(N)."""
    if not data:
        raise ValueError("Data kosong")
    max_value = data[0]
    for value in data[1:]:
        if value > max_value:
            max_value = value
    return max_value


def sum_all(data: List[int]) -> int:
    """Menjumlahkan seluruh elemen list. O(N)."""
    total = 0
    for value in data:
        total += value
    return total


def count_occurrences(data: List[int], target: int) -> int:
    """Menghitung berapa kali `target` muncul dalam list. O(N)."""
    count = 0
    for value in data:
        if value == target:
            count += 1
    return count


def reverse_list(data: List[int]) -> List[int]:
    """Membalik urutan list secara manual (tanpa slicing bawaan). O(N)."""
    result = []
    for i in range(len(data) - 1, -1, -1):
        result.append(data[i])
    return result
