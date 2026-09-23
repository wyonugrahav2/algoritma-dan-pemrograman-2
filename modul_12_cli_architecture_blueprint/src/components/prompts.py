"""
prompts.py
Kumpulan prompt interaktif sederhana: konfirmasi ya/tidak dan
pemilihan dari daftar opsi. Digunakan ketika argumen wajib tidak
disediakan lewat flag, tanpa menghalangi penggunaan non-interaktif.
"""

from typing import List, Optional, Sequence


def confirm(message: str, default: bool = False) -> bool:
    """Menampilkan prompt ya/tidak. Mengembalikan True/False."""
    suffix = "[Y/n]" if default else "[y/N]"
    answer = input(f"{message} {suffix}: ").strip().lower()
    if not answer:
        return default
    return answer in ("y", "yes", "ya")


def select_option(message: str, options: Sequence[str]) -> Optional[str]:
    """Menampilkan daftar opsi bernomor dan meminta pengguna memilih satu."""
    if not options:
        return None

    print(message)
    for idx, option in enumerate(options, start=1):
        print(f"  {idx}. {option}")

    while True:
        raw = input(f"Pilih (1-{len(options)}): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        print("Pilihan tidak valid, coba lagi.")
