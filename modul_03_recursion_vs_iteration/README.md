# Modul 03: Rekursi versus Iterasi

## Ringkasan

Modul ini berfokus pada analisis komparatif dan pengujian performa antara
dua paradigma pemrosesan data utama: **Rekursi** (call stack-based) dan
**Iterasi** (loop-based). Tujuan utamanya adalah membangun *execution &
benchmarking engine* yang mengeksekusi problem matematika/struktur data
kompleks secara paralel, mengukur penggunaan memori (stack depth vs heap
allocation), serta menganalisis efisiensi waktu eksekusi secara presisi
hingga tingkat mikrodetik (microsecond).

## Instalasi

```bash
pip install -e .
# atau untuk pengembangan (termasuk pytest)
pip install -e ".[dev]"
```

## Menjalankan Benchmark

```bash
python main.py
```

## Menjalankan Test

```bash
pytest
```

## Struktur Proyek

```
modul_03_recursion_vs_iteration/
├── config/                          # Konfigurasi sistem & batas eksekusi
│   ├── settings.py                  # Max recursion depth limit & timeout settings
│   └── constants.py                 # Parameter pengujian (data sizes, iteration limits)
│
├── docs/                            # Dokumentasi Analisis Komparatif
│   ├── memory_stack_analysis.md     # Penjelasan penggunaan Call Stack vs Loop Memory
│   └── algorithm_benchmarks.md      # Catatan teori Big-O Time & Space Complexity
│
├── src/
│   ├── algorithms/
│   │   ├── recursive/               # fibonacci.py, tree_traversal.py, tail_recursion.py
│   │   └── iterative/                # fibonacci.py, tree_traversal.py
│   ├── engine/                      # runner.py, profiler.py, timer.py
│   ├── formatters/                  # table_presenter.py, chart_generator.py
│   └── utils/                       # stack_overflow_guard.py
│
├── tests/                           # test_recursive_correctness.py, test_iterative_correctness.py,
│                                     # test_result_parity.py
│
├── .env.example
├── main.py                          # Entry Point (CLI Runner & Interactive Benchmark)
├── pyproject.toml
└── README.md
```

## Komponen Utama

1. **Configuration & Benchmark Parameters** (`config/`, `docs/`) — batas
   kedalaman rekursi, timeout, skala data uji, serta dokumen teori.
2. **Dual Algorithm Implementation Layer** (`src/algorithms/`) —
   implementasi paralel rekursif dan iteratif dengan signature identik.
3. **Execution & Benchmarking Engine** (`src/engine/`) — menjalankan kedua
   versi berdampingan dan mengukur waktu serta memori.
4. **Visualization & Output Layer** (`src/formatters/`) — tabel dan grafik
   ASCII di terminal.
5. **Safety Guard & Utilities** (`src/utils/`, `tests/`) — proteksi
   `RecursionError` dan pengujian paritas hasil.
