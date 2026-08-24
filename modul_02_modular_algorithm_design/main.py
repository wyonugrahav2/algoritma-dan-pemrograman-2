from __future__ import annotations

import os
import sys

# Tambahkan path folder saat ini ke sys.path sebelum import lokal
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

"""
Entry Point aplikasi.

Bertanggung jawab untuk:
    1. Membaca konfigurasi & modul yang terdaftar.
    2. Menyiapkan Event Bus dan Dispatcher.
    3. Menjalankan pipeline modul secara dinamis.

Kode di file ini SENGAJA dibuat tipis (thin) -- semua logika berat
ada di dalam masing-masing modul, bukan di sini.
"""

import logging

from config.module_registry import registry
from config.settings import settings
from src.core.bus import event_bus
from src.core.dispatcher import Dispatcher
from src.utils.error_handlers import ModularAppError, logger


def configure_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def run_demo_pipeline() -> None:
    """Contoh alur: transformation -> analytics, dengan validation terpisah."""
    dispatcher = Dispatcher(registry, event_bus)

    raw_payload = {"values": ["  10 ", "20", "", "30", None]}

    logger.info("Menjalankan modul 'transformation'...")
    transformed = dispatcher.run_single("transformation", raw_payload)
    logger.info("Hasil transformation: %s", transformed)

    logger.info("Menjalankan modul 'validation'...")
    validation_result = dispatcher.run_single(
        "validation", {"data": transformed["values"]}
    )
    logger.info("Hasil validation: %s", validation_result)

    if not validation_result["valid"]:
        logger.warning("Data tidak lolos validasi, pipeline dihentikan lebih awal.")
        return

    numeric_values = [float(v) for v in transformed["values"]]
    logger.info("Menjalankan modul 'analytics'...")
    analytics_result = dispatcher.run_single("analytics", {"values": numeric_values})
    logger.info("Hasil analytics: %s", analytics_result)


def main() -> None:
    configure_logging()
    logger.info("Memulai aplikasi: %s (env=%s)", settings.app_name, settings.environment)
    logger.info("Modul aktif: %s", list(registry.all_registered().keys()))

    try:
        run_demo_pipeline()
    except ModularAppError as exc:
        logger.error("Aplikasi berhenti karena error: %s", exc)
        raise


if __name__ == "__main__":
    main()