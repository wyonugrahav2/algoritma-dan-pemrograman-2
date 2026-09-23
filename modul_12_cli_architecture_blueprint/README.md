# Modul 12 — CLI Architecture Blueprint

CLI Architecture Framework & Command Dispatcher Engine yang memisahkan
tampilan antarmuka terminal (Presentation Layer) dari logika bisnis
utama (Application Core), mengelola sistem perintah bersarang
(subcommands, options, & flags), serta menyediakan komponen visual
terminal yang modern.

## Struktur Proyek

```
modul_12_cli_architecture_blueprint/
├── config/                # Konfigurasi sistem CLI & branding
├── docs/                  # Dokumentasi arsitektur & UX
├── src/
│   ├── cli/               # Parser, Router, Theme (Presentation Layer)
│   ├── commands/          # Handler tiap subcommand (search, process, config)
│   ├── components/        # Tabel, prompt, spinner (UI Component Library)
│   └── core/              # Context & Controller (Application Core Bridge)
├── tests/                 # Pengujian arsitektur CLI
├── main.py                # Entry point
└── pyproject.toml
```

## Instalasi

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
cp .env.example .env
```

Tidak ada dependensi eksternal wajib — proyek ini murni menggunakan
pustaka standar Python (`argparse`, `threading`, dll).

## Penggunaan

```bash
# Menampilkan bantuan & daftar perintah
python3 main.py --help

# Mencari data
python3 main.py search sort --format table --limit 5

# Memproses berkas (mode simulasi)
python3 main.py process data.txt --dry-run

# Mengelola konfigurasi
python3 main.py config set theme dark
python3 main.py config get theme
python3 main.py config list

# Mengganti tema tampilan & mode verbose
python3 main.py --theme mono --verbose search binary
```

## Menjalankan Test

```bash
python3 -m pytest tests/ -v
# atau tanpa pytest:
python3 -m unittest discover -s tests
```

## Prinsip Arsitektur

- **Separation of Concerns**: `src/cli` (presentation) tidak pernah
  memanggil logika bisnis secara langsung — semuanya lewat `BaseCommand`
  dan, jika perlu, `AppController`.
- **Extensible by Registry**: menambah subcommand baru cukup dengan
  membuat class turunan `BaseCommand` dan mendaftarkannya di
  `config/commands_registry.py`, tanpa menyentuh `router.py`.
- **Konsisten & Ramah Pengguna**: seluruh command mewarisi penanganan
  error dan gaya output yang seragam dari `BaseCommand` dan `AppContext`.
