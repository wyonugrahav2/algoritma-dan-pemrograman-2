"""
Dependency Injection (DI) Container.

Mengatur inisialisasi dan penyuntikan dependensi ke setiap modul
secara otomatis, sehingga modul tidak perlu tahu cara membuat
dependensinya sendiri -- cukup mendeklarasikan apa yang dibutuhkan.
"""

from __future__ import annotations

from typing import Any, Callable, Dict


class DependencyContainer:
    """Container sederhana untuk service/dependency registration & resolution."""

    def __init__(self) -> None:
        self._factories: Dict[str, Callable[[], Any]] = {}
        self._singletons: Dict[str, Any] = {}

    def register_factory(self, key: str, factory: Callable[[], Any]) -> None:
        """Daftarkan factory: dipanggil ulang setiap kali resolve() dipanggil."""
        self._factories[key] = factory

    def register_singleton(self, key: str, instance: Any) -> None:
        """Daftarkan instance tunggal yang akan selalu dikembalikan apa adanya."""
        self._singletons[key] = instance

    def resolve(self, key: str) -> Any:
        if key in self._singletons:
            return self._singletons[key]

        if key in self._factories:
            instance = self._factories[key]()
            return instance

        raise KeyError(f"Dependency '{key}' tidak terdaftar di container.")

    def has(self, key: str) -> bool:
        return key in self._factories or key in self._singletons

    def clear(self) -> None:
        self._factories.clear()
        self._singletons.clear()


# Instance global yang dipakai lintas aplikasi.
container = DependencyContainer()
