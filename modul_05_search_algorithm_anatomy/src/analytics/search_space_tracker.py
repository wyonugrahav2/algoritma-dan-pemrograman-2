"""
search_space_tracker.py
Melacak koordinat pointer internal (left, mid/pos, right, bound) pada
setiap iterasi eksekusi algoritma pencarian.

PointerSnapshot didefinisikan di sini agar seluruh algoritma di
src/algorithms/ dapat mengimpor tipe yang sama tanpa duplikasi.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class PointerSnapshot:
    """
    Merepresentasikan satu titik waktu (satu iterasi) dalam eksekusi
    algoritma pencarian, mencatat posisi pointer yang relevan.

    Tidak semua field relevan untuk semua algoritma:
      - linear_search  -> hanya `pos` yang bermakna
      - binary_search  -> `left`, `mid` (disimpan di `pos`), `right`
      - interpolation  -> `left`, `pos` (estimasi), `right`
      - exponential    -> `bound`, lalu `left`/`pos`/`right` saat fase binary
      - hash_search    -> hanya `pos` (posisi hasil lookup)
    """

    step: int
    left: Optional[int] = None
    right: Optional[int] = None
    pos: Optional[int] = None
    bound: Optional[int] = None
    note: str = ""

    def space_size(self) -> Optional[int]:
        """Menghitung ukuran ruang pencarian saat ini (right - left + 1)."""
        if self.left is not None and self.right is not None:
            return max(0, self.right - self.left + 1)
        return None


@dataclass
class SearchSpaceTracker:
    """
    Kelas pembantu opsional untuk mengumpulkan snapshot secara imperatif
    (dipakai jika algoritma ditulis dengan gaya iteratif eksplisit,
    sebagai alternatif dari membangun list trace secara inline).
    """

    snapshots: List[PointerSnapshot] = field(default_factory=list)

    def record(self, **kwargs) -> PointerSnapshot:
        step = len(self.snapshots) + 1
        snapshot = PointerSnapshot(step=step, **kwargs)
        self.snapshots.append(snapshot)
        return snapshot

    def reduction_ratios(self) -> List[float]:
        """
        Menghitung rasio penyusutan ruang pencarian antar iterasi
        berurutan (space[i+1] / space[i]), untuk analisis empiris
        terhadap teori di docs/search_space_reduction.md.
        """
        sizes = [s.space_size() for s in self.snapshots if s.space_size() is not None]
        ratios = []
        for i in range(len(sizes) - 1):
            if sizes[i] and sizes[i] > 0:
                ratios.append(sizes[i + 1] / sizes[i])
        return ratios

    def total_steps(self) -> int:
        return len(self.snapshots)
