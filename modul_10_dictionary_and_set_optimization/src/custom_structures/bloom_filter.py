"""
bloom_filter.py
Struktur data himpunan probabilitas (Probabilistic Set) untuk membership
testing sangat cepat dengan pemakaian memori mendekati nol dibanding
menyimpan seluruh key secara eksplisit.

Sifat penting:
- Tidak pernah menghasilkan False Negative ("mungkin belum pernah dilihat"
  selalu benar).
- Bisa menghasilkan False Positive ("mungkin sudah pernah dilihat" bisa
  salah), dengan probabilitas yang dapat dihitung/dikontrol.
"""

from __future__ import annotations
import hashlib
import math
from typing import Iterable


class BloomFilter:
    def __init__(self, expected_items: int = 10_000, false_positive_rate: float = 0.01):
        if expected_items <= 0:
            raise ValueError("expected_items harus > 0")
        if not (0 < false_positive_rate < 1):
            raise ValueError("false_positive_rate harus di antara 0 dan 1")

        self.expected_items = expected_items
        self.false_positive_rate = false_positive_rate

        # Formula standar ukuran bit array optimal:
        # m = -(n * ln(p)) / (ln(2)^2)
        self.size = max(
            8,
            int(-(expected_items * math.log(false_positive_rate)) / (math.log(2) ** 2)),
        )

        # Jumlah fungsi hash optimal: k = (m/n) * ln(2)
        self.hash_count = max(1, round((self.size / expected_items) * math.log(2)))

        self._bit_array = bytearray((self.size + 7) // 8)
        self.items_added = 0

    # ------------------------------------------------------------------ #
    # Hashing: gunakan double hashing (dua hash independen) untuk
    # mensimulasikan k fungsi hash tanpa perlu k algoritma hash berbeda.
    # ------------------------------------------------------------------ #
    def _hashes(self, item: str) -> Iterable[int]:
        data = str(item).encode("utf-8")
        h1 = int(hashlib.md5(data).hexdigest(), 16)
        h2 = int(hashlib.sha1(data).hexdigest(), 16)
        for i in range(self.hash_count):
            yield (h1 + i * h2) % self.size

    def _set_bit(self, index: int) -> None:
        self._bit_array[index // 8] |= 1 << (index % 8)

    def _get_bit(self, index: int) -> bool:
        return bool(self._bit_array[index // 8] & (1 << (index % 8)))

    # ------------------------------------------------------------------ #
    # API publik
    # ------------------------------------------------------------------ #
    def add(self, item: str) -> None:
        for idx in self._hashes(item):
            self._set_bit(idx)
        self.items_added += 1

    def might_contain(self, item: str) -> bool:
        return all(self._get_bit(idx) for idx in self._hashes(item))

    def current_false_positive_rate(self) -> float:
        """Estimasi FP rate aktual berdasarkan jumlah item yang sudah ditambahkan."""
        if self.items_added == 0:
            return 0.0
        exponent = -self.hash_count * self.items_added / self.size
        return (1 - math.exp(exponent)) ** self.hash_count

    def __len__(self) -> int:
        return self.items_added

    def __repr__(self) -> str:
        return (
            f"BloomFilter(size_bits={self.size}, hash_count={self.hash_count}, "
            f"items_added={self.items_added}, est_fp_rate={self.current_false_positive_rate():.4f})"
        )


if __name__ == "__main__":
    bf = BloomFilter(expected_items=1000, false_positive_rate=0.01)
    for word in ["apel", "jeruk", "mangga", "pisang"]:
        bf.add(word)
    print(bf)
    print("apel di dalam?", bf.might_contain("apel"))
    print("nanas di dalam?", bf.might_contain("nanas"))
