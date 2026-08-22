"""
presenters.py
Render visual CLI menggunakan tabel sederhana dan indikator warna ANSI,
tanpa dependensi wajib pada library eksternal (Rich bersifat opsional).
"""

from typing import Any, Dict, List

from config.constants import MAX_TERMINAL_ROWS
from src.domain.models import PipelineReport
from src.output_layer.formatters import format_as_json, format_as_plain_text, format_as_table_rows


class AnsiColor:
    """Kode warna ANSI dasar untuk indikator visual terminal."""
    RESET = "\033[0m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"


def _render_table(rows: List[Dict[str, Any]]) -> str:
    """Merender daftar dict menjadi tabel ASCII rata kolom."""
    if not rows:
        return "(tidak ada data untuk ditampilkan)"

    rows = rows[:MAX_TERMINAL_ROWS]
    headers = list(rows[0].keys())
    col_widths = {
        h: max(len(h), max(len(str(row[h])) for row in rows)) for h in headers
    }

    def render_row(values: List[str]) -> str:
        return " | ".join(v.ljust(col_widths[h]) for h, v in zip(headers, values))

    separator = "-+-".join("-" * col_widths[h] for h in headers)

    lines = [render_row(headers), separator]
    for row in rows:
        lines.append(render_row([str(row[h]) for h in headers]))

    return "\n".join(lines)


def present(report: PipelineReport, output_format: str = "table", use_color: bool = True) -> str:
    """Menghasilkan string presentasi akhir yang siap dicetak ke terminal."""
    status_label = "SUKSES" if report.is_successful else "GAGAL"
    color = AnsiColor.GREEN if report.is_successful else AnsiColor.RED

    if output_format == "json":
        body = format_as_json(report)
    elif output_format == "plain":
        body = format_as_plain_text(report)
    else:
        body = _render_table(format_as_table_rows(report))

    if not use_color:
        return f"[{status_label}] Hasil Pemrosesan IPO\n{body}"

    header = f"{AnsiColor.BOLD}{color}[{status_label}]{AnsiColor.RESET} Hasil Pemrosesan IPO"
    return f"{header}\n{AnsiColor.CYAN}{body}{AnsiColor.RESET}"


def print_report(report: PipelineReport, output_format: str = "table", use_color: bool = True) -> None:
    """Mencetak laporan langsung ke stdout."""
    print(present(report, output_format=output_format, use_color=use_color))
