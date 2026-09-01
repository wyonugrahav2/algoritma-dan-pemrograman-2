"""
binary_search.py
Implementasi Binary Search (Divide & Conquer) O(log N).
Mensyaratkan data terurut (lihat src/indexer/sorter.py).
"""

from typing import Sequence

from src.algorithms.linear_search import SearchResult
from src.analytics.search_space_tracker import PointerSnapshot


def binary_search(data: Sequence[float], target: float) -> SearchResult:
    """
    Binary Search klasik: memotong ruang pencarian menjadi setengah
    pada setiap iterasi dengan membandingkan target terhadap elemen
    tengah (mid).

    Prasyarat: `data` harus sudah terurut ascending.
    """
    left, right = 0, len(data) - 1
    comparisons = 0
    trace = []

    while left <= right:
        mid = (left + right) // 2
        comparisons += 1
        trace.append(
            PointerSnapshot(step=comparisons, left=left, right=right, pos=mid)
        )

        if data[mid] == target:
            return SearchResult(
                found=True,
                index=mid,
                comparisons=comparisons,
                algorithm="binary",
                trace=trace,
            )
        elif data[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return SearchResult(
        found=False,
        index=-1,
        comparisons=comparisons,
        algorithm="binary",
        trace=trace,
    )
