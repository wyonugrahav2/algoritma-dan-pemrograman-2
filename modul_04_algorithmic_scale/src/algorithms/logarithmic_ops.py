"""
logarithmic_ops.py
Contoh algoritma dengan kompleksitas O(log N) — waktu eksekusi
bertambah sangat lambat seiring pertumbuhan N, karena tiap langkah
memangkas ruang pencarian menjadi separuhnya.
"""

from typing import List, Optional


def binary_search(sorted_data: List[int], target: int) -> Optional[int]:
    """
    Mencari index target dalam data yang SUDAH TERURUT menggunakan
    binary search. O(log N). Mengembalikan None jika tidak ditemukan.
    """
    low, high = 0, len(sorted_data) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_data[mid] == target:
            return mid
        elif sorted_data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return None


def count_digits(n: int) -> int:
    """Menghitung banyaknya digit sebuah bilangan. O(log N)."""
    if n == 0:
        return 1
    n = abs(n)
    count = 0
    while n > 0:
        n //= 10
        count += 1
    return count


def binary_search_insert_position(sorted_data: List[int], value: int) -> int:
    """
    Mencari posisi yang tepat untuk menyisipkan `value` agar list
    tetap terurut, tanpa benar-benar menyisipkannya. O(log N).
    """
    low, high = 0, len(sorted_data)
    while low < high:
        mid = (low + high) // 2
        if sorted_data[mid] < value:
            low = mid + 1
        else:
            high = mid
    return low
