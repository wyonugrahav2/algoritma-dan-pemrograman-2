"""
quick_sort.py
-------------
Implementasi Quick Sort: pendekatan "Pivot-based Partitioning" (Lomuto scheme).

Ide dasar: pilih satu elemen sebagai pivot, lalu partisi array sehingga
semua elemen lebih kecil dari pivot berada di kiri, dan elemen lebih besar
di kanan. Rekursi diterapkan pada kedua sisi partisi.

Kompleksitas waktu : O(N log N) average case, O(N^2) worst case (jika pivot
                      selalu menjadi elemen terkecil/terbesar, misalnya pada
                      array yang sudah terurut dengan pivot = elemen terakhir).
Kompleksitas ruang  : O(log N) average (kedalaman rekursi call stack),
                      bisa O(N) pada worst case.
Stability           : Tidak stable (swap dalam partisi bisa mengubah urutan
                      relatif elemen bernilai sama).
"""


def quick_sort(
    array: list[int],
    swap_counter=None,
    compare_counter=None,
    snapshot=None,
) -> list[int]:
    """Mengurutkan array secara ascending menggunakan Quick Sort (in-place)."""
    arr = list(array)
    _quick_sort_recursive(arr, 0, len(arr) - 1, swap_counter, compare_counter, snapshot)
    return arr


def _quick_sort_recursive(arr, low, high, swap_counter, compare_counter, snapshot):
    if low < high:
        pivot_index = _partition(arr, low, high, swap_counter, compare_counter, snapshot)
        _quick_sort_recursive(arr, low, pivot_index - 1, swap_counter, compare_counter, snapshot)
        _quick_sort_recursive(arr, pivot_index + 1, high, swap_counter, compare_counter, snapshot)


def _partition(arr, low, high, swap_counter, compare_counter, snapshot) -> int:
    """Partisi Lomuto: pivot = elemen paling akhir dari rentang [low, high]."""
    pivot = arr[high]
    i = low - 1  # batas elemen yang lebih kecil dari pivot

    for j in range(low, high):
        if compare_counter:
            compare_counter.record()
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            if swap_counter:
                swap_counter.record()
            if snapshot:
                snapshot.capture(arr, highlight=(i, j))

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    if swap_counter:
        swap_counter.record()
    if snapshot:
        snapshot.capture(arr, highlight=(i + 1, high))

    return i + 1
