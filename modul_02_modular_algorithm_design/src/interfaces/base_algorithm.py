"""
Template dasar untuk seluruh algoritma yang dipakai di dalam modul.

Berbeda dari BaseModule (yang mengatur siklus hidup modul secara umum),
BaseAlgorithm berfokus murni pada kontrak input -> proses -> output
sebuah algoritma tunggal, sehingga algoritma dapat diuji dan diganti
secara independen dari modul yang membungkusnya.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseAlgorithm(ABC):
    """Kontrak standar untuk sebuah algoritma yang dapat dipasang/dilepas."""

    name: str = "base_algorithm"
    version: str = "1.0.0"

    @abstractmethod
    def validate_input(self, data: Any) -> bool:
        """Cek apakah data input valid sebelum diproses."""
        raise NotImplementedError

    @abstractmethod
    def process(self, data: Any) -> Any:
        """Jalankan logika inti algoritma."""
        raise NotImplementedError

    def run(self, data: Any) -> Any:
        if not self.validate_input(data):
            raise ValueError(f"Input tidak valid untuk algoritma '{self.name}'.")
        return self.process(data)
