# Teori Kompleksitas: Big-O Notation

Dokumen ini merangkum kurva pertumbuhan kompleksitas waktu/ruang yang
menjadi acuan `complexity_analyzer.py` dalam menebak kelas Big-O suatu
fungsi berdasarkan data hasil profiling.

## Kelas Kompleksitas yang Didukung

| Notasi        | Nama            | Karakteristik Pertumbuhan                               | Contoh Operasi                         |
|---------------|-----------------|-----------------------------------------------------------|-----------------------------------------|
| O(1)          | Konstan         | Waktu tidak berubah walau N membesar                      | Akses elemen array via index            |
| O(log N)      | Logaritmik      | Waktu bertambah sangat lambat, memotong ruang cari separuh | Binary search                           |
| O(N)          | Linear          | Waktu bertambah proporsional dengan N                      | Linear scan / traversal array           |
| O(N log N)    | Linearithmic    | Sedikit lebih cepat dari kuadratik, umum di sorting        | Merge sort, quicksort (average case)    |
| O(N^2)        | Kuadratik       | Waktu bertambah dengan kuadrat N                            | Nested loop, bubble sort                |

## Cara Estimasi Otomatis

`complexity_analyzer.py` mengestimasi kelas Big-O dengan membandingkan
rasio pertumbuhan waktu eksekusi terhadap pertumbuhan N di antara dua
titik skala berurutan (mis. Medium -> Large). Secara kasar:

- Jika `waktu(2N) / waktu(N) ≈ 1`      → kandidat **O(1)**
- Jika rasio ≈ `log(2N) / log(N)`      → kandidat **O(log N)**
- Jika rasio ≈ `2`                     → kandidat **O(N)**
- Jika rasio ≈ `2 * log(2N)/log(N)`    → kandidat **O(N log N)**
- Jika rasio ≈ `4`                     → kandidat **O(N^2)**

Kelas yang dipilih adalah kelas dengan rasio prediksi **paling dekat**
(error absolut terkecil) dengan rasio yang benar-benar terukur.

## Best / Average / Worst Case

Untuk algoritma yang sensitif terhadap urutan data (mis. algoritma
sorting berbasis perbandingan), profil kinerja diuji pada tiga skenario:

1. **Best Case** — data sudah terurut sempurna.
2. **Average Case** — data acak (random shuffle).
3. **Worst Case** — data terbalik total (reverse-sorted).

Perbedaan performa antar skenario ini membantu mengungkap apakah suatu
algoritma memiliki kompleksitas best-case yang lebih baik dari
worst-case-nya (contoh klasik: quicksort naive O(N log N) rata-rata,
namun O(N^2) pada worst case data yang sudah terurut).
