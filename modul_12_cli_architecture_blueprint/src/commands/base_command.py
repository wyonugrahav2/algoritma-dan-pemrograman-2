"""
base_command.py
Kelas dasar abstrak (Abstract Base Class) yang menjamin semua perintah
memiliki mekanisme penanganan kesalahan dan dokumentasi bantuan (--help)
yang seragam.

Setiap subcommand baru WAJIB mewarisi BaseCommand dan mengimplementasikan
method execute().
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class CommandError(Exception):
    """Exception khusus untuk kegagalan eksekusi command."""


class BaseCommand(ABC):
    #: Diisi ulang oleh subclass untuk teks bantuan (--help)
    help_text: str = "Tidak ada deskripsi untuk perintah ini."

    def __init__(self, context):
        self.context = context

    def run(self, args: Dict[str, Any]) -> int:
        """
        Template method: membungkus execute() dengan penanganan
        kesalahan yang seragam di semua command.
        Mengembalikan exit code (0 = sukses).
        """
        try:
            self.execute(args)
            return 0
        except CommandError as exc:
            self.context.presenter_error(str(exc))
            return 1
        except Exception as exc:  # pragma: no cover - safety net
            self.context.presenter_error(f"Kesalahan tak terduga: {exc}")
            return 2

    @abstractmethod
    def execute(self, args: Dict[str, Any]) -> None:
        """Logika eksekusi spesifik command. Wajib diimplementasikan subclass."""
        raise NotImplementedError

    def print_help(self) -> None:
        print(self.help_text)
