# Modul 07 — Algorithm Integration Blueprint

CLI Data Pipeline & Multi-Algorithm Orchestrator Engine yang mengalirkan
data dari tahap pembersihan (cleansing), pengurutan (sorting), pencarian
(searching), hingga transformasi format data (adapter), semuanya
dirangkai lewat Pipeline Orchestrator agar bebas hambatan (bottleneck)
dan duplikasi memori.

## Instalasi

Tidak ada dependensi eksternal wajib. Untuk menjalankan test:

```bash
pip install pytest --break-system-packages
```

## Menjalankan CLI

```bash
# Route bawaan: Filter -> Quick Sort -> Binary Search
python main.py --route clean_sort_search --target 42

# Route: Merge Sort -> ubah jadi Binary Search Tree
python main.py --route sort_to_tree

# Route: Filter -> ubah jadi Hash Index
python main.py --route dedupe_to_hash

# Lanjutkan meski ada stage yang gagal (skip, bukan berhenti total)
python main.py --route clean_sort_search --continue-on-error
```

## Menjalankan Test

```bash
pytest tests/ -v
# atau tanpa pytest:
python tests/test_pipeline_flow.py
python tests/test_adapter_conversions.py
python tests/test_failure_recovery.py
```

## Struktur Proyek

```
modul_07_algorithm_integration/
├── config/            # Konfigurasi pipeline & pemetaan strategi
├── docs/              # Dokumentasi arsitektur & analisis coupling
├── src/
│   ├── components/    # Filter, Sorter, Searcher (wrapper seragam)
│   ├── pipeline/       # Context, Builder (Fluent), Runner
│   ├── adapters/       # Array->Tree, List->Hash (Adapter Pattern)
│   └── ui/             # Visualizer & Stage Reporter
├── tests/             # End-to-end, adapter, dan failure-recovery tests
└── main.py            # Entry point CLI interaktif
```

## Konsep Kunci

- **Fluent Builder Pattern** untuk menyusun pipeline secara deklaratif.
- **Uniform Stage Interface**: `fn(context) -> (context, message)`.
- **Adapter Pattern** untuk menjembatani format data antar-algoritma.
- **Graceful Failure Handling** dengan opsi stop-on-failure atau
  continue-on-error, lengkap dengan stage profiling.
