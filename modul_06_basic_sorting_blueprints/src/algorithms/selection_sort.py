"""
selection_sort.py
-------------------
Implementasi Selection Sort: pendekatan "Minimum Finding & Swap".

Ide dasar: pada setiap iterasi, cari elemen terkecil dari bagian array
yang belum terurut, lalu tukar dengan elemen pertama di bagian tersebut.

Kompleksitas waktu : O(N^2) pada semua kasus (best/average/worst sama saja,
                      karena selalu melakukan pencarian minimum penuh).
Kompleksitas ruang  : O(1) — in-place.
Stability           : Tidak stable (swap jarak jauh bisa melompati elemen
                      lain yang bernilai sama).
Keunggulan          : Jumlah swap minimal, yaitu tepat O(N) — berguna saat
                      biaya operasi tulis/swap jauh lebih mahal dari
                      biaya pembacaan/perbandingan.
"""


def selection_sort(
    array: list[int],
    swap_counter=None,
    compare_counter=None,
    snapshot=None,
) -> list[int]:
    """Mengurutkan array secara ascending menggunakan Selection Sort."""
    arr = list(array)
    n = len(arr)

    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if compare_counter:
                compare_counter.record()
            if arr[j] < arr[min_idx]:
                min_idx = j

        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            if swap_counter:
                swap_counter.record()
            if snapshot:
                snapshot.capture(arr, highlight=(i, min_idx))

    return arr
