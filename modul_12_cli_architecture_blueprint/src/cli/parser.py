"""
parser.py
Ekstraktor argumen baris perintah. Menerjemahkan teks masukan pengguna
(sys.argv) menjadi objek 'ParsedCommand' yang siap diteruskan ke router.

Presentation Layer TIDAK boleh berisi logika bisnis apa pun -- parser
hanya bertugas membaca struktur argumen (command, subcommand, flags).
"""

import argparse
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from config.settings import APP_NAME, APP_VERSION
from config.commands_registry import get_registered_commands


@dataclass
class ParsedCommand:
    """Hasil parsing: nama command, argumen posisional, dan opsi/flag."""
    name: Optional[str]
    args: Dict[str, Any] = field(default_factory=dict)
    verbose: bool = False
    theme: str = "default"


def build_parser() -> argparse.ArgumentParser:
    """Membangun ArgumentParser lengkap dengan seluruh subcommand terdaftar."""
    parser = argparse.ArgumentParser(
        prog=APP_NAME,
        description="CLI Architecture Framework & Command Dispatcher Engine",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"{APP_NAME} {APP_VERSION}"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Tampilkan log eksekusi detail"
    )
    parser.add_argument(
        "--theme", default="default", choices=["default", "mono"],
        help="Pilih tema warna terminal"
    )

    subparsers = parser.add_subparsers(dest="command", help="Subcommand yang tersedia")

    # search
    search_p = subparsers.add_parser("search", help="Mencari data berdasarkan kata kunci")
    search_p.add_argument("query", help="Kata kunci pencarian")
    search_p.add_argument("--format", default="table", choices=["table", "json"])
    search_p.add_argument("--limit", type=int, default=20)

    # process
    process_p = subparsers.add_parser("process", help="Memproses data masukan")
    process_p.add_argument("input", help="Path berkas atau data masukan")
    process_p.add_argument("--output", default=None, help="Path berkas keluaran")
    process_p.add_argument("--dry-run", action="store_true")

    # config
    config_p = subparsers.add_parser("config", help="Mengelola konfigurasi aplikasi")
    config_sub = config_p.add_subparsers(dest="config_action")
    get_p = config_sub.add_parser("get")
    get_p.add_argument("key")
    set_p = config_sub.add_parser("set")
    set_p.add_argument("key")
    set_p.add_argument("value")
    config_sub.add_parser("list")

    return parser


def parse_args(argv=None) -> ParsedCommand:
    """
    Parsing utama. Mengembalikan ParsedCommand siap pakai oleh router.
    argv=None berarti mengambil dari sys.argv (perilaku default argparse).
    """
    parser = build_parser()
    namespace = parser.parse_args(argv)

    args_dict = vars(namespace).copy()
    command_name = args_dict.pop("command", None)
    verbose = args_dict.pop("verbose", False)
    theme = args_dict.pop("theme", "default")

    # Buang kunci yang bernilai None supaya handler tidak perlu cek None terus
    args_dict = {k: v for k, v in args_dict.items() if v is not None}

    return ParsedCommand(name=command_name, args=args_dict, verbose=verbose, theme=theme)
