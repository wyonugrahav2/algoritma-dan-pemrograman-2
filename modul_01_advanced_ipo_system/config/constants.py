"""
constants.py
Konstanta global untuk sistem IPO: kode error, batas nilai, dan format standar.
Tidak ada nilai bisnis yang boleh di-hardcode di luar file ini.
"""

from enum import Enum


class ErrorCode(Enum):
    """Kode galat kustom untuk keseluruhan sistem."""
    INVALID_INPUT_TYPE = "E1001"
    VALUE_OUT_OF_RANGE = "E1002"
    EMPTY_INPUT = "E1003"
    PARSING_FAILED = "E1004"
    PROCESS_FAILURE = "E2001"
    PIPELINE_BROKEN = "E2002"
    EXPORT_FAILED = "E3001"
    UNSUPPORTED_FORMAT = "E3002"


# Batas ambang batas (threshold) default untuk validasi numerik
MIN_VALUE_THRESHOLD = -1_000_000
MAX_VALUE_THRESHOLD = 1_000_000

# Format output yang didukung oleh Output Layer
SUPPORTED_EXPORT_FORMATS = ("csv", "json", "log", "txt")

# Format tampilan default untuk presenter CLI
DEFAULT_DISPLAY_FORMAT = "table"

# Jumlah maksimum baris yang ditampilkan di terminal sebelum dipotong (truncate)
MAX_TERMINAL_ROWS = 50

# Standar penamaan file log
LOG_FILE_NAME = "ipo_system.log"

# Versi skema data internal (untuk kompatibilitas antar modul)
DATA_SCHEMA_VERSION = "1.0.0"
