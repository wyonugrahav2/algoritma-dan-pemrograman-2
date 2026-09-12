"""
key_compressor.py
Penghemat alokasi memori string key menggunakan teknik String Interning:
memastikan string yang identik secara isi berbagi satu objek memori yang
sama, bukan disalin berulang kali.
"""

from __future__ import annotations
import sys
from typing import Dict, Iterable, List


class KeyCompressor:
    """
    Wrapper di atas sys.intern() dengan statistik pemakaian, supaya bisa
    dilihat berapa banyak duplikasi string key yang berhasil dihemat.
    """

    def __init__(self) -> None:
        self._pool: Dict[str, str] = {}
        self.total_requests = 0
        self.pool_hits = 0

    def compress(self, key: str) -> str:
        self.total_requests += 1
        interned = sys.intern(str(key))
        if interned in self._pool:
            self.pool_hits += 1
        else:
            self._pool[interned] = interned
        return interned

    def compress_many(self, keys: Iterable[str]) -> List[str]:
        return [self.compress(k) for k in keys]

    @property
    def unique_keys(self) -> int:
        return len(self._pool)

    def savings_ratio(self) -> float:
        """Perkiraan persentase alokasi string yang dihindari."""
        if self.total_requests == 0:
            return 0.0
        return self.pool_hits / self.total_requests

    def __repr__(self) -> str:
        return (
            f"KeyCompressor(unique_keys={self.unique_keys}, "
            f"requests={self.total_requests}, savings={self.savings_ratio():.2%})"
        )


if __name__ == "__main__":
    compressor = KeyCompressor()
    keys = ["status", "active", "status", "status", "inactive", "active"]
    compressed = compressor.compress_many(keys)
    print(compressor)
    # Buktikan bahwa dua string "status" adalah objek identik (identity check)
    print("Identity check:", compressed[0] is compressed[2])
