"""
state_snapshot.py
-------------------
Mengambil snapshot atau rekam jejak kondisi array setiap kali terjadi
mutasi elemen atau swap. Rekaman ini menjadi bahan baku untuk animasi
bar chart di src/ui/bar_chart_renderer.py.
"""


class StateSnapshot:
    """Merekam salinan array pada setiap titik mutasi penting."""

    def __init__(self):
        self._frames: list[list[int]] = []
        self._highlighted_indices: list[tuple[int, ...]] = []

    def capture(self, array: list[int], highlight: tuple[int, ...] = ()) -> None:
        """
        Menyimpan salinan (bukan referensi) dari array saat ini,
        beserta indeks yang ingin disorot (misal posisi yang baru ditukar).
        """
        self._frames.append(list(array))
        self._highlighted_indices.append(highlight)

    @property
    def frames(self) -> list[list[int]]:
        return self._frames

    @property
    def highlighted_indices(self) -> list[tuple[int, ...]]:
        return self._highlighted_indices

    def __len__(self) -> int:
        return len(self._frames)

    def clear(self) -> None:
        self._frames.clear()
        self._highlighted_indices.clear()
