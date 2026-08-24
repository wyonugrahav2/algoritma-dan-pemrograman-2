"""
Modul Analisis Data (Analytics Module).

Modul terisolasi yang khusus menangani perhitungan metrik dan analisis
statistik data. Tidak memiliki dependensi langsung ke modul lain
(transformation, validation) -- hanya berkomunikasi lewat Event Bus
jika diperlukan.
"""

from __future__ import annotations

from typing import Any, Dict, List

from src.interfaces.base_module import BaseModule
from src.modules.analytics import metrics


class AnalyticsModule(BaseModule):
    """Menghitung ringkasan statistik dari data numerik yang diberikan."""

    name = "analytics"

    def initialize(self) -> None:
        # Tidak ada resource eksternal yang perlu dibuka untuk modul ini,
        # tapi hook ini tetap ada agar konsisten dengan kontrak BaseModule.
        self._ready = True

    def execute(self, payload: Any) -> Dict[str, Any]:
        """
        payload yang diharapkan:
            {"values": [1, 2, 3, ...]}
        """
        values: List[float] = payload.get("values", []) if isinstance(payload, dict) else list(payload)
        return metrics.summary(values)

    def cleanup(self) -> None:
        self._ready = False
