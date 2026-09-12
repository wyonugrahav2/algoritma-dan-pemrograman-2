"""
deduplicator.py
Pembersih data duplikat berkecepatan tinggi memanfaatkan sifat unik Set,
sekaligus mendukung mode "hemat memori" via Bloom Filter untuk dataset
sangat besar di mana sedikit false-positive dapat diterima.
"""

from __future__ import annotations
from typing import Hashable, Iterable, List

from src.custom_structures.bloom_filter import BloomFilter


def deduplicate_exact(items: Iterable[Hashable]) -> List[Hashable]:
    """
    Deduplikasi 100% akurat menggunakan set, sambil menjaga urutan asli
    kemunculan pertama tiap elemen (stable dedup).
    """
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def deduplicate_approximate(
    items: Iterable[str],
    expected_items: int = 100_000,
    false_positive_rate: float = 0.01,
) -> List[str]:
    """
    Deduplikasi hemat memori menggunakan Bloom Filter. Karena Bloom Filter
    bisa menghasilkan false positive, sebagian kecil item unik (yang
    seharusnya lolos) mungkin ikut terbuang -- trade-off yang disengaja
    demi efisiensi memori pada skala data masif.
    """
    bloom = BloomFilter(expected_items=expected_items, false_positive_rate=false_positive_rate)
    result = []
    for item in items:
        if not bloom.might_contain(item):
            bloom.add(item)
            result.append(item)
    return result


def duplicate_ratio(items: Iterable[Hashable]) -> float:
    """Menghitung proporsi elemen yang merupakan duplikat dari total."""
    items = list(items)
    if not items:
        return 0.0
    unique_count = len(set(items))
    return 1 - (unique_count / len(items))


if __name__ == "__main__":
    sample = ["a", "b", "a", "c", "b", "b", "d"]
    print("Original       :", sample)
    print("Deduplicated    :", deduplicate_exact(sample))
    print("Duplicate ratio :", f"{duplicate_ratio(sample):.2%}")
