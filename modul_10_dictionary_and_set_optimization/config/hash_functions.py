"""
hash_functions.py
Pilihan algoritma hashing (Murmur3 sederhana, SHA-256, FNV-1a) yang bisa
dipasang-lepas (pluggable) ke dalam Custom Hash Table.
"""

import hashlib
from typing import Callable, Dict


def fnv1a_hash(key: str) -> int:
    """Implementasi FNV-1a: cepat, non-cryptographic, cocok untuk hash table."""
    FNV_OFFSET_BASIS = 0x811C9DC5
    FNV_PRIME = 0x01000193
    h = FNV_OFFSET_BASIS
    for byte in key.encode("utf-8"):
        h ^= byte
        h = (h * FNV_PRIME) & 0xFFFFFFFF
    return h


def murmur3_like_hash(key: str, seed: int = 0) -> int:
    """
    Implementasi ringan bergaya Murmur3 (bukan implementasi resmi, tapi
    memenuhi properti distribusi yang baik untuk keperluan pembelajaran).
    """
    data = key.encode("utf-8")
    m = 0x5BD1E995
    h = seed ^ len(data)
    for i in range(0, len(data) - 3, 4):
        k = int.from_bytes(data[i:i + 4], "little")
        k = (k * m) & 0xFFFFFFFF
        k ^= k >> 24
        k = (k * m) & 0xFFFFFFFF
        h = (h * m) & 0xFFFFFFFF
        h ^= k
    tail = data[len(data) - (len(data) % 4):]
    for byte in reversed(tail):
        h = (h ^ byte) & 0xFFFFFFFF
        h = (h * m) & 0xFFFFFFFF
    h ^= h >> 13
    h = (h * m) & 0xFFFFFFFF
    h ^= h >> 15
    return h & 0xFFFFFFFF


def sha256_hash(key: str) -> int:
    """Hash kriptografis SHA-256, dipotong menjadi integer 32-bit."""
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


# Registry fungsi hash yang bisa dipilih lewat settings.py
HASH_FUNCTIONS: Dict[str, Callable[[str], int]] = {
    "fnv1a": fnv1a_hash,
    "murmur3": murmur3_like_hash,
    "sha256": sha256_hash,
}


def get_hash_function(name: str = "fnv1a") -> Callable[[str], int]:
    try:
        return HASH_FUNCTIONS[name]
    except KeyError as exc:
        raise ValueError(
            f"Fungsi hash '{name}' tidak dikenal. Pilihan: {list(HASH_FUNCTIONS)}"
        ) from exc
