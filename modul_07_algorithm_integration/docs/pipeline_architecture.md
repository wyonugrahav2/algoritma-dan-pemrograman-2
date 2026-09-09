# Pipeline Architecture — Modul 07

## Diagram Alur Integrasi Antar-Algoritma

```
                    ┌──────────────────┐
   Data Mentah ───▶ │ FilterComponent  │  (cleansing: buang entri invalid)
                    └────────┬─────────┘
                             ▼
                    ┌──────────────────┐
                    │ SorterComponent  │  (Quick Sort / Merge Sort)
                    └────────┬─────────┘
                             ▼
              ┌───────────────────────────────┐
              │  Percabangan (opsional)        │
              │  A. SearcherComponent (Binary) │
              │  B. ArrayToTreeAdapter (BST)   │
              │  C. ListToHashAdapter (Hash)   │
              └───────────────────────────────┘
                             ▼
                    ┌──────────────────┐
                    │  PipelineContext │  (payload akhir + metadata)
                    └────────┬─────────┘
                             ▼
              ┌────────────────────────────────┐
              │ pipeline_visualizer + reporter  │
              └────────────────────────────────┘
```

## Prinsip Desain

1. **Fluent Builder Pattern** (`src/pipeline/builder.py`) — menyusun rantai
   stage secara deklaratif dan mudah dibaca.
2. **Uniform Stage Interface** — setiap stage adalah callable dengan
   signature `fn(context) -> (context, message)`. Ini memungkinkan
   Component, Adapter, dan stage kustom apa pun dipasang secara seragam
   ke dalam `PipelineRunner`.
3. **Immutability by Convention** — `PipelineContext.with_payload()`
   selalu mengembalikan context baru, bukan memutasi context lama secara
   langsung, sehingga riwayat (history) tetap konsisten untuk audit.
4. **Adapter Pattern** — menjembatani ketidakcocokan format data antar
   algoritma (misalnya array terurut dari sorter perlu diubah dulu ke BST
   sebelum dipakai algoritma pohon lain).
5. **Graceful Failure Handling** — `PipelineRunner` menangkap exception
   tiap stage secara terisolasi; perilaku berhenti-atau-lanjut diatur via
   `stop_on_failure`.

## Contoh Kombinasi Route

Lihat `config/pipeline_routes.py` untuk kombinasi siap pakai seperti
`clean_sort_search` (Filter → Quick Sort → Binary Search).
