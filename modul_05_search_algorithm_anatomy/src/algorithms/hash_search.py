"""
hash_search.py
Implementasi Direct Key Lookup O(1) rata-rata, memanfaatkan struktur
HashIndex yang dibangun oleh src/indexer/index_builder.py.
"""

from typing import Any, Optional, Sequence

from src.algorithms.linear_search import SearchResult
from src.analytics.search_space_tracker import PointerSnapshot
from src.indexer.index_builder import HashIndex, build_hash_index


def hash_search(
    data: Sequence[Any], target: Any, prebuilt_index: Optional[HashIndex] = None
) -> SearchResult:
    """
    Direct Key Lookup: mencari `target` melalui HashIndex.

    Jika `prebuilt_index` tidak diberikan, indeks akan dibangun on-the-fly
    dari `data` (biaya O(N) satu kali, tetapi lookup berikutnya O(1)).
    Untuk penggunaan berulang pada dataset yang sama, sebaiknya bangun
    indeks sekali di awal via build_hash_index() dan gunakan kembali.
    """
    comparisons = 0
    trace = []

    hash_index = prebuilt_index if prebuilt_index is not None else build_hash_index(data)

    # Lookup pada hash map dianggap 1 "operasi perbandingan efektif"
    # (perbandingan hash key), sesuai definisi step_counter.py untuk
    # algoritma O(1).
    comparisons += 1
    positions = hash_index.get(target)

    if positions:
        first_pos = positions[0]
        trace.append(PointerSnapshot(step=comparisons, pos=first_pos, note="hash hit"))
        return SearchResult(
            found=True,
            index=first_pos,
            comparisons=comparisons,
            algorithm="hash",
            trace=trace,
        )

    trace.append(PointerSnapshot(step=comparisons, pos=-1, note="hash miss"))
    return SearchResult(
        found=False,
        index=-1,
        comparisons=comparisons,
        algorithm="hash",
        trace=trace,
    )
