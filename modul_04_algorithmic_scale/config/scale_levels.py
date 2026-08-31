"""
scale_levels.py
Definisi tingkatan skala N yang digunakan oleh stress testing engine.

Setiap level merepresentasikan ukuran dataset sintetis yang akan
digunakan untuk menguji daya tahan (skalabilitas) sebuah algoritma,
mulai dari data sangat kecil (Tiny) hingga data skala raksasa (Huge).
"""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ScaleLevel:
    """Representasi satu tingkatan skala data uji."""
    name: str
    n: int
    description: str

    def __str__(self) -> str:
        return f"{self.name} (N={self.n:,})"


# Urutan skala dari yang terkecil ke yang terbesar.
SCALE_LEVELS: List[ScaleLevel] = [
    ScaleLevel("Tiny", 10, "Sampel data minimal, digunakan untuk uji sanity check cepat."),
    ScaleLevel("Small", 100, "Dataset kecil, dampak overhead lebih terlihat daripada kompleksitas."),
    ScaleLevel("Medium", 10_000, "Dataset menengah, mulai memperlihatkan pola pertumbuhan kompleksitas."),
    ScaleLevel("Large", 100_000, "Dataset besar, algoritma tidak efisien mulai melambat signifikan."),
    ScaleLevel("Huge", 1_000_000, "Dataset skala raksasa, menguji batas ketahanan waktu & memori."),
]


def get_level_by_name(name: str) -> ScaleLevel:
    """Mengambil objek ScaleLevel berdasarkan nama (case-insensitive)."""
    for level in SCALE_LEVELS:
        if level.name.lower() == name.lower():
            return level
    valid = ", ".join(level.name for level in SCALE_LEVELS)
    raise ValueError(f"Skala '{name}' tidak dikenal. Pilihan valid: {valid}")


def levels_up_to(name: str) -> List[ScaleLevel]:
    """Mengembalikan semua level dari Tiny hingga level 'name' (inklusif)."""
    result = []
    for level in SCALE_LEVELS:
        result.append(level)
        if level.name.lower() == name.lower():
            return result
    raise ValueError(f"Skala '{name}' tidak dikenal.")
