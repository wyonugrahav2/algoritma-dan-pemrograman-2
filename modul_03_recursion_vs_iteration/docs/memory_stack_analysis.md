# Analisis Memori: Call Stack vs Loop Memory

## 1. Call Stack Frame pada Sistem Operasi

Setiap kali sebuah fungsi dipanggil, sistem operasi (melalui runtime bahasa
pemrograman) mengalokasikan sebuah **stack frame** baru di atas call stack.
Stack frame ini menyimpan:

- Alamat kembali (return address) ke pemanggil.
- Parameter fungsi yang diteruskan.
- Variabel lokal fungsi tersebut.
- Register CPU yang perlu disimpan sementara (saved registers).

Pada pendekatan **rekursif**, setiap pemanggilan diri sendiri (self-call)
menambah satu frame baru ke call stack. Untuk fungsi seperti `fibonacci(n)`
yang dipanggil secara rekursif murni, kedalaman stack bertumbuh sebanding
dengan `n`, sehingga kompleksitas ruang (space complexity) menjadi **O(N)**.

## 2. Bahaya Stack Overflow

Karena ukuran call stack bersifat terbatas (biasanya beberapa MB, atau
dibatasi oleh `sys.setrecursionlimit()` di Python), rekursi yang terlalu
dalam akan menyebabkan **Stack Overflow** — dalam Python direpresentasikan
sebagai exception `RecursionError`.

Kasus umum yang memicu Stack Overflow:

1. Basis kasus (base case) tidak pernah tercapai (infinite recursion).
2. Ukuran input (N) melebihi batas kedalaman rekursi yang wajar.
3. Setiap frame menyimpan data besar, mempercepat pemenuhan stack.

Modul ini menyediakan `stack_overflow_guard.py` sebagai lapisan pertahanan
agar sistem tidak crash mendadak ketika batas ini tercapai.

## 3. Loop Memory (Iteratif)

Pada pendekatan **iteratif**, tidak ada penumpukan call stack baru untuk
setiap langkah pengulangan — variabel-variabel yang dibutuhkan (misalnya
akumulator) disimpan dan diperbarui di **heap/local scope yang sama**
sepanjang eksekusi loop. Ini membuat kompleksitas ruang menjadi **O(1)**
untuk kasus seperti Fibonacci iteratif, karena hanya dibutuhkan sejumlah
variabel tetap (constant) tanpa memperhatikan seberapa besar N.

## 4. Ringkasan Perbandingan

| Aspek                  | Rekursi              | Iterasi        |
|-------------------------|----------------------|----------------|
| Space Complexity         | O(N) (umumnya)       | O(1) (umumnya) |
| Risiko Stack Overflow    | Ada                  | Tidak ada      |
| Keterbacaan kode         | Sering lebih elegan  | Kadang lebih verbose |
| Overhead pemanggilan     | Ada (function call overhead) | Minimal |
| Optimisasi Tail Call     | Bergantung interpreter (Python: tidak otomatis) | Tidak relevan |

## 5. Catatan tentang Tail Call Recursion di Python

Berbeda dengan beberapa bahasa (misalnya Scheme atau Scala), interpreter
CPython **tidak melakukan Tail Call Optimization (TCO)** secara otomatis.
Artinya, walaupun fungsi ditulis dalam gaya tail-recursive
(`tail_recursion.py`), pemanggilan tersebut tetap menambah stack frame baru
di Python. Implementasi pada modul ini tetap menyertakan versi tail
recursive untuk tujuan perbandingan gaya penulisan kode, namun secara
praktik performa dan keamanan stack-nya tetap setara dengan rekursi biasa —
bukan seperti pada bahasa yang mendukung TCO native.
