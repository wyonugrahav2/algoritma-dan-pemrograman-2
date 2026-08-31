"""
generators.py
Generator data sintetis (angka & string) berskala besar, terisolasi
dari logika algoritma target agar pengukuran waktu/memori murni
mencerminkan performa algoritma, bukan proses pembuatan datanya.
"""

import random
import string
from typing import List

from config.settings import Settings


def _seeded_random(seed: int = None) -> random.Random:
    """Membuat instance Random terpisah agar tidak mengganggu state global."""
    rng = random.Random()
    rng.seed(seed if seed is not None else Settings.RANDOM_SEED)
    return rng


def generate_random_integers(n: int, low: int = 0, high: int = 10_000_000, seed: int = None) -> List[int]:
    """Menghasilkan list berisi n bilangan bulat acak dalam rentang [low, high]."""
    if n < 0:
        raise ValueError("n tidak boleh negatif")
    rng = _seeded_random(seed)
    return [rng.randint(low, high) for _ in range(n)]


def generate_sorted_integers(n: int, step: int = 1) -> List[int]:
    """Menghasilkan list bilangan bulat yang sudah terurut naik (best case)."""
    if n < 0:
        raise ValueError("n tidak boleh negatif")
    return [i * step for i in range(n)]


def generate_reversed_integers(n: int, step: int = 1) -> List[int]:
    """Menghasilkan list bilangan bulat terurut turun (worst case untuk banyak sorting)."""
    if n < 0:
        raise ValueError("n tidak boleh negatif")
    return [i * step for i in range(n - 1, -1, -1)]


def generate_random_string(length: int, seed: int = None) -> str:
    """Menghasilkan satu string acak sepanjang `length` karakter alfanumerik."""
    if length < 0:
        raise ValueError("length tidak boleh negatif")
    rng = _seeded_random(seed)
    alphabet = string.ascii_letters + string.digits
    return "".join(rng.choice(alphabet) for _ in range(length))


def generate_random_string_list(n: int, string_length: int = 10, seed: int = None) -> List[str]:
    """Menghasilkan n buah string acak, masing-masing sepanjang `string_length`."""
    if n < 0:
        raise ValueError("n tidak boleh negatif")
    rng = _seeded_random(seed)
    alphabet = string.ascii_letters + string.digits
    return [
        "".join(rng.choice(alphabet) for _ in range(string_length))
        for _ in range(n)
    ]


def generate_key_value_pairs(n: int, seed: int = None) -> dict:
    """Menghasilkan dictionary berisi n pasangan key-value acak (untuk uji hashmap)."""
    if n < 0:
        raise ValueError("n tidak boleh negatif")
    rng = _seeded_random(seed)
    alphabet = string.ascii_letters + string.digits
    pairs = {}
    for i in range(n):
        key = f"key_{i}_" + "".join(rng.choice(alphabet) for _ in range(6))
        pairs[key] = rng.randint(0, 1_000_000)
    return pairs
