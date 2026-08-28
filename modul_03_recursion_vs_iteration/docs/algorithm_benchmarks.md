# Catatan Teori: Big-O Time & Space Complexity

## 1. Kompleksitas Waktu (Time Complexity)

| Algoritma                     | Rekursif            | Iteratif      |
|--------------------------------|----------------------|---------------|
| Fibonacci (naive)               | O(2^N)               | O(N)          |
| Fibonacci (tail recursion)      | O(N)                 | O(N)          |
| Tree Traversal (pre/in/post)    | O(N)                 | O(N)          |

Fibonacci rekursif naif (tanpa memoization) memiliki kompleksitas
eksponensial O(2^N) karena setiap pemanggilan `fib(n)` memicu dua
pemanggilan baru (`fib(n-1)` dan `fib(n-2)`), yang menghasilkan pohon
rekursi yang tumbuh secara eksponensial. Versi tail-recursive dan iteratif
keduanya berjalan linear O(N) karena hanya menghitung setiap nilai
Fibonacci sekali.

## 2. Kompleksitas Ruang (Space Complexity)

| Algoritma                     | Rekursif            | Iteratif      |
|--------------------------------|----------------------|---------------|
| Fibonacci (naive)               | O(N) — stack depth   | O(1)          |
| Fibonacci (tail recursion)      | O(N) — di Python*    | O(1)          |
| Tree Traversal                  | O(H) — H = tinggi pohon | O(1)–O(N)** |

\* Python tidak mendukung Tail Call Optimization, sehingga versi tail
recursive tetap memakan O(N) stack frame walaupun secara konsep
"seharusnya" bisa O(1) pada bahasa yang mendukung TCO.

\** Traversal iteratif menggunakan stack/queue eksplisit yang disimpan di
heap (bukan call stack), sehingga secara teknis tetap memakan memori
sebanding dengan tinggi/jumlah node pohon — namun tidak berisiko
`RecursionError` karena tidak bergantung pada batas call stack interpreter.

## 3. Trade-off Umum

- **Rekursi** cenderung menghasilkan kode yang lebih ringkas dan mendekati
  definisi matematis asli (misalnya definisi Fibonacci atau traversal
  pohon), tetapi rentan terhadap overhead pemanggilan fungsi dan risiko
  stack overflow pada input besar.
- **Iterasi** umumnya lebih hemat memori dan lebih cepat pada Python karena
  tidak ada overhead pembuatan stack frame berulang, tetapi terkadang
  memerlukan struktur data eksplisit (stack/queue) untuk mensimulasikan
  proses yang secara natural rekursif (seperti traversal pohon).

## 4. Metodologi Benchmarking pada Modul Ini

1. Setiap fungsi diuji dengan beberapa ukuran input N (lihat
   `config/constants.py`).
2. Waktu eksekusi diukur menggunakan `time.perf_counter()` untuk presisi
   hingga level mikrodetik.
3. Setiap pengujian diulang sebanyak `BENCHMARK_REPEAT_COUNT` kali dan
   diambil rata-ratanya untuk mengurangi noise pengukuran.
4. Kedalaman stack (untuk versi rekursif) dilacak menggunakan
   `sys._getframe()` atau penghitung manual di dalam fungsi.
5. Hasil dari kedua pendekatan dibandingkan menggunakan
   `test_result_parity.py` untuk memastikan validitas sebelum
   membandingkan performanya.
