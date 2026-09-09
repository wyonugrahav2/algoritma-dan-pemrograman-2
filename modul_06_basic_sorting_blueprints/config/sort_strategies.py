"""
sort_strategies.py
-------------------
Registrasi algoritma pengurutan menggunakan Strategy Pattern.
Menambahkan algoritma baru cukup dilakukan di sini, tanpa mengubah kode
yang memanggilnya (Open/Closed Principle).
"""

from src.algorithms.bubble_sort import bubble_sort
from src.algorithms.selection_sort import selection_sort
from src.algorithms.insertion_sort import insertion_sort
from src.algorithms.merge_sort import merge_sort
from src.algorithms.quick_sort import quick_sort


SORT_STRATEGIES = {
    "bubble": {
        "function": bubble_sort,
        "label": "Bubble Sort",
        "complexity_time": "O(N^2)",
        "complexity_space": "O(1)",
        "stable": True,
        "in_place": True,
    },
    "selection": {
        "function": selection_sort,
        "label": "Selection Sort",
        "complexity_time": "O(N^2)",
        "complexity_space": "O(1)",
        "stable": False,
        "in_place": True,
    },
    "insertion": {
        "function": insertion_sort,
        "label": "Insertion Sort",
        "complexity_time": "O(N^2)",
        "complexity_space": "O(1)",
        "stable": True,
        "in_place": True,
    },
    "merge": {
        "function": merge_sort,
        "label": "Merge Sort",
        "complexity_time": "O(N log N)",
        "complexity_space": "O(N)",
        "stable": True,
        "in_place": False,
    },
    "quick": {
        "function": quick_sort,
        "label": "Quick Sort",
        "complexity_time": "O(N log N) avg / O(N^2) worst",
        "complexity_space": "O(log N)",
        "stable": False,
        "in_place": True,
    },
}


def get_strategy(name: str):
    """Mengambil metadata + fungsi strategi sorting berdasarkan nama."""
    key = name.strip().lower()
    if key not in SORT_STRATEGIES:
        valid = ", ".join(SORT_STRATEGIES.keys())
        raise ValueError(f"Strategi '{name}' tidak dikenali. Pilihan valid: {valid}")
    return SORT_STRATEGIES[key]


def list_strategies():
    """Mengembalikan daftar nama strategi yang terdaftar."""
    return list(SORT_STRATEGIES.keys())
