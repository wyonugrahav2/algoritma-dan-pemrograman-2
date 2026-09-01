# Search Space Reduction: Matematika Penyusutan Ruang Pencarian

## 1. Konsep Dasar

Setiap algoritma pencarian dapat dilihat sebagai proses **penciutan ruang
pencarian (search space)** — himpunan indeks yang masih mungkin berisi
elemen target. Efisiensi algoritma ditentukan oleh seberapa cepat ruang
ini menyusut menuju ukuran nol (atau menuju satu elemen yang diperiksa).

## 2. Linear Search — Penyusutan Linear O(N)

Ruang pencarian menyusut **satu elemen per iterasi**:

```
N -> N-1 -> N-2 -> ... -> 1 -> 0
```

Tidak ada informasi tambahan yang dimanfaatkan (data boleh tidak
terurut), sehingga rata-rata dibutuhkan `N/2` perbandingan pada kasus
target ditemukan, dan `N` perbandingan pada kasus target tidak ada.

## 3. Binary Search — Penyusutan Logaritmik O(log N)

Karena data **wajib terurut**, algoritma dapat membuang separuh ruang
pencarian pada setiap iterasi:

```
N -> N/2 -> N/4 -> N/8 -> ... -> 1
```

Jumlah iterasi maksimum adalah `ceil(log2(N))`. Contoh untuk N = 1.000.000:

```
log2(1,000,000) ≈ 19.93 -> maksimum 20 langkah
```

Dibandingkan Linear Search yang butuh hingga 1.000.000 langkah, ini
adalah lompatan efisiensi yang sangat besar.

## 4. Interpolation Search — Estimasi Posisi, bukan Sekadar Pemotongan

Alih-alih selalu mengambil titik tengah, Interpolation Search menghitung
estimasi posisi berdasarkan nilai target relatif terhadap rentang nilai:

```
pos = left + ((target - arr[left]) * (right - left)) / (arr[right] - arr[left])
```

Pada data yang **terdistribusi uniform**, penyusutan ruang pencarian
mendekati:

```
N -> sqrt(N) -> sqrt(sqrt(N)) -> ... 
```

yang secara rata-rata menghasilkan kompleksitas **O(log log N)** — lebih
cepat dari Binary Search. Namun pada distribusi yang tidak uniform,
estimasi posisi bisa sangat meleset dan kompleksitas dapat memburuk
mendekati O(N) pada kasus terburuk (lihat `data_distribution_impact.md`).

## 5. Exponential Search — Menemukan Rentang Sebelum Memotongnya

Exponential Search berguna ketika ukuran data tidak diketahui (unbounded)
atau target diperkirakan berada di posisi awal array. Prosesnya dua fase:

1. **Fase eksponensial**: melipatgandakan batas (`1, 2, 4, 8, ...`) hingga
   `arr[bound] >= target`.
2. **Fase pemotongan**: menjalankan Binary Search pada rentang
   `[bound/2, bound]`.

Total kompleksitas tetap **O(log N)**, karena kedua fase masing-masing
logaritmik.

## 6. Hash Lookup — Penyusutan Instan O(1)

Hash Lookup tidak menyusutkan ruang pencarian secara bertahap;
sebaliknya, ia memetakan langsung `key -> posisi/nilai` melalui fungsi
hash. Selama tidak ada collision signifikan (load factor terjaga sesuai
`IndexConfig.hash_max_load_factor`), pencarian selesai dalam waktu
konstan rata-rata **O(1)**.

## 7. Ringkasan Perbandingan

| Algoritma            | Prasyarat Data      | Pola Penyusutan       | Kompleksitas Rata-rata |
|-----------------------|---------------------|------------------------|--------------------------|
| Linear Search         | Tidak perlu terurut | N -> N-1 -> ...        | O(N)                     |
| Binary Search         | Terurut             | N -> N/2 -> N/4 -> ...  | O(log N)                 |
| Interpolation Search  | Terurut & uniform   | N -> sqrt(N) -> ...     | O(log log N)             |
| Exponential Search    | Terurut             | 1 -> 2 -> 4 -> ... -> N | O(log N)                 |
| Hash Lookup           | Ter-index (hash map)| Langsung ke posisi     | O(1)                     |

Modul `src/analytics/search_space_tracker.py` mencatat nilai `left`,
`mid`/`pos`, dan `right` pada setiap iterasi eksekusi nyata, sehingga
teori di atas dapat diverifikasi langsung terhadap data aktual melalui
`step_visualizer.py`.
