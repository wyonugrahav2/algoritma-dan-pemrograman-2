"""
set_operations.py
Eksekutor operasi himpunan (Intersection, Union, Difference,
Symmetric Difference) berukuran masif secara efisien, memanfaatkan
implementasi Set native Python yang sudah dioptimasi di level C.
"""

from __future__ import annotations
from typing import Hashable, Iterable, Set


def to_set(items: Iterable[Hashable]) -> Set[Hashable]:
    return set(items)


def intersection(a: Iterable[Hashable], b: Iterable[Hashable]) -> Set[Hashable]:
    """Elemen yang ada di kedua himpunan. O(min(len(a), len(b)))."""
    return to_set(a) & to_set(b)


def union(a: Iterable[Hashable], b: Iterable[Hashable]) -> Set[Hashable]:
    """Gabungan seluruh elemen unik dari kedua himpunan."""
    return to_set(a) | to_set(b)


def difference(a: Iterable[Hashable], b: Iterable[Hashable]) -> Set[Hashable]:
    """Elemen yang ada di a tapi tidak ada di b."""
    return to_set(a) - to_set(b)


def symmetric_difference(a: Iterable[Hashable], b: Iterable[Hashable]) -> Set[Hashable]:
    """Elemen yang hanya ada di salah satu himpunan, tapi tidak di keduanya."""
    return to_set(a) ^ to_set(b)


def is_subset(a: Iterable[Hashable], b: Iterable[Hashable]) -> bool:
    return to_set(a) <= to_set(b)


def jaccard_similarity(a: Iterable[Hashable], b: Iterable[Hashable]) -> float:
    """Ukuran kemiripan dua himpunan: |A ∩ B| / |A ∪ B|."""
    set_a, set_b = to_set(a), to_set(b)
    union_size = len(set_a | set_b)
    if union_size == 0:
        return 1.0
    return len(set_a & set_b) / union_size


if __name__ == "__main__":
    group_a = ["alice", "bob", "carol", "dave"]
    group_b = ["carol", "dave", "eve"]

    print("Union       :", union(group_a, group_b))
    print("Intersection:", intersection(group_a, group_b))
    print("Difference  :", difference(group_a, group_b))
    print("Sym. Diff   :", symmetric_difference(group_a, group_b))
    print("Jaccard sim :", f"{jaccard_similarity(group_a, group_b):.2f}")
