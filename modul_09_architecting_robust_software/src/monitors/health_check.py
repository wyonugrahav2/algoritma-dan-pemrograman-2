"""Memeriksa integritas dependensi, sistem berkas, dan ruang penyimpanan
sebelum eksekusi dilanjutkan.
"""
from __future__ import annotations

import importlib
import shutil
from dataclasses import dataclass, field

from config.settings import HEALTH_CHECK_MIN_DISK_MB


@dataclass
class HealthCheckResult:
    name: str
    passed: bool
    detail: str = ""


@dataclass
class HealthReport:
    results: list[HealthCheckResult] = field(default_factory=list)

    @property
    def healthy(self) -> bool:
        return all(r.passed for r in self.results)

    def add(self, result: HealthCheckResult) -> None:
        self.results.append(result)

    def summary(self) -> str:
        status = "SEHAT" if self.healthy else "BERMASALAH"
        lines = [f"Status Sistem: {status}"]
        for r in self.results:
            mark = "OK" if r.passed else "GAGAL"
            lines.append(f"  [{mark}] {r.name}: {r.detail}")
        return "\n".join(lines)


def check_disk_space(path: str = ".", min_mb: int = HEALTH_CHECK_MIN_DISK_MB) -> HealthCheckResult:
    try:
        usage = shutil.disk_usage(path)
        free_mb = usage.free / (1024 * 1024)
        passed = free_mb >= min_mb
        return HealthCheckResult(
            "disk_space",
            passed,
            f"{free_mb:.1f}MB tersisa (minimum {min_mb}MB)",
        )
    except OSError as exc:
        return HealthCheckResult("disk_space", False, f"Gagal cek disk: {exc}")


def check_dependency(module_name: str) -> HealthCheckResult:
    try:
        importlib.import_module(module_name)
        return HealthCheckResult(f"dependency:{module_name}", True, "tersedia")
    except ImportError as exc:
        return HealthCheckResult(f"dependency:{module_name}", False, f"tidak ditemukan ({exc})")


def check_writable(path: str = ".") -> HealthCheckResult:
    import os

    ok = os.access(path, os.W_OK)
    return HealthCheckResult("writable_path", ok, path if ok else f"{path} tidak dapat ditulis")


def run_health_check(
    dependencies: list[str] | None = None,
    path: str = ".",
) -> HealthReport:
    """Menjalankan seluruh pemeriksaan kesehatan dan mengembalikan HealthReport."""
    report = HealthReport()
    report.add(check_disk_space(path))
    report.add(check_writable(path))
    for dep in dependencies or []:
        report.add(check_dependency(dep))
    return report
