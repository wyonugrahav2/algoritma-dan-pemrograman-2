"""
merge_sort.py
-------------
Implementasi Merge Sort: pendekatan "Divide & Conquer" dengan Auxiliary Space.

Ide dasar:
1. Divide  : bagi array menjadi dua bagian sama besar secara rekursif
             sampai ukuran sub-array = 1 (sudah pasti terurut).
2. Conquer : gabungkan (merge) dua sub-array terurut menjadi satu
             array terurut yang lebih besar, memakai array bantu.

Kompleksitas waktu : O(N log N) pada SEMUA kasus (best/average/worst sama).
Kompleksitas ruang  : O(N) — membutuhkan array tambahan saat proses merge.
Stability           : Stable (saat nilai sama, elemen dari sub-array kiri
                      selalu diambil lebih dulu — gunakan `<=`).
"""


def merge_sort(
    array: list[int],
    swap_counter=None,
    compare_counter=None,
    snapshot=None,
) -> list[int]:
    """Mengurutkan array secara ascending menggunakan Merge Sort."""
    arr = list(array)
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], swap_counter, compare_counter, snapshot)
    right = merge_sort(arr[mid:], swap_counter, compare_counter, snapshot)

    return _merge(left, right, swap_counter, compare_counter, snapshot)


def _merge(left, right, swap_counter, compare_counter, snapshot) -> list[int]:
    """Menggabungkan dua sub-array terurut menjadi satu array terurut."""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if compare_counter:
            compare_counter.record()
        # "<=" (bukan "<") menjaga stability: elemen kiri didahulukan jika sama.
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

        if swap_counter:
            swap_counter.record()  # dihitung sebagai 1 operasi write ke auxiliary array
        if snapshot:
            snapshot.capture(result)

    result.extend(left[i:])
    result.extend(right[j:])
    return result
