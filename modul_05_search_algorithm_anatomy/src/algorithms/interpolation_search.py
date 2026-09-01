"""
interpolation_search.py
Implementasi Interpolation Search, rata-rata O(log log N) pada data
yang terdistribusi uniform. Mensyaratkan data terurut dan numerik.
"""

from typing import Sequence

from src.algorithms.linear_search import SearchResult
from src.analytics.search_space_tracker import PointerSnapshot


def interpolation_search(data: Sequence[float], target: float) -> SearchResult:
    """
    Interpolation Search: mengestimasi posisi target berdasarkan
    proporsi nilainya relatif terhadap rentang [data[left], data[right]],
    bukan sekadar mengambil titik tengah seperti Binary Search.

    Formula estimasi posisi:
        pos = left + ((target - data[left]) * (right - left))
                     // (data[right] - data[left])

    Prasyarat: `data` harus sudah terurut ascending dan bertipe numerik.
    Lihat docs/data_distribution_impact.md untuk analisis performa pada
    distribusi non-uniform.
    """
    left, right = 0, len(data) - 1
    comparisons = 0
    trace = []

    while left <= right and data[left] <= target <= data[right]:
        comparisons += 1

        if data[left] == data[right]:
            # Semua elemen dalam rentang bernilai sama; periksa langsung.
            pos = left
        else:
            pos = left + int(
                ((target - data[left]) * (right - left)) / (data[right] - data[left])
            )
            # Klem posisi agar tetap valid di dalam rentang [left, right],
            # menjaga dari estimasi yang meleset akibat distribusi skewed.
            pos = max(left, min(right, pos))

        trace.append(PointerSnapshot(step=comparisons, left=left, right=right, pos=pos))

        if data[pos] == target:
            return SearchResult(
                found=True,
                index=pos,
                comparisons=comparisons,
                algorithm="interpolation",
                trace=trace,
            )
        elif data[pos] < target:
            left = pos + 1
        else:
            right = pos - 1

    return SearchResult(
        found=False,
        index=-1,
        comparisons=comparisons,
        algorithm="interpolation",
        trace=trace,
    )
