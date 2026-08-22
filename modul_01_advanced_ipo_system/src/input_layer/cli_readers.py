"""
cli_readers.py
Reader interaktif dan argument parser untuk antarmuka CLI.
Bertanggung jawab hanya pada mekanisme "bagaimana" data diterima,
bukan "apa arti" data tersebut (dipisahkan ke validators/parsers).
"""

import argparse
from typing import List, Optional

from src.domain.models import RawInput


def build_cli_argument_parser() -> argparse.ArgumentParser:
    """Membangun argument parser untuk mode non-interaktif (CLI flags)."""
    parser = argparse.ArgumentParser(
        prog="ipo-cli",
        description="Advanced IPO Problem Analysis CLI System",
    )
    parser.add_argument(
        "--values",
        type=str,
        help="Daftar nilai numerik dipisahkan koma, contoh: '1,2,3.5'",
    )
    parser.add_argument(
        "--format",
        type=str,
        default="table",
        choices=("table", "json", "plain"),
        help="Format tampilan output di terminal.",
    )
    parser.add_argument(
        "--export",
        type=str,
        default=None,
        help="Path berkas tujuan untuk ekspor hasil (opsional).",
    )
    return parser


def read_cli_arguments(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Membaca argumen dari command line."""
    parser = build_cli_argument_parser()
    return parser.parse_args(argv)


def read_interactive_input(prompt: str = "Masukkan nilai: ") -> RawInput:
    """Membaca satu baris input interaktif dari pengguna melalui stdin."""
    raw_value = input(prompt)
    return RawInput(raw_value=raw_value, source="interactive")


def read_from_string(value: str, source: str = "cli_flag") -> RawInput:
    """Membungkus nilai string (mis. dari argparse) menjadi RawInput."""
    return RawInput(raw_value=value, source=source)
