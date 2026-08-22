"""
logger.py
Logger sistem terpusat untuk melacak alur eksekusi (audit trail)
di seluruh layer aplikasi.
"""

import logging
import sys
from pathlib import Path

from config.settings import settings


def get_logger(name: str) -> logging.Logger:
    """Membuat/mengambil logger dengan konfigurasi standar sistem IPO."""
    logger = logging.getLogger(name)

    if logger.handlers:
        # Hindari duplikasi handler jika logger sudah pernah dikonfigurasi
        return logger

    logger.setLevel(settings.log_level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    try:
        settings.log_dir.mkdir(parents=True, exist_ok=True)
        log_file = Path(settings.log_dir) / "ipo_system.log"
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except OSError:
        # Jika direktori log tidak dapat dibuat, sistem tetap berjalan
        # hanya dengan logging ke konsol.
        logger.warning("Tidak dapat membuat direktori log; logging file dinonaktifkan.")

    logger.propagate = False
    return logger
