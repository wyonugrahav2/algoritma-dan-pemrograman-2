# Modul 05: Search Algorithm Anatomy

CLI Search Engine & Search Space Inspector yang tidak hanya mencari
keberadaan data, tetapi juga membedah **anatomi internal** proses
pencarian: penyusutan ruang pencarian (search space reduction),
pergerakan pointer (pointer tracking), dan jumlah operasi perbandingan
(comparison count) secara real-time.

## Ringkasan Modul

Modul ini menganalisis lima strategi pencarian:

| Algoritma            | Kompleksitas rata-rata | Prasyarat Data       |
|------------------------|--------------------------|------------------------|
| Linear Search          | O(N)                     | Tidak perlu terurut    |
| Binary Search           | O(log N)                 | Terurut                |
| Interpolation Search    | O(log log N)             | Terurut & uniform      |
| Exponential Search      | O(log N)                 | Terurut                |
| Hash Lookup             | O(1)                     | Ter-index (hash map)   |

Detail teori ada di `docs/search_space_reduction.md` dan
`docs/data_distribution_impact.md`.

## Struktur Proyek

```
modul_05_search_algorithm_anatomy/
├── config/                # Strategy Registry & threshold pencarian
├── docs/                  # Dokumentasi teori anatomi pencarian
├── src/
│   ├── indexer/            # Load, sort, dan index data
│   ├── algorithms/         # Implementasi 5 algoritma pencarian
│   ├── analytics/          # Step counter, pointer tracker, profiler
│   └── ui/                 # Query parser, presenter, visualizer CLI
├── tests/                  # Correctness, edge cases, index integrity
├── main.py                 # Entry point CLI
├── pyproject.toml
└── .env.example
```

## Instalasi

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
```

## Penggunaan CLI

Pencarian tunggal dengan data contoh bawaan (algoritma direkomendasikan
otomatis berdasarkan karakteristik data):

```bash
python main.py --target 71
```

Menentukan algoritma secara eksplisit:

```bash
python main.py --target 71 --algo interpolation
```

Menampilkan animasi pergerakan pointer di terminal:

```bash
python main.py --target 71 --algo binary --visualize
```

Menjalankan seluruh algoritma sekaligus untuk perbandingan performa
(jumlah perbandingan, latensi, dan memori):

```bash
python main.py --target 71 --benchmark
```

Menggunakan sumber data eksternal:

```bash
python main.py --source data/dataset.json --target 250
python main.py --source data/dataset.csv --column price --target 19.99
```

## Menjalankan Test

```bash
pytest -v
```

Test dibagi menjadi tiga fokus utama:

- `test_search_correctness.py` — memastikan setiap algoritma menemukan
  nilai target dengan benar pada dataset standar.
- `test_edge_cases.py` — menguji kasus batas (data kosong, elemen di
  ujung, target tidak ada, duplikasi nilai).
- `test_index_integrity.py` — memvalidasi integritas Hash Index dan
  Inverted Index yang dibangun `src/indexer/index_builder.py`.

## Konfigurasi

Semua ambang batas (threshold) dan parameter indeks diatur terpusat di
`config/settings.py`, sementara pemetaan strategi ke handler algoritma
(Strategy Pattern) ada di `config/search_strategies.py`.
