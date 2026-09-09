"""
swap_counter.py
---------------
Menghitung jumlah operasi penukaran posisi (Swap/Write) yang terjadi
selama proses sorting. Dipisahkan dari compare_counter.py agar setiap
metrik punya tanggung jawab tunggal (Single Responsibility Principle).
"""


class SwapCounter:
    """Objek penghitung swap yang bisa disuntikkan ke dalam algoritma sorting."""

    def __init__(self):
        self._count = 0

    def record(self, n: int = 1) -> None:
        """Mencatat terjadinya swap sebanyak n kali (default 1)."""
        self._count += n

    @property
    def count(self) -> int:
        return self._count

    def reset(self) -> None:
        self._count = 0

    def __repr__(self) -> str:
        return f"SwapCounter(count={self._count})"
