# Modul 09 — Architecting Robust Software

**Fault-Tolerant CLI Engine & Resilience Inspector**

Modul ini membangun arsitektur perangkat lunak yang tahan terhadap kegagalan
(*resilience & robustness*), menerapkan hirarki exception kustom, dan
mencegah aplikasi crash mendadak melalui mekanisme pemulihan otomatis
(*self-healing*) serta *Graceful Degradation*.

## Fitur Utama

- **Custom Exception Hierarchy** — `ValidationError` & `ExecutionError`
  turunan dari `AppException`, masing-masing membawa kode error standar.
- **Circuit Breaker** — mencegah efek domino ketika komponen gagal berulang.
- **Retry Handler** — percobaan ulang otomatis dengan *exponential backoff*.
- **Fallback Manager** — alur/data cadangan saat komponen utama gagal.
- **Health Check** — verifikasi disk space, izin tulis, dan dependensi
  sebelum eksekusi utama berjalan.
- **Crash Reporter** — mencatat laporan kegagalan terstruktur (JSON) untuk
  audit dan debugging.
- **Graceful CLI UX** — pesan error yang ramah serta prompt pemulihan
  interaktif bagi pengguna.

## Struktur Proyek

```
modul_09_architecting_robust_software/
├── config/          # Threshold retry/timeout/fallback & kode error
├── docs/            # Fault tolerance matrix & exception hierarchy
├── src/
│   ├── exceptions/  # Hirarki custom exception
│   ├── resilience/  # Circuit breaker, retry, fallback
│   ├── monitors/    # Health check, crash reporter
│   └── ui/          # Error presenter, recovery prompt
├── tests/           # Chaos engineering & fault injection tests
└── main.py          # Entry point (Robust CLI Orchestrator)
```

## Instalasi

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
```

## Menjalankan Aplikasi

```bash
python main.py
```

Setiap kali dijalankan, layanan simulasi (`unstable_service_call`) memiliki
peluang gagal secara acak untuk mendemonstrasikan alur:
health check → circuit breaker → retry → fallback → crash report (jika perlu).

## Menjalankan Tes

```bash
pytest
```

Mencakup pengujian *fault injection*, *circuit breaker state transitions*,
dan verifikasi *graceful recovery* setelah error tertangani.

## Konfigurasi

Semua parameter (threshold retry, timeout, circuit breaker, dsb.) dapat
diatur lewat environment variable — lihat `.env.example` dan
`config/settings.py`.
