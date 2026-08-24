"""
Penanganan error terpusat untuk seluruh modul.

Mendefinisikan hierarki exception khusus aplikasi serta helper untuk
menangkap dan mencatat error secara konsisten, tanpa membuat modul
individual bergantung satu sama lain.
"""

from __future__ import annotations

import logging
import traceback
from typing import Any, Callable, TypeVar

logger = logging.getLogger("modular_app")
T = TypeVar("T")


class ModularAppError(Exception):
    """Base exception untuk seluruh error kustom aplikasi ini."""


class ModuleNotFoundError_(ModularAppError):
    """Dilempar saat modul yang diminta tidak terdaftar di registry."""


class ModuleExecutionError(ModularAppError):
    """Dilempar saat modul gagal dieksekusi (error di dalam execute())."""

    def __init__(self, module_name: str, original_error: Exception) -> None:
        self.module_name = module_name
        self.original_error = original_error
        super().__init__(
            f"Modul '{module_name}' gagal dieksekusi: {original_error}"
        )


class ValidationFailedError(ModularAppError):
    """Dilempar saat data tidak lolos validasi dan proses harus dihentikan."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__(f"Validasi gagal: {'; '.join(errors)}")


def safe_run(func: Callable[..., T], *args: Any, **kwargs: Any) -> T | None:
    """Jalankan fungsi, tangkap & catat error tanpa menghentikan aplikasi."""
    try:
        return func(*args, **kwargs)
    except ModularAppError as exc:
        logger.error(str(exc))
        return None
    except Exception as exc:  # noqa: BLE001 - sengaja menangkap semua error tak terduga
        logger.error("Error tak terduga: %s\n%s", exc, traceback.format_exc())
        return None
