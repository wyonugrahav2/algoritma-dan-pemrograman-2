"""
formatters.py
Mengubah hasil eksekusi dari process layer menjadi berbagai format
representasi (table-ready data, JSON, plain text) sebelum dirender.
"""

import json
from typing import Any, Dict, List

from src.domain.exceptions import UnsupportedFormatError
from src.domain.models import PipelineReport


def format_as_plain_text(report: PipelineReport) -> str:
    """Merepresentasikan PipelineReport sebagai teks polos."""
    lines = [
        f"Ringkasan Input : {report.input_summary}",
        f"Status          : {'SUKSES' if report.is_successful else 'GAGAL'}",
        f"Durasi Total    : {report.total_duration_ms:.3f} ms",
        "Tahapan:",
    ]
    for stage in report.stages:
        status = "OK" if stage.success else "ERROR"
        lines.append(f"  - [{status}] {stage.stage_name} ({stage.duration_ms:.3f} ms)")
    lines.append(f"Output Akhir    : {report.final_output}")
    return "\n".join(lines)


def format_as_json(report: PipelineReport) -> str:
    """Merepresentasikan PipelineReport sebagai string JSON."""
    payload: Dict[str, Any] = {
        "input_summary": report.input_summary,
        "is_successful": report.is_successful,
        "total_duration_ms": report.total_duration_ms,
        "generated_at": report.generated_at.isoformat(),
        "stages": [
            {
                "stage_name": s.stage_name,
                "success": s.success,
                "duration_ms": s.duration_ms,
                "error_message": s.error_message,
            }
            for s in report.stages
        ],
        "final_output": report.final_output,
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def format_as_table_rows(report: PipelineReport) -> List[Dict[str, Any]]:
    """Mengubah tahapan pipeline menjadi baris-baris siap tampil sebagai tabel."""
    rows = []
    for stage in report.stages:
        rows.append(
            {
                "Tahap": stage.stage_name,
                "Status": "OK" if stage.success else "ERROR",
                "Durasi (ms)": f"{stage.duration_ms:.3f}",
                "Catatan": stage.error_message or "-",
            }
        )
    return rows


FORMATTER_REGISTRY = {
    "plain": format_as_plain_text,
    "json": format_as_json,
    "table": format_as_table_rows,
}


def format_report(report: PipelineReport, output_format: str):
    """Dispatcher utama untuk memilih formatter berdasarkan nama format."""
    formatter_fn = FORMATTER_REGISTRY.get(output_format)
    if formatter_fn is None:
        raise UnsupportedFormatError(f"Format '{output_format}' tidak didukung.")
    return formatter_fn(report)
