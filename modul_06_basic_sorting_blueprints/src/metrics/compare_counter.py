"""
compare_counter.py
-------------------
Menghitung jumlah operasi evaluasi kondisi (Comparisons), yaitu setiap kali
algoritma melakukan pengecekan seperti `A > B` atau `A < B`.
"""


class CompareCounter:
    """Objek penghitung comparison yang bisa disuntikkan ke algoritma sorting."""

    def __init__(self):
        self._count = 0

    def record(self, n: int = 1) -> None:
        """Mencatat terjadinya comparison sebanyak n kali (default 1)."""
        self._count += n

    @property
    def count(self) -> int:
        return self._count

    def reset(self) -> None:
        self._count = 0

    def __repr__(self) -> str:
        return f"CompareCounter(count={self._count})"
