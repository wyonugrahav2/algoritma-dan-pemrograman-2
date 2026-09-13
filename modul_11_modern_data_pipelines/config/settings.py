"""
settings.py
Memuat konfigurasi global untuk pipeline: ukuran chunk, kapasitas buffer,
encoding berkas, dan environment variables (.env).
"""

import os
from dataclasses import dataclass


def _load_dotenv(path: str = ".env") -> None:
    """Loader .env sederhana tanpa dependensi eksternal (python-dotenv)."""
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


@dataclass(frozen=True)
class Settings:
    # Ukuran rekam data per kelompok saat streaming (Lazy Evaluation)
    CHUNK_SIZE: int = int(os.getenv("PIPELINE_CHUNK_SIZE", 1000))

    # Kapasitas buffer maksimum sebelum backpressure diaktifkan
    BUFFER_CAPACITY: int = int(os.getenv("PIPELINE_BUFFER_CAPACITY", 5000))

    # Encoding default untuk membaca/menulis berkas
    FILE_ENCODING: str = os.getenv("PIPELINE_FILE_ENCODING", "utf-8")

    # Delimiter default untuk berkas CSV
    CSV_DELIMITER: str = os.getenv("PIPELINE_CSV_DELIMITER", ",")

    # Interval (baris) untuk melaporkan progress ke UI
    PROGRESS_REPORT_INTERVAL: int = int(os.getenv("PIPELINE_PROGRESS_INTERVAL", 500))

    # Ambang batas backpressure (rasio buffer terisi sebelum jeda diberlakukan)
    BACKPRESSURE_HIGH_WATERMARK: float = float(
        os.getenv("PIPELINE_HIGH_WATERMARK", 0.85)
    )
    BACKPRESSURE_LOW_WATERMARK: float = float(
        os.getenv("PIPELINE_LOW_WATERMARK", 0.40)
    )


settings = Settings()
