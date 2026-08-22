# Advanced IPO Problem Analysis — CLI System

Sistem CLI berskala besar dengan arsitektur **Decoupled Layer (IPO)**:
pemisahan tegas antara Input, Process, dan Output agar logika bisnis
tidak terikat pada mekanisme masukan pengguna maupun format tampilan.

## Arsitektur

```
config/            → Konfigurasi & konstanta global
docs/               → Spesifikasi & user stories
src/domain/         → Entity murni & custom exceptions
src/input_layer/    → Validasi, parsing, dan pembacaan CLI
src/process_layer/  → Engine bisnis & pipeline transformasi
src/output_layer/   → Formatter, presenter, dan exporter
src/infrastructure/ → Logger, metrics, dan file storage
tests/              → Unit test & integration test
```

## Instalasi

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
cp .env.example .env
```

## Penggunaan

**Mode CLI flag (non-interaktif):**
```bash
python main.py --values "10,2,8,4,99" --format table
```

**Mode interaktif:**
```bash
python main.py
```

**Ekspor hasil ke berkas:**
```bash
python main.py --values "1,2,3,4,5" --export output/hasil.csv
```

**Format output yang didukung:** `table` (default), `json`, `plain`

## Menjalankan Test

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## Alur Data (IPO Pipeline)

```
RawInput (CLI/Interaktif)
    → Validasi (input_layer/validators.py)
    → Parsing (input_layer/parsers.py)
    → Pipeline: filter_outliers → sort_values → normalize_values
    → PipelineReport
    → Format (table/json/plain)
    → Tampilkan di terminal / Ekspor ke file (.csv/.json/.log)
```

## Konvensi Kode Galat

| Prefiks | Layer | Contoh |
|---|---|---|
| `E1xxx` | Input | `E1002` — nilai di luar rentang |
| `E2xxx` | Process | `E2002` — pipeline terhenti |
| `E3xxx` | Output | `E3001` — gagal ekspor berkas |

Lihat `config/constants.py` untuk daftar lengkap.

## Lisensi
Materi pembelajaran internal — Modul 01, ALGO2: Advanced IPO Problem Analysis.
