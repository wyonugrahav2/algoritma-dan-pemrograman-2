"""
test_sorting_correctness.py
------------------------------
Memastikan data benar-benar terurut (Ascending) untuk semua algoritma
yang terdaftar di SORT_STRATEGIES, menggunakan sorted() bawaan Python
sebagai oracle pembanding.
"""

import random
import pytest

from config.sort_strategies import SORT_STRATEGIES


@pytest.mark.parametrize("name,strategy", SORT_STRATEGIES.items())
def test_random_arrays_are_sorted_correctly(name, strategy):
    random.seed(42)
    for _ in range(10):
        size = random.randint(0, 50)
        arr = [random.randint(-100, 100) for _ in range(size)]
        expected = sorted(arr)

        result = strategy["function"](arr)

        assert result == expected, f"{name} gagal mengurutkan: {arr}"


@pytest.mark.parametrize("name,strategy", SORT_STRATEGIES.items())
def test_does_not_mutate_original_array(name, strategy):
    """Algoritma harus mengembalikan array baru, bukan memutasi input asli."""
    original = [5, 3, 1, 4, 2]
    original_copy = list(original)

    strategy["function"](original)

    assert original == original_copy, f"{name} memutasi array input asli"
