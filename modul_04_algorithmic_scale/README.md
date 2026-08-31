# Modul 04 — Algorithmic Scale

Stress testing engine untuk menganalisis **skalabilitas algoritma**
dan efisiensi pemrosesan data masif menggunakan kerangka kerja
**Big-O Notation**: `O(1)`, `O(log N)`, `O(N)`, `O(N log N)`, `O(N^2)`.

Engine ini menguji daya tahan kode dari skala data kecil hingga
skala raksasa (hingga 1.000.000+ sampel), sekaligus mendeteksi titik
kemacetan (**bottleneck**) dan lonjakan penggunaan memori secara presisi.

## Fitur Utama

- **Dataset scale configuration** — lima tingkatan skala (Tiny, Small,
  Medium, Large, Huge) dengan ambang batas timeout & RAM yang dapat
  dikonfigurasi.
- **Synthetic data generator** — pembuat data angka/string acak,
  termasuk skenario Best/Average/Worst Case.
- **Algorithm target library** — contoh algoritma untuk tiap kelas
  Big-O sebagai benchmark.
- **Scalability profiler** — pengukuran waktu eksekusi & puncak
  memori secara presisi.
- **Complexity analyzer** — estimasi otomatis kelas Big-O dari data
  hasil profiling.
- **Terminal visualizer & report exporter** — grafik ASCII di CLI
  serta ekspor laporan ke Markdown/JSON.

## Struktur Proyek

```
modul_04_algorithmic_scale/
├── config/                 # Konfigurasi skala & threshold
├── docs/                   # Dokumentasi teori & metodologi
├── src/
│   ├── datasets/            # Generator data sintetis
│   ├── algorithms/          # Library algoritma target (O(1)..O(N^2))
│   ├── profiler/             # Time/memory profiler & complexity analyzer
│   └── visualizers/          # ASCII plotter & report exporter
├── tests/                    # Unit test
├── .env.example
├── main.py                    # Entry point CLI interaktif
├── pyproject.toml
└── README.md
```

## Instalasi

Proyek ini hanya menggunakan pustaka standar Python (tidak ada
dependensi eksternal wajib), sehingga cukup memastikan Python >= 3.9
terpasang.

```bash
# (Opsional) buat virtual environment
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# (Opsional) salin file environment
cp .env.example .env
```

Untuk menjalankan unit test, pasang `pytest` (opsional):

```bash
pip install pytest
```

## Cara Menjalankan

Jalankan CLI interaktif:

```bash
python3 main.py
```

Anda akan diminta memilih:
1. Algoritma target yang ingin diuji (mis. `bubble_sort`, `merge_sort`,
   `binary_search`, dll).
2. Skala maksimum pengujian (Tiny s.d. Huge).

Engine akan menjalankan pengujian bertahap dari skala terkecil hingga
skala yang dipilih, menampilkan grafik pertumbuhan waktu di terminal,
estimasi kelas Big-O, dan menawarkan opsi ekspor laporan.

## Menjalankan Unit Test

```bash
python3 -m pytest tests/ -v
# atau tanpa pytest:
python3 -m unittest discover -s tests -v
```

## Konfigurasi

Semua ambang batas dapat diubah lewat environment variable (lihat
`.env.example`) atau langsung di `config/settings.py`:

| Variabel                    | Default | Keterangan                                  |
|------------------------------|---------|-----------------------------------------------|
| `EXECUTION_TIMEOUT_SECONDS`  | 10.0    | Batas waktu eksekusi per pengujian (detik)     |
| `MAX_MEMORY_MB`               | 512.0   | Batas puncak penggunaan memori (MB)            |
| `REPEATS_PER_MEASUREMENT`     | 3       | Jumlah pengulangan pengukuran waktu            |
| `RANDOM_SEED`                  | 42      | Seed data sintetis agar hasil reproducible     |
| `REPORT_OUTPUT_DIR`            | reports | Direktori output laporan                        |
| `ASCII_PLOT_WIDTH/HEIGHT`      | 60 / 15 | Ukuran grafik ASCII di terminal                 |

## Dokumentasi Tambahan

- [`docs/complexity_theory.md`](docs/complexity_theory.md) — teori
  kurva pertumbuhan Big-O dan metode estimasi otomatis.
- [`docs/stress_testing_guides.md`](docs/stress_testing_guides.md) —
  metodologi lengkap alur stress testing & deteksi bottleneck.

## Lisensi

Proyek ini dibuat untuk keperluan pembelajaran/edukasi.
