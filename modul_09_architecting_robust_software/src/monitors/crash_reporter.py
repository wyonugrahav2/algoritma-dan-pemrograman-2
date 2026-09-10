"""Mencatat log dump dan status sistem saat terjadi kegagalan
untuk kebutuhan audit dan debugging.
"""
from __future__ import annotations

import json
import os
import traceback
from datetime import datetime, timezone

from config.settings import CRASH_LOG_DIR
from src.exceptions.base_exceptions import AppException


class CrashReporter:
    """Menulis crash report terstruktur (JSON) ke direktori log."""

    def __init__(self, log_dir: str = CRASH_LOG_DIR):
        self.log_dir = log_dir

    def _ensure_log_dir(self) -> None:
        os.makedirs(self.log_dir, exist_ok=True)

    def build_report(self, exc: BaseException, context: dict | None = None) -> dict:
        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "exception_type": type(exc).__name__,
            "message": str(exc),
            "traceback": traceback.format_exception(type(exc), exc, exc.__traceback__),
            "context": context or {},
        }
        if isinstance(exc, AppException):
            report["error_code"] = exc.error_code
            report["app_exception"] = exc.to_dict()
        return report

    def report(self, exc: BaseException, context: dict | None = None) -> str:
        """Menyimpan crash report ke berkas dan mengembalikan path-nya."""
        self._ensure_log_dir()
        report = self.build_report(exc, context)
        filename = f"crash_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')}.json"
        filepath = os.path.join(self.log_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        return filepath
