# Modul 02 — Modular Algorithm Design

Modul pembelajaran yang berfokus pada penerapan **Modular Architecture**
dan prinsip-prinsip software engineering modern seperti **Loose Coupling**
(keterikatan rendah) dan **High Cohesion** (kepadatan tinggi).

Tujuan utamanya adalah merancang algoritma yang terisolasi ke dalam
komponen-komponen mandiri (*pluggable modules*) sehingga aplikasi mudah
dikembangkan, diuji secara terpisah, dan ditambahkan fitur baru tanpa
merusak kode yang sudah ada.

## Struktur Proyek

```
modul_02_modular_algorithm_design/
├── config/                          # Konfigurasi aplikasi & pendaftaran modul
│   ├── __init__.py
│   ├── settings.py                  # Konfigurasi sistem global
│   └── module_registry.py           # Registry untuk mendaftarkan modul secara dinamis
│
├── docs/                            # Dokumentasi Desain Modular
│   ├── modular_architecture.md      # Diagram alur antar-modul & dependensi
│   └── api_contracts.md             # Kontrak interface (kontrak input/output antar modul)
│
├── src/                             # Core Application Source Code
│   ├── __init__.py
│   │
│   ├── interfaces/                  # 1. Layer Abstract Base Classes (Kontrak Modul)
│   │   ├── __init__.py
│   │   ├── base_module.py           # Interface standar yang WAJIB diimplementasi tiap modul
│   │   ├── base_algorithm.py        # Template dasar untuk semua algoritma
│   │   └── base_handler.py          # Contract handler untuk pemrosesan data
│   │
│   ├── modules/                     # 2. Modul-Modul Independen (Plug-and-Play)
│   │   ├── __init__.py
│   │   ├── analytics/               # Modul Analisis Data
│   │   │   ├── __init__.py
│   │   │   ├── analyzer.py
│   │   │   └── metrics.py
│   │   ├── transformation/          # Modul Transformasi Data
│   │   │   ├── __init__.py
│   │   │   ├── cleansers.py
│   │   │   └── converters.py
│   │   └── validation/              # Modul Validasi
│   │       ├── __init__.py
│   │       └── rules.py
│   │
│   ├── core/                        # 3. Orchestrator & Dependency Injection Engine
│   │   ├── __init__.py
│   │   ├── bus.py                   # Event Bus / Message Pass antar modul
│   │   ├── dispatcher.py            # Pengatur urutan eksekusi modul
│   │   └── container.py             # Dependency Injection Container
│   │
│   └── utils/                       # 4. Shared Utilities (Helper terisolasi)
│       ├── __init__.py
│       ├── helpers.py
│       └── error_handlers.py
│
├── tests/                           # Pengujian Modularisasi
│   ├── __init__.py
│   ├── unit_modules/                # Test tiap modul secara terisolasi (Mocking)
│   │   ├── test_analytics_module.py
│   │   └── test_validation_module.py
│   └── integration_bus/             # Test komunikasi antar-modul lewat Event Bus
│       └── test_module_dispatch.py
│
├── .env.example
├── main.py                          # Entry Point (Inisialisasi & Run Dynamic Modules)
├── pyproject.toml
└── README.md
```

## Deskripsi Arsitektur & Peran Komponen

### 1. Configuration & Contract Registry (`config/`, `docs/`)
- `module_registry.py` — pendaftar modul dinamis (*Dynamic Module Registry*)
  yang mencatat dan memuat modul mana saja yang aktif saat runtime.
- `api_contracts.md` & `modular_architecture.md` — dokumen spesifikasi
  kontrak antarmuka yang menetapkan aturan komunikasi antar-modul dan
  diagram dependensi sistem.

### 2. Abstract Interface Layer (`src/interfaces/`)
- `base_module.py` & `base_algorithm.py` — Abstract Base Class (ABC) yang
  mendefinisikan standar method wajib (`initialize()`, `execute()`,
  `cleanup()`) untuk seluruh modul turunan.
- `base_handler.py` — kontrak standar untuk komponen penanganan data agar
  memiliki signature fungsi yang seragam.

### 3. Independent Functional Modules (`src/modules/`)
- `analytics/` — modul terisolasi untuk perhitungan metrik dan analisis
  statistik data.
- `transformation/` — modul mandiri untuk pembersihan (*cleansing*) dan
  konversi format data.
- `validation/` — modul independen berisi aturan-aturan validasi
  (*validation rules*) yang bisa dipasang atau dilepas secara fleksibel.

### 4. Core Orchestration Layer (`src/core/`)
- `bus.py` (Event Bus) — memfasilitasi komunikasi antar-modul tanpa perlu
  saling mengimpor (*no direct dependency*).
- `container.py` (Dependency Injection Container) — mengatur inisialisasi
  dan penyuntikan dependensi ke setiap modul secara otomatis.
- `dispatcher.py` — mengatur urutan alur eksekusi antar-modul berdasarkan
  konfigurasi pendaftaran.

### 5. Testing & Isolation Suite (`tests/`)
- `unit_modules/` — pengujian unit terisolasi menggunakan Mocking/Stubbing
  untuk menguji logika internal satu modul tanpa menjalankan modul lainnya.
- `integration_bus/` — pengujian integrasi untuk memverifikasi kelancaran
  pertukaran pesan dan data antar-modul melalui Event Bus.

## Cara Menjalankan

1. Salin `.env.example` menjadi `.env` lalu sesuaikan nilainya.
2. (Opsional) buat virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependensi:
   ```bash
   pip install -e ".[dev]"
   ```
4. Jalankan aplikasi:
   ```bash
   python main.py
   ```
5. Jalankan seluruh test:
   ```bash
   pytest
   ```

## Menambahkan Modul Baru

1. Buat folder baru di `src/modules/<nama_modul>/`.
2. Implementasikan kelas yang mewarisi `BaseModule`
   (`src/interfaces/base_module.py`).
3. Daftarkan modul di `config/module_registry.py`:
   ```python
   registry.register("nama_modul", "src.modules.nama_modul.file.KelasModul")
   ```
4. Tambahkan pengujian unit di `tests/unit_modules/`.
5. Perbarui `docs/api_contracts.md` dengan kontrak input/output modul baru.

Tidak ada kode di `src/core/` atau modul lain yang perlu diubah — inilah
inti dari desain *pluggable module*.
