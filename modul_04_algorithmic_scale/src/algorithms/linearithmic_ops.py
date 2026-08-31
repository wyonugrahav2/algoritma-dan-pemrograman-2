"""
linearithmic_ops.py
Contoh algoritma dengan kompleksitas O(N log N) — umum dijumpai pada
algoritma sorting berbasis divide-and-conquer seperti merge sort.
"""

from typing import List


def merge_sort(data: List[int]) -> List[int]:
    """Mengurutkan list menggunakan merge sort. O(N log N) di semua kasus."""
    if len(data) <= 1:
        return data[:]

    mid = len(data) // 2
    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])

    return _merge(left, right)


def _merge(left: List[int], right: List[int]) -> List[int]:
    """Menggabungkan dua list terurut menjadi satu list terurut. O(N)."""
    result = []
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


def heap_sort(data: List[int]) -> List[int]:
    """Mengurutkan list menggunakan heap sort. O(N log N)."""
    import heapq
    heap = data[:]
    heapq.heapify(heap)
    return [heapq.heappop(heap) for _ in range(len(heap))]


def count_inversions(data: List[int]) -> int:
    """
    Menghitung jumlah inversi (pasangan elemen yang tidak terurut)
    menggunakan modifikasi merge sort. O(N log N).
    """
    def sort_and_count(arr: List[int]):
        if len(arr) <= 1:
            return arr, 0
        mid = len(arr) // 2
        left, inv_left = sort_and_count(arr[:mid])
        right, inv_right = sort_and_count(arr[mid:])
        merged = []
        i = j = inv_split = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
                inv_split += len(left) - i
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, inv_left + inv_right + inv_split

    _, total_inversions = sort_and_count(data)
    return total_inversions
