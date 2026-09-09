"""
array_factory.py
-----------------
Generator untuk membuat sampel array dengan berbagai variasi kondisi awal:
Random (acak), Nearly Sorted (hampir terurut), dan Reversed (terbalik total).

Ketiga kondisi ini penting untuk menguji sifat "Adaptive" suatu algoritma
(contoh: Insertion Sort jauh lebih cepat pada data Nearly Sorted).
"""

import random

from config.settings import RANDOM_VALUE_MIN, RANDOM_VALUE_MAX


def generate_random_array(size: int) -> list[int]:
    """Menghasilkan array dengan urutan acak sepenuhnya (Average Case)."""
    return [random.randint(RANDOM_VALUE_MIN, RANDOM_VALUE_MAX) for _ in range(size)]


def generate_nearly_sorted_array(size: int, swap_fraction: float = 0.05) -> list[int]:
    """
    Menghasilkan array yang hampir terurut (Best Case untuk algoritma adaptive).
    swap_fraction menentukan proporsi elemen yang ditukar posisinya secara acak
    dari kondisi terurut sempurna.
    """
    arr = list(range(1, size + 1))
    num_swaps = max(1, int(size * swap_fraction)) if size > 1 else 0
    for _ in range(num_swaps):
        i, j = random.randint(0, size - 1), random.randint(0, size - 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def generate_reversed_array(size: int) -> list[int]:
    """Menghasilkan array terbalik total (Worst Case untuk banyak algoritma)."""
    return list(range(size, 0, -1))


def generate_array(size: int, case: str = "random") -> list[int]:
    """
    Factory utama: pilih kondisi data lewat parameter `case`.
    case ∈ {"random", "nearly_sorted", "reversed"}
    """
    case = case.strip().lower()
    if case == "random":
        return generate_random_array(size)
    if case == "nearly_sorted":
        return generate_nearly_sorted_array(size)
    if case == "reversed":
        return generate_reversed_array(size)
    raise ValueError(
        f"Case '{case}' tidak dikenali. Pilihan valid: random, nearly_sorted, reversed"
    )
