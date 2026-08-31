"""
settings.py
Pengaturan global engine: ambang batas waktu eksekusi (timeout),
batas alokasi RAM, dan opsi default lainnya.

Nilai-nilai ini dapat dioverride lewat environment variable
(lihat .env.example) agar mudah disesuaikan tanpa mengubah kode.
"""

import os


def _get_float_env(key: str, default: float) -> float:
    try:
        return float(os.environ.get(key, default))
    except (TypeError, ValueError):
        return default


def _get_int_env(key: str, default: int) -> int:
    try:
        return int(os.environ.get(key, default))
    except (TypeError, ValueError):
        return default


class Settings:
    # Batas waktu eksekusi (detik) sebelum sebuah uji dianggap timeout.
    EXECUTION_TIMEOUT_SECONDS: float = _get_float_env("EXECUTION_TIMEOUT_SECONDS", 10.0)

    # Batas alokasi memori (MB) sebelum sebuah uji dianggap melebihi kuota RAM.
    MAX_MEMORY_MB: float = _get_float_env("MAX_MEMORY_MB", 512.0)

    # Jumlah pengulangan (repeats) tiap pengukuran untuk mengurangi noise waktu.
    REPEATS_PER_MEASUREMENT: int = _get_int_env("REPEATS_PER_MEASUREMENT", 3)

    # Seed default untuk data sintetis agar hasil dapat direproduksi.
    RANDOM_SEED: int = _get_int_env("RANDOM_SEED", 42)

    # Direktori output laporan.
    REPORT_OUTPUT_DIR: str = os.environ.get("REPORT_OUTPUT_DIR", "reports")

    # Lebar grafik ASCII default (karakter).
    ASCII_PLOT_WIDTH: int = _get_int_env("ASCII_PLOT_WIDTH", 60)
    ASCII_PLOT_HEIGHT: int = _get_int_env("ASCII_PLOT_HEIGHT", 15)

    @classmethod
    def as_dict(cls) -> dict:
        return {
            "EXECUTION_TIMEOUT_SECONDS": cls.EXECUTION_TIMEOUT_SECONDS,
            "MAX_MEMORY_MB": cls.MAX_MEMORY_MB,
            "REPEATS_PER_MEASUREMENT": cls.REPEATS_PER_MEASUREMENT,
            "RANDOM_SEED": cls.RANDOM_SEED,
            "REPORT_OUTPUT_DIR": cls.REPORT_OUTPUT_DIR,
            "ASCII_PLOT_WIDTH": cls.ASCII_PLOT_WIDTH,
            "ASCII_PLOT_HEIGHT": cls.ASCII_PLOT_HEIGHT,
        }
