# Fault Tolerance Matrix

Dokumen ini memetakan skenario kegagalan yang mungkin terjadi pada sistem
beserta mekanisme pemulihan yang diterapkan.

| Skenario Kegagalan                      | Deteksi                     | Strategi Pemulihan                     | Komponen Terkait          |
|------------------------------------------|------------------------------|------------------------------------------|----------------------------|
| Layanan eksternal timeout sesekali       | Exception saat pemanggilan   | Retry dengan exponential backoff        | `retry_handler.py`         |
| Layanan eksternal gagal berulang kali    | Gagal beruntun >= threshold  | Circuit breaker OPEN, tolak sementara   | `circuit_breaker.py`       |
| Circuit breaker OPEN / retry habis       | `CircuitOpenError` / `RetryExhaustedError` | Gunakan data/alur cadangan (fallback) | `fallback_manager.py`      |
| Input pengguna tidak valid               | Validasi awal                | Tolak dengan pesan jelas, tanpa crash   | `validation_errors.py`     |
| Sumber daya sistem tidak cukup           | Health check sebelum eksekusi| Peringatkan pengguna, mode hati-hati    | `health_check.py`          |
| Kegagalan tak terduga (unhandled)        | Try/except di titik akhir    | Catat crash report, tawarkan pemulihan  | `crash_reporter.py`, `recovery_prompt.py` |

## Prinsip Utama

1. **Fail fast, recover gracefully** — kegagalan dideteksi secepat mungkin,
   namun pemulihan selalu diarahkan agar pengguna tidak mengalami crash mentah.
2. **Isolasi kegagalan** — circuit breaker mencegah efek domino ke komponen lain.
3. **Selalu ada jalan keluar** — setiap kegagalan memiliki fallback atau opsi
   pemulihan interaktif, bukan dead-end.
