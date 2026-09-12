# Analisis Overhead Memori: PyDict / PySet vs Memory Array

## 1. Mengapa Dict/Set di Python "Mahal" Secara Memori?

`dict` dan `set` bawaan Python dioptimalkan untuk **kecepatan akses O(1)**,
bukan untuk efisiensi memori. Setiap entri menyimpan bukan hanya value,
tetapi juga:

- Hash value yang telah dihitung (cache untuk menghindari re-hash).
- Pointer ke key dan value (referensi objek, bukan nilai mentah).
- Slot kosong tambahan yang disediakan untuk menjaga load factor rendah
  (CPython menjaga rasio pengisian sekitar 1/3 - 2/3).

## 2. Perbandingan Kasar (ilustratif)

| Struktur              | ~Overhead per elemen (64-bit CPython) |
|------------------------|----------------------------------------|
| `list` murni            | ~8 byte (pointer) + objek Python        |
| `array.array` (typed)   | Mendekati ukuran native (4-8 byte)      |
| `dict`                  | ~50-120 byte per entri (tergantung versi)|
| `set`                   | Mirip dict tanpa value, tetap besar     |
| `custom_hash_table.py` (edukasi) | Bergantung desain, umumnya lebih besar dari native karena Python-level object overhead, tapi lebih transparan/terkontrol |

## 3. Kapan Memory Array Lebih Baik?

Jika key berupa integer padat (misalnya 0..N) dan value berukuran
tetap/kecil, struktur array mentah (atau `array.array`, NumPy) akan jauh
lebih hemat memori dibanding dict, karena tidak perlu menyimpan hash,
pointer key, dan bucket kosong.

## 4. Bloom Filter Sebagai Alternatif Hemat Memori

`bloom_filter.py` pada modul ini adalah contoh struktur *probabilistic
set* yang menukar akurasi 100% dengan penghematan memori drastis:

- Sebuah `set` Python untuk 1 juta string bisa menghabiskan puluhan MB.
- Bloom filter dengan tingkat false-positive 1% untuk data yang sama bisa
  hanya membutuhkan beberapa MB (ukuran bit array), karena hanya
  menyimpan bit, bukan objek key itu sendiri.

## 5. String Interning (`key_compressor.py`)

Ketika banyak key string yang identik/berulang muncul di seluruh sistem
(misalnya nama kolom, kode negara, status), `sys.intern()` memastikan
hanya satu objek string disimpan di memori dan direferensikan berulang
kali, mengurangi duplikasi objek string secara signifikan.
