"""
Abstract Base Class standar yang WAJIB diimplementasikan oleh setiap modul.

Setiap modul independen (analytics, transformation, validation, dst.)
harus mewarisi kelas ini dan mengimplementasikan method initialize(),
execute(), dan cleanup() agar dapat dikenali dan dijalankan secara
seragam oleh dispatcher / container, terlepas dari logika internalnya.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseModule(ABC):
    """Kontrak dasar untuk seluruh modul plug-and-play."""

    #: Nama unik modul, dipakai oleh registry & event bus.
    name: str = "base_module"

    def __init__(self, **config: Any) -> None:
        self.config: Dict[str, Any] = config
        self._initialized: bool = False

    @abstractmethod
    def initialize(self) -> None:
        """Persiapan modul sebelum dieksekusi (load resource, dsb.)."""
        raise NotImplementedError

    @abstractmethod
    def execute(self, payload: Any) -> Any:
        """Logika utama modul. Menerima payload, mengembalikan hasil."""
        raise NotImplementedError

    @abstractmethod
    def cleanup(self) -> None:
        """Pembersihan resource setelah modul selesai dipakai."""
        raise NotImplementedError

    def run(self, payload: Any) -> Any:
        """Helper standar: initialize -> execute -> cleanup."""
        if not self._initialized:
            self.initialize()
            self._initialized = True
        try:
            return self.execute(payload)
        finally:
            self.cleanup()
