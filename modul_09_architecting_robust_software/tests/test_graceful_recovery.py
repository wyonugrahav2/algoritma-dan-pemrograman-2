"""Uji sistem tetap aman dan tidak crash setelah error tertangani."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import tempfile

from src.exceptions.validation_errors import InvalidInputError
from src.monitors.crash_reporter import CrashReporter
from src.monitors.health_check import run_health_check
from src.ui.error_presenter import present_error


def test_error_presenter_handles_app_exception():
    exc = InvalidInputError("umur", -5)
    message = present_error(exc)
    assert "VAL-100" in message
    assert "Kesalahan" in message


def test_error_presenter_handles_generic_exception():
    message = present_error(ValueError("hal tak terduga"))
    assert "Tak Terduga" in message


def test_crash_reporter_writes_report():
    with tempfile.TemporaryDirectory() as tmpdir:
        reporter = CrashReporter(log_dir=tmpdir)
        try:
            raise RuntimeError("simulasi crash")
        except RuntimeError as exc:
            path = reporter.report(exc, context={"stage": "test"})
        assert Path(path).exists()


def test_health_check_reports_status():
    report = run_health_check(dependencies=["os", "json"])
    assert report.healthy in (True, False)
    assert len(report.results) >= 2
