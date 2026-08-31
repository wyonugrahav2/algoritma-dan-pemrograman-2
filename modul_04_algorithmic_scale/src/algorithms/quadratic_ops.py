"""
quadratic_ops.py
Contoh algoritma dengan kompleksitas O(N^2) — waktu eksekusi bertambah
dengan kuadrat N, umumnya karena penggunaan nested loop.
"""

from typing import List


def bubble_sort(data: List[int]) -> List[int]:
    """Mengurutkan list menggunakan bubble sort klasik. O(N^2)."""
    arr = data[:]
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def selection_sort(data: List[int]) -> List[int]:
    """Mengurutkan list menggunakan selection sort. O(N^2)."""
    arr = data[:]
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def find_duplicate_pairs(data: List[int]) -> List[tuple]:
    """
    Mencari seluruh pasangan index (i, j) dengan nilai yang sama
    menggunakan nested loop naif. O(N^2).
    """
    pairs = []
    n = len(data)
    for i in range(n):
        for j in range(i + 1, n):
            if data[i] == data[j]:
                pairs.append((i, j))
    return pairs


def has_duplicate_naive(data: List[int]) -> bool:
    """Mengecek adanya duplikat dengan membandingkan tiap pasangan elemen. O(N^2)."""
    n = len(data)
    for i in range(n):
        for j in range(i + 1, n):
            if data[i] == data[j]:
                return True
    return False
