"""
insertion_sort.py
-------------------
Implementasi Insertion Sort: pendekatan "Adaptive Shift & Insert".

Ide dasar: bangun bagian array yang terurut sedikit demi sedikit dari kiri.
Setiap elemen baru "disisipkan" ke posisi yang tepat di dalam bagian yang
sudah terurut, dengan menggeser elemen-elemen yang lebih besar ke kanan.

Kompleksitas waktu : O(N^2) worst/average, O(N) best case (data sudah
                      terurut/hampir terurut) — bersifat ADAPTIVE.
Kompleksitas ruang  : O(1) — in-place.
Stability           : Stable (pergeseran hanya untuk elemen yang > key,
                      elemen sama nilai tidak dilewati).
"""


def insertion_sort(
    array: list[int],
    swap_counter=None,
    compare_counter=None,
    snapshot=None,
) -> list[int]:
    """Mengurutkan array secara ascending menggunakan Insertion Sort."""
    arr = list(array)
    n = len(arr)

    for i in range(1, n):
        key = arr[i]
        j = i - 1

        while j >= 0:
            if compare_counter:
                compare_counter.record()
            if arr[j] > key:
                arr[j + 1] = arr[j]
                if swap_counter:
                    swap_counter.record()  # dihitung sebagai 1 operasi geser/write
                if snapshot:
                    snapshot.capture(arr, highlight=(j, j + 1))
                j -= 1
            else:
                break

        arr[j + 1] = key
        if snapshot:
            snapshot.capture(arr, highlight=(j + 1,))

    return arr
