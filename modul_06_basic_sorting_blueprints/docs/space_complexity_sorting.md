# Space Complexity: In-Place vs Auxiliary Space

## In-Place Sorting — O(1) Auxiliary Space

Algoritma disebut **in-place** jika hanya membutuhkan sejumlah kecil memori
tambahan (konstan) di luar array input itu sendiri — biasanya hanya
beberapa variabel bantu seperti `temp`, `i`, `j`.

- **Bubble Sort** — O(1): hanya butuh satu variabel temporer untuk swap.
- **Selection Sort** — O(1): hanya butuh indeks minimum & satu variabel swap.
- **Insertion Sort** — O(1): hanya butuh satu variabel `key` untuk elemen yang disisipkan.
- **Quick Sort** — O(log N): secara teknis in-place karena partisi dilakukan
  langsung pada array, namun rekursi menggunakan call stack sedalam
  O(log N) pada kasus rata-rata (bisa O(N) pada kasus terburuk jika pivot
  buruk terus-menerus).

## Auxiliary Space Sorting — O(N)

- **Merge Sort** — O(N): pada setiap pemanggilan `merge()`, dibutuhkan
  array sementara berukuran total N untuk menampung hasil penggabungan
  dua sub-array sebelum disalin kembali ke array asli. Ini adalah harga
  yang dibayar untuk mendapatkan kompleksitas waktu O(N log N) yang
  konsisten pada semua kasus (best, average, worst).

## Trade-off

| Algoritma       | Time (Avg)     | Space     | Cocok untuk                                      |
|-----------------|----------------|-----------|---------------------------------------------------|
| Bubble Sort      | O(N^2)         | O(1)      | Edukasi, data sangat kecil                         |
| Selection Sort   | O(N^2)         | O(1)      | Ketika biaya swap mahal (jumlah swap minimal = N)  |
| Insertion Sort   | O(N^2)*        | O(1)      | Data yang hampir terurut (adaptive)                |
| Merge Sort       | O(N log N)     | O(N)      | Data besar, butuh stability, external sorting      |
| Quick Sort       | O(N log N)     | O(log N)  | Data besar, memori terbatas, stability tidak wajib |

`*` Insertion Sort bersifat *adaptive*: mendekati O(N) pada data yang
hampir terurut karena jumlah pergeseran elemen menjadi sangat sedikit.

## Pengukuran Empiris

`src/metrics/memory_tracker.py` melacak alokasi memori tambahan secara
nyata menggunakan modul `tracemalloc` bawaan Python, sehingga klaim
teoritis di atas dapat diverifikasi dengan data pengukuran aktual saat
menjalankan `main.py`.
