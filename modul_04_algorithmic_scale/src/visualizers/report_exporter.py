"""
report_exporter.py
Memfasilitasi ekspor laporan analisis skalabilitas ke format
Markdown atau JSON, agar hasil stress testing dapat didokumentasikan
dan dibagikan.
"""

import json
import os
from dataclasses import asdict, is_dataclass
from datetime import datetime
from typing import Any, Dict, List

from config.settings import Settings


def _to_serializable(value: Any) -> Any:
    """Mengonversi dataclass / enum menjadi struktur dict/primitif agar bisa di-JSON-kan."""
    if is_dataclass(value):
        return {k: _to_serializable(v) for k, v in asdict(value).items()}
    if isinstance(value, dict):
        return {k: _to_serializable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_serializable(v) for v in value]
    if hasattr(value, "value") and not isinstance(value, (int, float, str, bool)):
        # Menangani Enum
        return value.value
    return value


def export_to_json(report: Dict[str, Any], filename: str = None, output_dir: str = None) -> str:
    """Mengekspor dictionary laporan ke file JSON. Mengembalikan path file yang dibuat."""
    output_dir = output_dir or Settings.REPORT_OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scalability_report_{timestamp}.json"

    filepath = os.path.join(output_dir, filename)
    serializable_report = _to_serializable(report)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(serializable_report, f, indent=2, ensure_ascii=False)

    return filepath


def export_to_markdown(report: Dict[str, Any], filename: str = None, output_dir: str = None) -> str:
    """Mengekspor dictionary laporan ke file Markdown yang mudah dibaca. Mengembalikan path file."""
    output_dir = output_dir or Settings.REPORT_OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scalability_report_{timestamp}.md"

    filepath = os.path.join(output_dir, filename)

    lines: List[str] = []
    lines.append(f"# Laporan Analisis Skalabilitas Algoritma")
    lines.append("")
    lines.append(f"- **Dihasilkan pada:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- **Algoritma diuji:** {report.get('algorithm_name', '-')}")
    lines.append(f"- **Estimasi kompleksitas:** {report.get('estimated_complexity', '-')}")
    lines.append(f"- **Confidence:** {report.get('confidence', '-')}")
    lines.append("")
    lines.append("## Hasil Pengukuran per Skala")
    lines.append("")
    lines.append("| Level | N | Rata-rata Waktu (s) | Peak Memory (MB) | Status |")
    lines.append("|---|---|---|---|---|")

    for row in report.get("measurements", []):
        status = "Timeout" if row.get("timed_out") else ("Melebihi RAM" if row.get("exceeded_memory") else "OK")
        lines.append(
            f"| {row.get('level', '-')} | {row.get('n', '-')} | "
            f"{row.get('mean_seconds', 0):.6f} | {row.get('peak_mb', 0):.3f} | {status} |"
        )

    lines.append("")
    if report.get("bottlenecks"):
        lines.append("## Bottleneck Terdeteksi")
        lines.append("")
        for bottleneck in report["bottlenecks"]:
            lines.append(f"- {bottleneck}")
        lines.append("")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return filepath
