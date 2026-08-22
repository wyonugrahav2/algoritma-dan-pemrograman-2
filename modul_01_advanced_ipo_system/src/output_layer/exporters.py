"""
exporters.py
Memfasilitasi penyimpanan hasil luaran ke berkas eksternal (.csv, .json, .log, .txt).
"""

import csv
import json
from pathlib import Path

from config.constants import SUPPORTED_EXPORT_FORMATS
from src.domain.exceptions import ExportError, UnsupportedFormatError
from src.domain.models import ExportRequest, PipelineReport
from src.output_layer.formatters import format_as_json, format_as_plain_text, format_as_table_rows


def _export_json(report: PipelineReport, destination: Path) -> None:
    destination.write_text(format_as_json(report), encoding="utf-8")


def _export_txt_or_log(report: PipelineReport, destination: Path) -> None:
    destination.write_text(format_as_plain_text(report), encoding="utf-8")


def _export_csv(report: PipelineReport, destination: Path) -> None:
    rows = format_as_table_rows(report)
    if not rows:
        destination.write_text("", encoding="utf-8")
        return
    with destination.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


_EXPORTER_REGISTRY = {
    "json": _export_json,
    "csv": _export_csv,
    "txt": _export_txt_or_log,
    "log": _export_txt_or_log,
}


def export_report(request: ExportRequest, report: PipelineReport) -> Path:
    """Menyimpan PipelineReport ke berkas eksternal sesuai format yang diminta."""
    if request.file_format not in SUPPORTED_EXPORT_FORMATS:
        raise UnsupportedFormatError(
            f"Format ekspor '{request.file_format}' tidak didukung. "
            f"Pilihan: {SUPPORTED_EXPORT_FORMATS}"
        )

    destination = Path(request.destination_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    exporter_fn = _EXPORTER_REGISTRY.get(request.file_format)
    try:
        exporter_fn(report, destination)
    except OSError as exc:
        raise ExportError(f"Gagal menulis berkas ke '{destination}': {exc}") from exc

    return destination
