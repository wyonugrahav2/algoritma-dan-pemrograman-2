"""
theme.py
Pengelola skema warna terminal dan tata gaya tampilan. Menyediakan
lapisan abstraksi di atas kode ANSI mentah agar komponen UI lain
(tables.py, prompts.py, spinners.py) tidak perlu tahu kode escape-nya.
"""

import sys

from config.settings import THEMES, DEFAULT_THEME


def _is_tty() -> bool:
    """Deteksi apakah output diarahkan ke terminal interaktif (TTY)."""
    try:
        return sys.stdout.isatty()
    except AttributeError:
        return False


def get_theme(name: str = DEFAULT_THEME) -> dict:
    """
    Mengembalikan dictionary warna sesuai nama tema.
    Jika output bukan TTY (misal: dipipe ke file), otomatis fallback
    ke tema 'mono' agar tidak mencetak kode ANSI mentah.
    """
    if not _is_tty():
        return THEMES["mono"]
    return THEMES.get(name, THEMES[DEFAULT_THEME])


def colorize(text: str, role: str, theme: dict) -> str:
    """Membungkus teks dengan kode warna sesuai peran ('primary', 'error', dst)."""
    color = theme.get(role, "")
    reset = theme.get("reset", "")
    return f"{color}{text}{reset}"
