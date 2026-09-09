"""
bubble_sort.py
--------------
Implementasi Bubble Sort: pendekatan "Neighbor Swap".

Ide dasar: berulang kali menelusuri array dan menukar dua elemen
bersebelahan jika urutannya salah. Elemen terbesar akan "menggelembung"
(bubble up) ke posisi akhir pada setiap pass.

Kompleksitas waktu : O(N^2) worst/average, O(N) best (dengan optimasi
early-stop jika tidak ada swap dalam satu pass penuh).
Kompleksitas ruang  : O(1) — in-place.
Stability           : Stable (hanya menukar jika benar-benar `>`).
"""


def bubble_sort(
    array: list[int],
    swap_counter=None,
    compare_counter=None,
    snapshot=None,
) -> list[int]:
    """
    Mengurutkan array secara ascending menggunakan Bubble Sort.

    Parameter opsional swap_counter, compare_counter, dan snapshot
    memungkinkan pelacakan telemetry tanpa mengubah logika inti algoritma
    (Dependency Injection sederhana).
    """
    arr = list(array)  # jangan mutasi array asli milik pemanggil
    n = len(arr)

    for i in range(n - 1):
        swapped_in_pass = False
        for j in range(0, n - i - 1):
            if compare_counter:
                compare_counter.record()
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped_in_pass = True
                if swap_counter:
                    swap_counter.record()
                if snapshot:
                    snapshot.capture(arr, highlight=(j, j + 1))

        # Optimasi: jika satu pass penuh tanpa swap, array sudah terurut.
        if not swapped_in_pass:
            break

    return arr
