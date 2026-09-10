"""Entry Point: Robust CLI Orchestrator.

Mendemonstrasikan integrasi seluruh komponen resilience:
health check -> circuit breaker -> retry -> fallback -> crash reporting.
"""
from __future__ import annotations

import random
import sys

from src.exceptions.execution_errors import ResourceUnavailableError
from src.monitors.crash_reporter import CrashReporter
from src.monitors.health_check import run_health_check
from src.resilience.circuit_breaker import CircuitBreaker, CircuitOpenError
from src.resilience.fallback_manager import with_fallback
from src.resilience.retry_handler import RetryExhaustedError, retry_call
from src.ui.error_presenter import present_error
from src.ui.recovery_prompt import prompt_recovery_choice

breaker = CircuitBreaker(name="unstable-service")
crash_reporter = CrashReporter()


def unstable_service_call() -> str:
    """Simulasi layanan eksternal yang kadang gagal (untuk demo)."""
    if random.random() < 0.6:
        raise ResourceUnavailableError("unstable-service", "koneksi terputus")
    return "Data berhasil diambil dari layanan utama."


def fallback_service_call() -> str:
    return "Data cadangan (fallback) digunakan karena layanan utama bermasalah."


def run_pipeline() -> None:
    print("Menjalankan pemeriksaan kesehatan sistem...")
    report = run_health_check(dependencies=["json", "os"])
    print(report.summary())
    if not report.healthy:
        print("Sistem tidak sehat, tetap lanjut dengan mode hati-hati.\n")

    try:
        result = breaker.call(
            lambda: retry_call(
                unstable_service_call,
                max_attempts=3,
                base_backoff=0.1,
            )
        )
        print(f"Hasil: {result}")
    except (RetryExhaustedError, CircuitOpenError) as exc:
        print(present_error(exc))
        result = with_fallback(
            lambda: (_ for _ in ()).throw(exc),
            fallback_service_call,
            enabled=True,
        )
        print(f"Hasil (fallback): {result}")
    except Exception as exc:  # noqa: BLE001 - titik akhir penangkap crash
        crash_path = crash_reporter.report(exc, context={"stage": "run_pipeline"})
        print(present_error(exc))
        print(f"Laporan crash disimpan di: {crash_path}")
        choice = prompt_recovery_choice(input_fn=lambda _: "4")
        if choice == "4":
            sys.exit(1)


if __name__ == "__main__":
    run_pipeline()
