"""Menyediakan prompt pemulihan interaktif di terminal saat terjadi kegagalan."""
from __future__ import annotations

from typing import Callable

RECOVERY_OPTIONS = {
    "1": "Coba lagi (retry)",
    "2": "Gunakan mode cadangan (fallback)",
    "3": "Lewati langkah ini (skip)",
    "4": "Keluar dari aplikasi",
}


def render_recovery_menu() -> str:
    lines = ["Pilihan pemulihan yang tersedia:"]
    for key, label in RECOVERY_OPTIONS.items():
        lines.append(f"  [{key}] {label}")
    return "\n".join(lines)


def prompt_recovery_choice(input_fn: Callable[[str], str] = input) -> str:
    """Menampilkan menu pemulihan dan mengembalikan pilihan pengguna (tervalidasi)."""
    print(render_recovery_menu())
    while True:
        choice = input_fn("Pilih opsi [1-4]: ").strip()
        if choice in RECOVERY_OPTIONS:
            return choice
        print("Pilihan tidak valid, silakan coba lagi.")
