# Modul 06 — Basic Sorting Blueprints

CLI Data Sorting Engine & Mutation Visualizer yang membedah efisiensi
internal 5 algoritma pengurutan klasik: **Bubble Sort**, **Selection Sort**,
**Insertion Sort**, **Merge Sort**, dan **Quick Sort**.

## Fitur

- Implementasi murni tiap algoritma di `src/algorithms/`
- Telemetry: penghitung swap, comparison, dan pelacak memori (`src/metrics/`)
- Generator data uji: random, nearly sorted, reversed (`src/data_prep/`)
- Animasi bar chart ASCII di terminal (`src/ui/bar_chart_renderer.py`)
- Registry algoritma via Strategy Pattern (`config/sort_strategies.py`)
- Test suite lengkap: correctness, stability, edge cases (`tests/`)

## Instalasi

```bash
cd modul_06_basic_sorting_blueprints
cp .env.example .env      # opsional, sesuaikan konfigurasi
pip install -e ".[dev]"   # install pytest untuk testing
```

## Menjalankan

Jalankan semua algoritma sekaligus (mode perbandingan):

```bash
python main.py --size 20 --case random
```

Jalankan satu algoritma tertentu:

```bash
python main.py --algorithm quick --size 30 --case reversed
```

Dengan animasi visual bar chart:

```bash
python main.py --algorithm insertion --size 25 --case nearly_sorted --animate
```

Urutkan secara descending:

```bash
python main.py --algorithm bubble --descending
```

### Opsi CLI

| Flag              | Alias | Pilihan                                              | Default  |
|-------------------|-------|-------------------------------------------------------|----------|
| `--algorithm`      | `-a`  | bubble, selection, insertion, merge, quick, all       | all      |
| `--size`           | `-n`  | integer                                                | 15       |
| `--case`           | `-c`  | random, nearly_sorted, reversed                        | random   |
| `--animate`        |       | flag                                                    | False    |
| `--descending`     |       | flag                                                    | False    |

## Menjalankan Test

```bash
pytest -v
```

## Dokumentasi Tambahan

- [`docs/sorting_stability.md`](docs/sorting_stability.md) — konsep stability & klasifikasi tiap algoritma
- [`docs/space_complexity_sorting.md`](docs/space_complexity_sorting.md) — analisis In-Place vs Auxiliary Space

## Struktur Proyek

```
modul_06_basic_sorting_blueprints/
├── config/          # Konfigurasi & registry strategi sorting
├── docs/            # Dokumentasi teori
├── src/
│   ├── data_prep/   # Generator data & snapshot state
│   ├── algorithms/  # 5 implementasi sorting
│   ├── metrics/     # Swap/compare counter & memory tracker
│   └── ui/          # Renderer animasi, presenter, cli args
├── tests/           # Unit test
├── main.py          # Entry point CLI
└── pyproject.toml
```
