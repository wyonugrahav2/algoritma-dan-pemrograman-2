# Strategi Penanganan Bentrokan Hash (Hash Collision Strategies)

## 1. Apa itu Hash Collision?

Bentrokan hash terjadi ketika dua key berbeda menghasilkan indeks bucket yang
sama setelah dipetakan oleh fungsi hash: `index = hash(key) % capacity`.
Karena ruang key biasanya jauh lebih besar daripada jumlah bucket, bentrokan
adalah hal yang **pasti terjadi**, bukan kasus langka — pertanyaannya hanya
seberapa sering dan bagaimana menanganinya.

## 2. Chaining (Separate Chaining)

Setiap bucket menyimpan sebuah list (atau linked list) dari pasangan
`(key, value)`. Saat terjadi bentrokan, elemen baru cukup ditambahkan ke
list pada bucket tersebut.

- **Kelebihan**: implementasi sederhana, tidak ada masalah *clustering*,
  load factor bisa > 1.
- **Kekurangan**: overhead memori tambahan untuk struktur list, lookup
  terburuk menjadi O(n) jika satu bucket menampung banyak elemen.

## 3. Open Addressing (Linear Probing)

Semua elemen disimpan langsung di dalam array utama. Saat bentrokan
terjadi, algoritma mencari slot kosong berikutnya secara linear:
`index, index+1, index+2, ...` (mod capacity).

- **Kelebihan**: locality memori lebih baik (cache-friendly), tidak ada
  overhead struktur tambahan.
- **Kekurangan**: rawan *primary clustering*, penghapusan elemen lebih
  rumit (butuh tombstone), performa menurun tajam mendekati load factor 1.

## 4. Perbandingan Load Factor

| Load Factor | Chaining (avg lookup) | Open Addressing (avg lookup) |
|-------------|------------------------|-------------------------------|
| 0.25        | ~1.1 elemen/bucket     | Sangat cepat                  |
| 0.50        | ~1.25 elemen/bucket    | Cepat                          |
| 0.75        | ~1.5 elemen/bucket     | Mulai melambat                |
| 0.90+       | ~1.9 elemen/bucket     | Sangat lambat, sering resize  |

Implementasi `custom_hash_table.py` pada modul ini menggunakan strategi yang
dapat dikonfigurasi melalui `config/settings.py` (`COLLISION_STRATEGY`), dan
melakukan **rehashing otomatis** ketika load factor melewati
`LOAD_FACTOR_THRESHOLD`.

## 5. Rehashing

Ketika load factor melewati ambang batas, tabel akan:
1. Membuat array bucket baru dengan kapasitas `capacity * RESIZE_MULTIPLIER`.
2. Menghitung ulang indeks setiap key yang ada (karena `index = hash(key) % capacity_baru`).
3. Memindahkan seluruh pasangan key-value ke tabel baru.

Proses ini berbiaya O(n) namun **amortized O(1)** per insert jika dianalisis
dalam jangka panjang.
