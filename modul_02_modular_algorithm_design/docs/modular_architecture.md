# Modular Architecture

Dokumen ini menjelaskan diagram alur antar-modul & dependensi sistem.

## Prinsip Desain

- **Loose Coupling** — modul tidak saling mengimpor secara langsung.
  Komunikasi antar-modul terjadi lewat `Event Bus` (`src/core/bus.py`)
  atau lewat `Dispatcher` yang memanggil modul lewat kontrak
  `BaseModule`, bukan lewat referensi langsung ke kelas modul lain.
- **High Cohesion** — setiap modul (`analytics`, `transformation`,
  `validation`) hanya berisi logika yang berkaitan erat dengan satu
  tanggung jawab spesifik.
- **Pluggable Modules** — modul baru cukup didaftarkan di
  `config/module_registry.py` tanpa mengubah kode inti (`src/core/`).

## Alur Eksekusi Tingkat Tinggi

```
                ┌────────────────────┐
                │   main.py (entry)  │
                └─────────┬───────────┘
                          │
                          ▼
                ┌────────────────────┐
                │  ModuleRegistry    │◄──── config/module_registry.py
                │  (config/)         │
                └─────────┬───────────┘
                          │ load(name)
                          ▼
                ┌────────────────────┐
                │   Dispatcher        │───► publish event
                │  (src/core/)        │        │
                └─────────┬───────────┘        ▼
                          │             ┌────────────────┐
                          │             │   EventBus      │
                          │             └────────────────┘
                          ▼
        ┌─────────────────────────────────────────┐
        │            Modul Independen               │
        │  ┌───────────┐ ┌───────────────┐ ┌───────┐ │
        │  │ analytics │ │ transformation │ │ valid.│ │
        │  └───────────┘ └───────────────┘ └───────┘ │
        └─────────────────────────────────────────┘
                          ▲
                          │ inject dependencies
                ┌────────────────────┐
                │ DependencyContainer │
                │  (src/core/)        │
                └────────────────────┘
```

## Dependensi Antar-Layer

| Layer             | Boleh bergantung pada                 | Tidak boleh bergantung pada              |
| ----------------- | ------------------------------------- | ---------------------------------------- |
| `src/interfaces/` | (tidak ada, ini kontrak paling dasar) | modul spesifik apapun                    |
| `src/modules/*`   | `src/interfaces/`, `src/utils/`       | modul independen lainnya secara langsung |
| `src/core/`       | `src/interfaces/`, `config/`          | isi/logika internal modul                |
| `config/`         | `src/interfaces/`                     | `src/core/`, `src/modules/`              |

## Pipeline Contoh

`main.py` menjalankan pipeline default: `transformation` → `validation`
→ `analytics`, di mana output satu modul menjadi input modul berikutnya
lewat `Dispatcher.run_pipeline(...)`. Urutan ini dapat diubah kapan saja
tanpa menyentuh kode modul itu sendiri.
