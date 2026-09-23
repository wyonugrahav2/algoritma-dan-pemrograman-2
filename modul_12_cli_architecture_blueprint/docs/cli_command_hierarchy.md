# CLI Command Hierarchy

Dokumen ini memetakan pohon navigasi perintah terminal untuk
**CLI Architecture Blueprint**.

```
cli-arch-blueprint
├── search <query>              # Handler: search_cmd.py
│   ├── --format table|json     # Format output hasil pencarian
│   └── --limit <n>             # Batas jumlah hasil
│
├── process <input>             # Handler: process_cmd.py
│   ├── --output <path>         # Lokasi berkas hasil proses
│   └── --dry-run               # Simulasi tanpa menulis berkas
│
├── config                      # Handler: config_cmd.py
│   ├── get <key>                # Membaca nilai konfigurasi
│   ├── set <key> <value>        # Mengubah nilai konfigurasi
│   └── list                     # Menampilkan seluruh konfigurasi
│
└── --help / -h                 # Bantuan global (setiap level)
```

## Prinsip Desain

1. **Satu command = satu handler class** yang mewarisi `BaseCommand`.
2. Setiap subcommand wajib mengekspos `--help` yang konsisten
   (diwariskan otomatis dari `BaseCommand`).
3. Flag global (`--verbose`, `--theme`) berlaku untuk semua subcommand
   dan ditangani oleh `parser.py` sebelum command spesifik dieksekusi.
4. Routing perintah ke handler bersifat dinamis melalui
   `commands_registry.py`, sehingga menambah perintah baru tidak
   memerlukan perubahan pada `router.py`.
