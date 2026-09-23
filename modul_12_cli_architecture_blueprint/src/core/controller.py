"""
controller.py
Jembatan penghubung antara perintah CLI (Presentation Layer) dan
logika bisnis inti (Application Core). Command handler idealnya
memanggil controller ini alih-alih menaruh logika bisnis langsung
di dalam file *_cmd.py, sehingga logika bisa diuji terpisah dari
lapisan CLI.
"""

from typing import Any, Dict, List

from src.core.context import AppContext


class AppController:
    """
    Titik masuk tunggal untuk operasi bisnis yang dipakai lebih dari
    satu command, atau yang cukup kompleks untuk dipisah dari handler.
    """

    def __init__(self, context: AppContext):
        self.context = context

    def health_check(self) -> Dict[str, Any]:
        """Contoh operasi inti: memeriksa status kesiapan sistem."""
        return {
            "status": "ok",
            "verbose": self.context.verbose,
            "config_keys": list(self.context.config.keys()),
        }
