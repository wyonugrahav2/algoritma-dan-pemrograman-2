"""
searcher_component.py
Mengemas modul pencarian (konsep dari Modul 05 - Search Algorithm Anatomy)
ke dalam antarmuka komponen yang seragam.

Target pencarian diambil dari context.metadata["search_target"], sehingga
pipeline bisa fleksibel: hasil pencarian tidak mengubah payload (array
tetap dipertahankan) melainkan disimpan di context.metadata["search_result"].
"""

from typing import Any, List, Optional


def _binary_search(arr: List[Any], target: Any) -> Optional[int]:
    """Mengasumsikan arr sudah terurut menaik (prasyarat pipeline)."""
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return None


class SearcherComponent:
    """Wrapper stage untuk mencari sebuah nilai target di dalam payload."""

    name = "searcher_component"

    def __init__(self, strategy: str = "binary"):
        if strategy != "binary":
            raise ValueError("Saat ini hanya strategi 'binary' yang didukung.")
        self.strategy = strategy

    def run(self, context):
        target = context.metadata.get("search_target")
        if target is None:
            message = "Tidak ada 'search_target' di metadata, stage dilewati."
            return context, message

        data: List[Any] = list(context.payload)
        index = _binary_search(data, target)

        context.metadata["search_result"] = index
        found = index is not None
        message = (
            f"Target {target!r} ditemukan di indeks {index}"
            if found
            else f"Target {target!r} tidak ditemukan"
        )
        return context, message


def binary_search_stage(context):
    return SearcherComponent("binary").run(context)
