"""Menyediakan data atau alur cadangan (fallback) saat komponen utama gagal."""
from __future__ import annotations

from typing import Callable, TypeVar

from config.settings import FALLBACK_ENABLED
from config.error_codes import ERR_FALLBACK_FAILED
from src.exceptions.execution_errors import ExecutionError

T = TypeVar("T")


class FallbackFailedError(ExecutionError):
    def __init__(self, primary_error: Exception, fallback_error: Exception):
        super().__init__(
            "Fallback juga gagal dieksekusi setelah komponen utama gagal.",
            error_code=ERR_FALLBACK_FAILED,
            cause=fallback_error,
        )
        self.primary_error = primary_error
        self.fallback_error = fallback_error


def with_fallback(
    primary: Callable[[], T],
    fallback: Callable[[], T],
    *,
    enabled: bool = FALLBACK_ENABLED,
    catch: tuple[type[Exception], ...] = (Exception,),
) -> T:
    """Jalankan `primary`; bila gagal dan fallback aktif, jalankan `fallback`.

    Jika fallback tidak diaktifkan (mis. lewat konfigurasi), error asli
    langsung diteruskan tanpa mencoba fallback.
    """
    try:
        return primary()
    except catch as primary_error:
        if not enabled:
            raise
        try:
            return fallback()
        except Exception as fallback_error:
            raise FallbackFailedError(primary_error, fallback_error) from fallback_error


class FallbackManager:
    """Registry sederhana untuk memetakan nama komponen ke fungsi fallback-nya."""

    def __init__(self):
        self._fallbacks: dict[str, Callable[[], object]] = {}

    def register(self, component_name: str, fallback_fn: Callable[[], object]) -> None:
        self._fallbacks[component_name] = fallback_fn

    def has_fallback(self, component_name: str) -> bool:
        return component_name in self._fallbacks

    def resolve(self, component_name: str, primary_error: Exception) -> object:
        if component_name not in self._fallbacks:
            raise primary_error
        try:
            return self._fallbacks[component_name]()
        except Exception as fallback_error:
            raise FallbackFailedError(primary_error, fallback_error) from fallback_error
