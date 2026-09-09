# Sorting Stability

## Definisi

Sebuah algoritma pengurutan disebut **stable** apabila algoritma tersebut
mempertahankan urutan relatif dari dua elemen yang memiliki nilai kunci
(key) yang sama.

Contoh: misalkan kita mengurutkan daftar mahasiswa berdasarkan nilai, dan
ada dua mahasiswa dengan nilai yang sama — `("Budi", 80)` dan `("Ani", 80)`.
Jika `("Budi", 80)` muncul lebih dulu pada data asli, algoritma yang stable
akan tetap menempatkan Budi sebelum Ani setelah pengurutan.

## Klasifikasi pada Modul 06

| Algoritma        | Stable? | Alasan                                                                 |
|-------------------|:-------:|-------------------------------------------------------------------------|
| Bubble Sort        | Ya      | Hanya menukar elemen yang bersebelahan jika benar-benar lebih besar (`>`), tidak pernah menukar elemen yang sama nilainya. |
| Selection Sort     | Tidak   | Menukar posisi elemen minimum secara langsung (swap jarak jauh) yang bisa memindahkan elemen melewati elemen lain bernilai sama. |
| Insertion Sort     | Ya      | Menyisipkan elemen baru dengan hanya menggeser elemen yang *lebih besar* secara ketat, sehingga elemen sama nilai tidak dilewati. |
| Merge Sort         | Ya      | Proses merge mengambil dari sisi kiri terlebih dahulu jika nilainya sama (`<=`). |
| Quick Sort         | Tidak   | Proses partisi melakukan swap berdasarkan posisi pivot, yang dapat mengubah urutan relatif elemen bernilai sama. |

## Mengapa Ini Penting?

Stability menjadi krusial ketika kita melakukan **multi-key sorting**
(mengurutkan berdasarkan lebih dari satu kriteria secara bertahap). Sebagai
contoh, jika kita ingin mengurutkan data berdasarkan "kota" lalu "nama",
kita bisa:

1. Urutkan dulu berdasarkan "nama" menggunakan algoritma stable.
2. Urutkan lagi berdasarkan "kota" menggunakan algoritma stable yang sama.

Karena algoritmanya stable, urutan nama di dalam kota yang sama akan tetap
terjaga dari langkah pertama.

## Verifikasi di Kode

Lihat `tests/test_stability.py` yang menguji stabilitas tiap algoritma
menggunakan pasangan `(nilai, indeks_asli)` sebagai data uji, lalu
memverifikasi bahwa untuk nilai yang sama, `indeks_asli` tetap terurut naik
setelah proses sorting.
