# Data Coupling Analysis — Modul 07

## Tujuan

Menganalisis seberapa erat (tight) atau longgar (loose) keterikatan antar
komponen dalam pipeline, agar penambahan/penggantian algoritma di satu
stage tidak berdampak domino ke stage lain.

## Analisis per Boundary

| Boundary                         | Bentuk Data yang Lewat        | Tingkat Coupling |
|-----------------------------------|--------------------------------|-------------------|
| Filter → Sorter                  | `list[Any]`                    | Longgar (loose)   |
| Sorter → Searcher                | `list[Any]` (harus terurut)    | Sedang (implicit contract: harus sudah sorted) |
| Sorter → ArrayToTreeAdapter       | `list[Any]` (harus terurut)    | Sedang            |
| Filter → ListToHashAdapter        | `list[Any]` (boleh tak terurut)| Longgar           |
| Searcher → Context.metadata       | `int | None` (indeks hasil)    | Longgar           |

## Mengapa Coupling "Sedang" Masih Bisa Diterima

Kontrak implisit "data harus terurut sebelum masuk ke Binary Search atau
BST Adapter" adalah kontrak algoritmik yang memang inheren pada Big-O
`O(log N)` dari kedua struktur tersebut — bukan keterikatan implementasi.
Selama kontrak ini didokumentasikan (seperti di sini) dan divalidasi lewat
`tests/test_pipeline_flow.py`, risiko regresi tetap rendah.

## Rekomendasi Mitigasi Lanjutan

1. Tambahkan validasi eksplisit di `SearcherComponent` untuk memverifikasi
   array benar-benar terurut sebelum melakukan binary search (fail-fast).
2. Gunakan `PipelineContext.metadata` sebagai satu-satunya jalur untuk
   data pendukung (target pencarian, hasil pencarian) — jangan mencampur
   ke dalam `payload` — supaya payload tetap murni representasi data
   utama yang mengalir.
3. Setiap adapter baru wajib mendokumentasikan bentuk input yang
   diharapkan dan bentuk output yang dihasilkan di docstring modulnya.
