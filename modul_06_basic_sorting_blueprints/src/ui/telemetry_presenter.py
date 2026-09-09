"""
telemetry_presenter.py
-------------------------
Menampilkan tabel ringkasan metrik statistik (Swaps vs Comparisons vs Time)
hasil eksekusi satu atau beberapa algoritma sorting.
"""


def present_single_result(label: str, swaps: int, comparisons: int, elapsed_ms: float, peak_kb: float) -> None:
    """Menampilkan hasil telemetry satu algoritma dalam format ringkas."""
    print(f"\n=== {label} ===")
    print(f"  Comparisons : {comparisons:,}")
    print(f"  Swaps/Writes: {swaps:,}")
    print(f"  Waktu       : {elapsed_ms:.4f} ms")
    print(f"  Peak Memory : {peak_kb} KB")


def present_comparison_table(results: list[dict]) -> None:
    """
    Menampilkan tabel perbandingan beberapa algoritma sekaligus.
    Tiap elemen `results` diharapkan berupa dict dengan key:
    label, comparisons, swaps, elapsed_ms, peak_kb
    """
    header = f"{'Algoritma':<18}{'Comparisons':>14}{'Swaps':>12}{'Waktu (ms)':>14}{'Peak (KB)':>12}"
    print("\n" + header)
    print("-" * len(header))
    for r in results:
        print(
            f"{r['label']:<18}"
            f"{r['comparisons']:>14,}"
            f"{r['swaps']:>12,}"
            f"{r['elapsed_ms']:>14.4f}"
            f"{r['peak_kb']:>12}"
        )
