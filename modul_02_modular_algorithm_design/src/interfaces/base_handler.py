"""
Kontrak standar untuk komponen penanganan data (handler).

Handler dipakai oleh modul-modul yang perlu memproses data masuk/keluar
dengan signature seragam, misalnya untuk membaca input, menulis output,
atau meneruskan data ke tahap berikutnya dalam pipeline.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseHandler(ABC):
    """Kontrak dasar untuk semua data handler."""

    name: str = "base_handler"

    @abstractmethod
    def can_handle(self, data: Any) -> bool:
        """Tentukan apakah handler ini sanggup memproses data tersebut."""
        raise NotImplementedError

    @abstractmethod
    def handle(self, data: Any) -> Any:
        """Proses data dan kembalikan hasilnya."""
        raise NotImplementedError
