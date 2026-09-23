"""
settings.py
Memuat versi aplikasi, tema warna terminal default, dan nilai bawaan (defaults)
untuk seluruh sistem CLI Architecture Blueprint.
"""

import os

# --- Metadata Aplikasi ---
APP_NAME = "cli-arch-blueprint"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "CLI Architecture Framework & Command Dispatcher Engine"

# --- Tema Warna Terminal (ANSI) ---
DEFAULT_THEME = os.environ.get("CLI_THEME", "default")

THEMES = {
    "default": {
        "primary": "\033[36m",    # Cyan
        "success": "\033[32m",    # Green
        "warning": "\033[33m",    # Yellow
        "error": "\033[31m",      # Red
        "muted": "\033[90m",      # Grey
        "reset": "\033[0m",
    },
    "mono": {
        "primary": "",
        "success": "",
        "warning": "",
        "error": "",
        "muted": "",
        "reset": "",
    },
}

# --- Nilai Bawaan (Defaults) ---
DEFAULT_OUTPUT_FORMAT = "table"   # table | json | plain
DEFAULT_PAGE_SIZE = 20
DEFAULT_TIMEOUT_SECONDS = 30

# --- Environment Overrides ---
DEBUG = os.environ.get("CLI_DEBUG", "false").lower() == "true"
