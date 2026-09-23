"""
context.py
Pengelola status konteks aplikasi: tema aktif, mode verbose,
serta penyimpanan konfigurasi in-memory (session-level).

AppContext diteruskan ke setiap command handler agar mereka bisa
mengakses state bersama dan memanggil presenter tanpa saling
mengimpor modul UI secara langsung.
"""

from typing import Dict

from src.cli.theme import get_theme, colorize


class AppContext:
    def __init__(self):
        self.theme: dict = get_theme()
        self.verbose: bool = False
        self.config: Dict[str, str] = {}

    # --- Presenter helpers: dipakai oleh command handlers ---
    def presenter_success(self, message: str) -> None:
        print(colorize(f"✔ {message}", "success", self.theme))

    def presenter_error(self, message: str) -> None:
        print(colorize(f"✘ {message}", "error", self.theme))

    def presenter_warning(self, message: str) -> None:
        print(colorize(f"⚠ {message}", "warning", self.theme))

    def log(self, message: str) -> None:
        """Log verbose -- hanya tercetak jika --verbose diaktifkan."""
        if self.verbose:
            print(colorize(f"[log] {message}", "muted", self.theme))
