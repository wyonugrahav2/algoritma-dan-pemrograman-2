"""
Dynamic Module Registry.

Bertugas mencatat modul mana saja yang aktif saat runtime, serta
menyediakan mekanisme untuk mendaftarkan (register), membatalkan
pendaftaran (unregister), dan memuat (load) modul secara dinamis
berdasarkan nama string -- tanpa import langsung di kode inti.

Ini adalah kunci dari "pluggable module": modul baru bisa ditambahkan
hanya dengan mendaftarkannya di sini, tanpa mengubah kode orchestrator.
"""

from __future__ import annotations

import importlib
from typing import Dict, Optional, Type

from src.interfaces.base_module import BaseModule


class ModuleRegistry:
    """Registry singleton untuk seluruh modul aplikasi."""

    def __init__(self) -> None:
        self._registry: Dict[str, str] = {}
        self._instances: Dict[str, BaseModule] = {}

    def register(self, name: str, dotted_path: str) -> None:
        """Daftarkan modul baru berdasarkan nama dan path kelasnya.

        Contoh:
            register("analytics", "src.modules.analytics.analyzer.AnalyticsModule")
        """
        self._registry[name] = dotted_path

    def unregister(self, name: str) -> None:
        self._registry.pop(name, None)
        self._instances.pop(name, None)

    def is_registered(self, name: str) -> bool:
        return name in self._registry

    def load(self, name: str, **kwargs) -> BaseModule:
        """Muat (instansiasi) modul berdasarkan nama yang terdaftar."""
        if name in self._instances:
            return self._instances[name]

        if name not in self._registry:
            raise KeyError(f"Modul '{name}' belum terdaftar di registry.")

        module_path, class_name = self._registry[name].rsplit(".", 1)
        module = importlib.import_module(module_path)
        module_class: Type[BaseModule] = getattr(module, class_name)

        instance = module_class(**kwargs)
        self._instances[name] = instance
        return instance

    def get(self, name: str) -> Optional[BaseModule]:
        return self._instances.get(name)

    def all_registered(self) -> Dict[str, str]:
        return dict(self._registry)


# Instance global yang dipakai di seluruh aplikasi.
registry = ModuleRegistry()

# Pendaftaran modul default (bisa ditambah/dikurangi tanpa menyentuh kode lain).
registry.register("analytics", "src.modules.analytics.analyzer.AnalyticsModule")
registry.register("transformation", "src.modules.transformation.cleansers.TransformationModule")
registry.register("validation", "src.modules.validation.rules.ValidationModule")
