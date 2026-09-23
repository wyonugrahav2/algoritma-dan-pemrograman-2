"""
process_cmd.py
Implementasi handler untuk subcommand 'process'.
Membaca berkas masukan, menerapkan transformasi sederhana (uppercase
baris demi baris sebagai contoh), lalu menulis ke berkas keluaran
atau menampilkannya di layar bila --dry-run digunakan.
"""

import os
from typing import Any, Dict

from src.commands.base_command import BaseCommand, CommandError
from src.components.spinners import run_with_spinner


class ProcessCommand(BaseCommand):
    help_text = "Memproses data masukan. Contoh: process <input> [--output PATH] [--dry-run]"

    def execute(self, args: Dict[str, Any]) -> None:
        input_path = args.get("input")
        output_path = args.get("output")
        dry_run = args.get("dry_run", False)

        if not input_path or not os.path.isfile(input_path):
            raise CommandError(f"Berkas masukan tidak ditemukan: {input_path}")

        processed_lines = run_with_spinner(
            "Memproses berkas...",
            lambda: self._process_file(input_path),
        )

        if dry_run or not output_path:
            self.context.presenter_success(
                f"[dry-run] {len(processed_lines)} baris berhasil diproses (tidak ditulis ke disk)."
            )
            for line in processed_lines[:5]:
                print(f"  {line}")
            if len(processed_lines) > 5:
                print(f"  ... ({len(processed_lines) - 5} baris lainnya)")
            return

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(processed_lines))

        self.context.presenter_success(
            f"{len(processed_lines)} baris ditulis ke {output_path}"
        )

    def _process_file(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return [line.rstrip("\n").upper() for line in lines]
