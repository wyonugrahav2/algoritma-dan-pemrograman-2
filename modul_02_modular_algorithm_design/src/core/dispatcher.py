"""
Dispatcher.

Mengatur urutan alur eksekusi antar-modul berdasarkan konfigurasi
pendaftaran (module_registry). Dispatcher tidak tahu apa-apa tentang
logika internal tiap modul -- ia hanya tahu urutan dan cara memanggil
modul lewat kontrak BaseModule, sehingga tetap loosely coupled.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from config.module_registry import ModuleRegistry
from src.core.bus import EventBus


class Dispatcher:
    """Menjalankan serangkaian modul secara berurutan (pipeline)."""

    def __init__(self, registry: ModuleRegistry, bus: Optional[EventBus] = None) -> None:
        self.registry = registry
        self.bus = bus

    def run_pipeline(self, module_names: List[str], initial_payload: Any) -> Dict[str, Any]:
        """
        Jalankan modul secara berurutan, meneruskan output modul sebelumnya
        sebagai input modul berikutnya. Mengembalikan hasil tiap tahap.
        """
        payload = initial_payload
        results: Dict[str, Any] = {}

        for name in module_names:
            module = self.registry.load(name)
            output = module.run(payload)
            results[name] = output
            payload = output

            if self.bus is not None:
                self.bus.publish(f"module.{name}.completed", output)

        return results

    def run_single(self, module_name: str, payload: Any) -> Any:
        """Jalankan satu modul saja, di luar konteks pipeline."""
        module = self.registry.load(module_name)
        output = module.run(payload)

        if self.bus is not None:
            self.bus.publish(f"module.{module_name}.completed", output)

        return output
