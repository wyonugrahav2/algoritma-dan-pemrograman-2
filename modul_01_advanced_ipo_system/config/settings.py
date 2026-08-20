"""
settings.py
Memuat variabel lingkungan (.env) dan menyediakan objek konfigurasi terpusat.
Tidak ada modul lain yang boleh membaca os.environ secara langsung.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path

try:
    # python-dotenv bersifat opsional; sistem tetap berjalan tanpa file .env
    from dotenv import load_dotenv
    _HAS_DOTENV = True
except ImportError:
    _HAS_DOTENV = False


BASE_DIR = Path(__file__).resolve().parent.parent


def _load_env_file() -> None:
    """Memuat file .env dari root proyek jika tersedia."""
    env_path = BASE_DIR / ".env"
    if _HAS_DOTENV and env_path.exists():
        load_dotenv(dotenv_path=env_path)


def _get_bool(key: str, default: bool) -> bool:
    val = os.getenv(key)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


def _get_int(key: str, default: int) -> int:
    val = os.getenv(key)
    if val is None:
        return default
    try:
        return int(val)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    """Objek konfigurasi terpusat untuk seluruh sistem."""

    app_name: str = "Advanced IPO CLI System"
    debug_mode: bool = False
    log_level: str = "INFO"
    log_dir: Path = field(default_factory=lambda: BASE_DIR / "logs")
    output_dir: Path = field(default_factory=lambda: BASE_DIR / "output")
    default_export_format: str = "json"
    max_input_length: int = 500
    metrics_enabled: bool = True


def load_settings() -> Settings:
    """Factory function untuk membangun objek Settings dari environment."""
    _load_env_file()
    return Settings(
        app_name=os.getenv("APP_NAME", "Advanced IPO CLI System"),
        debug_mode=_get_bool("DEBUG_MODE", False),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        log_dir=Path(os.getenv("LOG_DIR", str(BASE_DIR / "logs"))),
        output_dir=Path(os.getenv("OUTPUT_DIR", str(BASE_DIR / "output"))),
        default_export_format=os.getenv("DEFAULT_EXPORT_FORMAT", "json"),
        max_input_length=_get_int("MAX_INPUT_LENGTH", 500),
        metrics_enabled=_get_bool("METRICS_ENABLED", True),
    )


# Instance singleton yang dapat diimpor langsung oleh modul lain
settings = load_settings()
