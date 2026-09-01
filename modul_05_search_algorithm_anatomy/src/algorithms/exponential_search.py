"""
exponential_search.py
Implementasi Exponential Search (Unbounded Search), O(log N).
Berguna ketika ukuran data besar/tidak diketahui atau target
diperkirakan berada di posisi awal array.

Prasyarat: `data` harus sudah terurut ascending.
"""

from typing import Sequence

from src.algorithms.linear_search import SearchResult
from src.analytics.search_space_tracker import PointerSnapshot


def exponential_search(data: Sequence[float], target: float) -> SearchResult:
    """
    Fase 1 (eksponensial): melipatgandakan bound (1, 2, 4, 8, ...)
    hingga data[bound] >= target atau bound melampaui panjang data.

    Fase 2 (binary search): menjalankan binary search klasik pada
    rentang [bound // 2, min(bound, len(data) - 1)].
    """
    n = len(data)
    comparisons = 0
    trace = []

    if n == 0:
        return SearchResult(found=False, index=-1, comparisons=0, algorithm="exponential", trace=[])

    if data[0] == target:
        comparisons += 1
        trace.append(PointerSnapshot(step=comparisons, bound=0, pos=0, note="match di index 0"))
        return SearchResult(
            found=True, index=0, comparisons=comparisons, algorithm="exponential", trace=trace
        )

    bound = 1
    while bound < n:
        comparisons += 1
        trace.append(PointerSnapshot(step=comparisons, bound=bound, note="fase eksponensial"))
        if data[bound] >= target:
            break
        bound *= 2

    left = bound // 2
    right = min(bound, n - 1)

    # Fase 2: Binary Search klasik pada rentang yang ditemukan.
    while left <= right:
        mid = (left + right) // 2
        comparisons += 1
        trace.append(PointerSnapshot(step=comparisons, left=left, right=right, pos=mid, note="fase binary"))

        if data[mid] == target:
            return SearchResult(
                found=True,
                index=mid,
                comparisons=comparisons,
                algorithm="exponential",
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
        algorithm="exponential",
        trace=trace,
    )
