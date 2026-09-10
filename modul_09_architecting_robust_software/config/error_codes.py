"""Standarisasi kode error sistem.

Setiap kode error mengikuti format: <KATEGORI>-<NOMOR>
sehingga mudah dilacak pada log audit maupun laporan crash.
"""

# --- Validation errors (1xx) ---
ERR_INVALID_INPUT = "VAL-100"
ERR_OUT_OF_RANGE = "VAL-101"
ERR_MISSING_FIELD = "VAL-102"

# --- Execution errors (2xx) ---
ERR_TIMEOUT = "EXE-200"
ERR_RESOURCE_UNAVAILABLE = "EXE-201"
ERR_UNEXPECTED_FAILURE = "EXE-202"

# --- Resilience errors (3xx) ---
ERR_CIRCUIT_OPEN = "RES-300"
ERR_RETRY_EXHAUSTED = "RES-301"
ERR_FALLBACK_FAILED = "RES-302"

# --- System/health errors (4xx) ---
ERR_HEALTH_CHECK_FAILED = "SYS-400"
ERR_DISK_SPACE_LOW = "SYS-401"

ERROR_MESSAGES = {
    ERR_INVALID_INPUT: "Input yang diberikan tidak valid.",
    ERR_OUT_OF_RANGE: "Nilai berada di luar batas yang diizinkan.",
    ERR_MISSING_FIELD: "Terdapat field wajib yang belum diisi.",
    ERR_TIMEOUT: "Operasi melebihi batas waktu yang ditentukan.",
    ERR_RESOURCE_UNAVAILABLE: "Sumber daya yang dibutuhkan tidak tersedia.",
    ERR_UNEXPECTED_FAILURE: "Terjadi kegagalan yang tidak terduga.",
    ERR_CIRCUIT_OPEN: "Circuit breaker sedang terbuka, permintaan ditolak sementara.",
    ERR_RETRY_EXHAUSTED: "Seluruh percobaan ulang telah habis.",
    ERR_FALLBACK_FAILED: "Mekanisme fallback juga gagal dieksekusi.",
    ERR_HEALTH_CHECK_FAILED: "Pemeriksaan kesehatan sistem gagal.",
    ERR_DISK_SPACE_LOW: "Ruang penyimpanan disk tersisa terlalu sedikit.",
}
