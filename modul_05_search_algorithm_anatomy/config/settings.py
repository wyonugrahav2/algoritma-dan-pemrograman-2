"""
settings.py
Konfigurasi ambang batas (threshold) pencarian dan parameter indeks.

Modul ini menyimpan semua konstanta global yang digunakan oleh
strategy handler, indexer, dan analytics engine agar perilaku
CLI Search Engine tetap konsisten dan mudah dikonfigurasi ulang.
"""

import os
from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class SearchThresholds:
    """Ambang batas yang menentukan strategi pencarian mana yang layak dipakai."""

    # Di bawah nilai ini, Linear Search dianggap cukup efisien
    # walau data sudah terurut (overhead binary search tidak sepadan).
    linear_search_max_n: int = 32

    # Jumlah minimum elemen agar Interpolation Search dipertimbangkan
    # (di bawah ini, binary search sudah cukup optimal).
    interpolation_min_n: int = 64

    # Toleransi "keseragaman" distribusi data (0.0 - 1.0).
    # Semakin mendekati 1.0, data dianggap terdistribusi uniform,
    # sehingga Interpolation Search akan sangat efektif (mendekati O(log log N)).
    uniformity_tolerance: float = 0.85

    # Batas awal (bound) untuk Exponential Search sebelum binary search
    # dijalankan pada rentang yang ditemukan.
    exponential_initial_bound: int = 1

    # Faktor pertumbuhan bound pada Exponential Search (umumnya 2x).
    exponential_growth_factor: int = 2


@dataclass(frozen=True)
class IndexConfig:
    """Parameter untuk pembangunan struktur indeks (Hash Map & Inverted Index)."""

    # Rasio maksimum load factor sebelum hash map dianggap perlu di-resize.
    hash_max_load_factor: float = 0.75

    # Ukuran awal tabel hash (jumlah bucket).
    hash_initial_buckets: int = 16

    # Apakah data harus di-pre-sort sebelum diindeks (wajib untuk
    # Binary/Interpolation/Exponential Search).
    require_presort: bool = True

    # Kolom/field yang dianggap sebagai kunci pencarian utama saat
    # membangun inverted index dari dataset terstruktur (CSV/JSON).
    default_search_fields: List[str] = field(default_factory=lambda: ["id", "value", "key"])


@dataclass(frozen=True)
class AppSettings:
    """Kumpulan konfigurasi utama aplikasi, dapat dioverride lewat .env"""

    app_name: str = "Search Algorithm Anatomy CLI"
    version: str = "1.0.0"
    default_algorithm: str = "binary"
    enable_step_visualizer: bool = True
    enable_profiler: bool = True
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    thresholds: SearchThresholds = field(default_factory=SearchThresholds)
    index_config: IndexConfig = field(default_factory=IndexConfig)


# Instance singleton yang diimpor oleh modul-modul lain.
settings = AppSettings()


def load_settings_from_env() -> AppSettings:
    """
    Memuat ulang setting dari environment variable (.env) jika tersedia.
    Berguna saat aplikasi dijalankan di lingkungan deployment berbeda.
    """
    return AppSettings(
        default_algorithm=os.getenv("DEFAULT_ALGORITHM", "binary"),
        enable_step_visualizer=os.getenv("ENABLE_STEP_VISUALIZER", "true").lower() == "true",
        enable_profiler=os.getenv("ENABLE_PROFILER", "true").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )
