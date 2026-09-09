"""
settings.py
Konfigurasi alur kerja pipeline (Modul 07 - Algorithm Integration Blueprint).

Memuat nilai bawaan (defaults) untuk eksekusi pipeline: ukuran batch,
mode logging, dan perilaku saat terjadi kegagalan pada suatu stage.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PipelineSettings:
    """Kumpulan pengaturan global untuk eksekusi pipeline."""

    # Apakah pipeline berhenti total saat satu stage gagal, atau
    # tetap melanjutkan (skip) ke stage berikutnya.
    stop_on_failure: bool = True

    # Aktifkan pencatatan waktu (profiling) di tiap stage.
    enable_stage_profiling: bool = True

    # Jumlah maksimum elemen yang ditampilkan di preview hasil CLI.
    preview_limit: int = 10

    # Level verbosity output: "quiet", "normal", "verbose".
    verbosity: str = "normal"


DEFAULT_SETTINGS = PipelineSettings()
