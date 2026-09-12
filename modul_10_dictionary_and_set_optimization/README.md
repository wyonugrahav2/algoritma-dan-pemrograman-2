# Modul 10 — Dictionary and Set Optimization

Analisis dan optimasi struktur data berbasis pemetaan Hash (Dictionary &
Set): pencarian data berkecepatan O(1), penanganan bentrokan hash (Hash
Collision), dan minimalisasi overhead memori pada himpunan data unik
berskala masif.

## Fitur Utama

- **Custom Hash Table** dari nol, mendukung strategi *chaining* dan
  *open addressing* (linear probing) dengan rehashing otomatis.
- **Bloom Filter**: probabilistic set untuk membership testing hemat memori.
- **LRU Cache** O(1) berbasis Hash Map + Doubly Linked List.
- **Deduplicator**, **Key Compressor** (string interning), dan
  **Set Operations** (union/intersection/difference/Jaccard).
- **Collision Tracker** & **Lookup Benchmarker** untuk analisis performa.
- **Interactive CLI** (`store_cli.py`) untuk mencoba semua fitur langsung
  dari terminal.

## Struktur Proyek

```
modul_10_dictionary_and_set_optimization/
├── config/                # Konfigurasi Hash Table & Memory Pool
│   ├── settings.py
│   └── hash_functions.py
├── docs/                  # Dokumentasi Teori Hashing & Memori
│   ├── hash_collision_strategies.md
│   └── memory_overhead_analysis.md
├── src/
│   ├── custom_structures/
│   │   ├── custom_hash_table.py
│   │   ├── bloom_filter.py
│   │   └── lru_cache.py
│   ├── optimizers/
│   │   ├── deduplicator.py
│   │   ├── key_compressor.py
│   │   └── set_operations.py
│   ├── profiler/
│   │   ├── collision_tracker.py
│   │   └── lookup_benchmarker.py
│   └── ui/
│       ├── store_cli.py
│       └── memory_visualizer.py
├── tests/
│   ├── test_hash_correctness.py
│   ├── test_collision_handling.py
│   └── test_deduplication_speed.py
├── .env.example
├── main.py
├── pyproject.toml
└── README.md
```

## Instalasi

Proyek ini pure Python (tidak ada dependensi wajib di luar standard
library). Cukup pastikan Python 3.10+ tersedia.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"     # opsional, hanya untuk menjalankan pytest
```

## Menjalankan Aplikasi

```bash
# Mode interaktif (Store CLI)
python main.py

# Mode demo cepat (menunjukkan semua komponen sekaligus)
python main.py --demo
```

Contoh sesi interaktif:

```
store> put nama Budi
OK: 'nama' disimpan.
store> get nama
Budi
store> bloom-add python
'python' ditambahkan ke bloom filter.
store> bloom-check golang
Pasti tidak ada.
store> visualize
=== Distribusi Bucket (Memory Visualizer) ===
...
store> exit
```

## Menjalankan Test

```bash
python -m pytest tests/ -v
```

Atau tanpa pytest, menggunakan modul `unittest` bawaan:

```bash
python -m unittest discover -s tests -v
```

## Konsep Kunci yang Dipelajari

1. **Index Calculation**: `index = hash(key) % capacity`.
2. **Collision Resolution**: Chaining vs Open Addressing (linear probing
   + tombstone untuk delete).
3. **Rehashing**: strategi menjaga load factor tetap sehat agar performa
   O(1) rata-rata terjaga.
4. **Probabilistic Data Structures**: trade-off akurasi vs efisiensi
   memori pada Bloom Filter.
5. **Cache Eviction Policy**: LRU sebagai contoh strategi penggantian
   cache O(1).
6. **String Interning**: mengurangi duplikasi objek string di memori.

Lihat `docs/hash_collision_strategies.md` dan
`docs/memory_overhead_analysis.md` untuk pembahasan teori lebih lanjut.
