"""
sorter_component.py
Mengemas modul pengurutan (konsep dari Modul 06 - Basic Sorting Blueprints)
ke dalam antarmuka komponen yang seragam agar bisa dipasang langsung ke
dalam rantai pemrosesan pipeline.

Implementasi algoritma disertakan langsung di sini (versi ringkas) supaya
proyek Modul 07 tetap independen dan bisa langsung dijalankan.
"""

from typing import Any, List


def _quick_sort(arr: List[Any]) -> List[Any]:
    if len(arr) <= 1:
        return arr[:]
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return _quick_sort(left) + mid + _quick_sort(right)


def _merge_sort(arr: List[Any]) -> List[Any]:
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = _merge_sort(arr[:mid])
    right = _merge_sort(arr[mid:])
    result: List[Any] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


_STRATEGIES = {
    "quick": _quick_sort,
    "merge": _merge_sort,
}


class SorterComponent:
    """Wrapper stage untuk mengurutkan payload dengan strategi terpilih."""

    name = "sorter_component"

    def __init__(self, strategy: str = "quick"):
        if strategy not in _STRATEGIES:
            raise ValueError(
                f"Strategi sorting '{strategy}' tidak dikenal. "
                f"Pilihan: {list(_STRATEGIES)}"
            )
        self.strategy = strategy
        self._fn = _STRATEGIES[strategy]

    def run(self, context):
        data: List[Any] = list(context.payload)
        sorted_data = self._fn(data)
        message = f"Diurutkan dengan strategi '{self.strategy}' ({len(sorted_data)} elemen)"
        new_context = context.with_payload(sorted_data)
        return new_context, message


def quick_sort_stage(context):
    return SorterComponent("quick").run(context)


def merge_sort_stage(context):
    return SorterComponent("merge").run(context)
