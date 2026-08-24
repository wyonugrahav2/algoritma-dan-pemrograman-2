"""
Konfigurasi sistem global.

Menyimpan pengaturan aplikasi yang dapat dibaca oleh seluruh modul
tanpa membuat modul-modul tersebut saling bergantung satu sama lain
(loose coupling tetap terjaga karena semua bergantung pada file ini,
bukan pada satu sama lain).
"""

import os
from dataclasses import dataclass, field
from typing import List


@dataclass
class Settings:
    app_name: str = "Modular Algorithm Design"
    environment: str = os.getenv("APP_ENV", "development")
    debug: bool = os.getenv("APP_DEBUG", "true").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    # Daftar modul yang diaktifkan secara default saat startup.
    # Dapat di-override lewat module_registry.py atau environment variable.
    enabled_modules: List[str] = field(
        default_factory=lambda: ["analytics", "transformation", "validation"]
    )


settings = Settings()
