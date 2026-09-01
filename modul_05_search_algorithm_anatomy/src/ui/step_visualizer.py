"""
step_visualizer.py
Merender animasi visual pergeseran pointer dan penciutan ruang
pencarian secara langsung di jendela terminal CLI.
"""

import time
from typing import Sequence

from src.algorithms.linear_search import SearchResult

POINTER_SYMBOLS = {
    "left": "L",
    "right": "R",
    "pos": "^",
}


def render_step(data: Sequence, snapshot, width_per_cell: int = 4) -> str:
    """
    Merender satu baris representasi array beserta marker pointer
    (L untuk left, R untuk right, ^ untuk mid/pos) di bawahnya.
    """
    value_row = "".join(f"{str(v):>{width_per_cell}}" for v in data)
    marker_row = [" " * width_per_cell for _ in data]

    def place_marker(idx, symbol):
        if idx is not None and 0 <= idx < len(data):
            cell = " " * (width_per_cell - 1) + symbol
            marker_row[idx] = cell

    place_marker(getattr(snapshot, "left", None), "L")
    place_marker(getattr(snapshot, "right", None), "R")
    place_marker(getattr(snapshot, "pos", None), "^")

    return value_row + "\n" + "".join(marker_row)


def animate_search(
    data: Sequence,
    result: SearchResult,
    delay_seconds: float = 0.4,
    clear_screen: bool = False,
) -> None:
    """
    Memutar ulang (replay) seluruh trace dari `result` sebagai animasi
    teks sederhana di terminal, menunjukkan bagaimana search space
    menyusut pada tiap iterasi.

    Parameter `clear_screen` dapat dinonaktifkan (default False) agar
    seluruh riwayat langkah tetap terlihat, cocok untuk keperluan
    debugging/analisis; aktifkan untuk efek animasi murni.
    """
    print(f"\n--- Visualisasi Eksekusi: {result.algorithm.upper()} Search ---")
    print(f"Data ({len(data)} elemen): {list(data)}\n")

    for snapshot in result.trace:
        if clear_screen:
            print("\033c", end="")

        print(f"Langkah {snapshot.step}:")
        print(render_step(data, snapshot))

        space_size = snapshot.space_size() if hasattr(snapshot, "space_size") else None
        if space_size is not None:
            print(f"Ukuran ruang pencarian saat ini: {space_size}")
        if snapshot.note:
            print(f"Catatan: {snapshot.note}")

        print("-" * 40)
        time.sleep(delay_seconds)

    if result.found:
        print(f"Target ditemukan pada index {result.index} setelah {result.comparisons} langkah.")
    else:
        print(f"Target tidak ditemukan setelah {result.comparisons} langkah.")


def render_reduction_summary(result: SearchResult) -> str:
    """
    Menampilkan ringkasan tekstual (non-animasi) tentang bagaimana
    ukuran ruang pencarian menyusut sepanjang trace, contoh:
    "N=100 -> 50 -> 25 -> 12 -> 6 -> FOUND"
    """
    sizes = []
    for snapshot in result.trace:
        size = snapshot.space_size() if hasattr(snapshot, "space_size") else None
        if size is not None:
            sizes.append(str(size))

    if not sizes:
        return f"Tidak ada data ruang pencarian untuk algoritma '{result.algorithm}'."

    trail = " -> ".join(sizes)
    outcome = "FOUND" if result.found else "NOT FOUND"
    return f"{trail} -> {outcome}"
