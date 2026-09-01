"""
linear_search.py
Implementasi Sequential Search O(N).

Setiap algoritma pencarian pada modul ini mengembalikan objek
`SearchResult` yang seragam, agar bisa dikonsumsi secara konsisten
oleh src/analytics/ dan src/ui/result_presenter.py.
"""

from dataclasses import dataclass, field
from typing import Any, List, Sequence

from src.analytics.search_space_tracker import PointerSnapshot


@dataclass
class SearchResult:
    """Hasil generik dari eksekusi algoritma pencarian apa pun."""

    found: bool
    index: int  # -1 jika tidak ditemukan
    comparisons: int
    algorithm: str
    trace: List[PointerSnapshot] = field(default_factory=list)


def linear_search(data: Sequence[Any], target: Any) -> SearchResult:
    """
    Sequential Search: memeriksa elemen satu per satu dari kiri ke kanan.
    Tidak mensyaratkan data terurut. Kompleksitas O(N) kasus terburuk,
    O(N/2) rata-rata saat target ditemukan.
    """
    comparisons = 0
    trace: List[PointerSnapshot] = []

    for i, value in enumerate(data):
        comparisons += 1
        trace.append(PointerSnapshot(step=comparisons, left=0, right=len(data) - 1, pos=i))

        if value == target:
            return SearchResult(
                found=True,
                index=i,
                comparisons=comparisons,
                algorithm="linear",
                trace=trace,
            )

    return SearchResult(
        found=False,
        index=-1,
        comparisons=comparisons,
        algorithm="linear",
        trace=trace,
    )
