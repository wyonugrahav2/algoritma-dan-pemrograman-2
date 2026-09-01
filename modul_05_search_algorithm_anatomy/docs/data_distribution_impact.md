# Dampak Distribusi Data terhadap Performa Pencarian

## 1. Mengapa Distribusi Data Penting?

Binary Search selalu memotong ruang pencarian tepat di tengah, tanpa
memandang nilai data — sehingga performanya **stabil** terhadap
distribusi apa pun, selama data terurut. Sebaliknya, Interpolation
Search justru mengandalkan asumsi tentang bagaimana nilai tersebar,
sehingga performanya sangat bergantung pada bentuk distribusi data.

## 2. Distribusi Uniform (Seragam)

Ciri data uniform: selisih antar elemen bertetangga relatif konsisten,
misalnya `[10, 20, 30, 40, 50, ..., 1000]`.

Pada kondisi ini, rumus estimasi posisi Interpolation Search:

```
pos = left + ((target - arr[left]) * (right - left)) / (arr[right] - arr[left])
```

menghasilkan tebakan yang sangat akurat, karena posisi relatif nilai
target terhadap rentang `[arr[left], arr[right]]` mendekati posisi
relatif indeksnya. Hasilnya, jumlah iterasi mendekati **O(log log N)**,
mengungguli Binary Search terutama pada dataset besar (N > 10.000).

## 3. Distribusi Tidak Uniform (Skewed / Clustered)

Ciri data tidak uniform: nilai mengelompok (cluster) di beberapa area
dan jarang di area lain, misalnya `[1, 2, 3, 4, 5, 1000000]`.

Pada kondisi ini, estimasi posisi bisa sangat meleset. Contoh mencari
target = 4 pada array di atas:

```
pos = 0 + ((4 - 1) * (5 - 0)) / (1000000 - 1) ≈ 0 (dibulatkan)
```

Tebakan cenderung selalu jatuh ke ujung array karena satu nilai outlier
(1.000.000) mendominasi rentang. Akibatnya, algoritma harus melakukan
banyak iterasi tambahan untuk mengoreksi tebakan, dan **kompleksitas
kasus terburuk mendekati O(N)** — lebih buruk daripada Binary Search.

## 4. Metrik Keseragaman (Uniformity Score)

Modul `config/settings.py` mendefinisikan `uniformity_tolerance`
(default `0.85`) sebagai ambang batas untuk menentukan apakah data cukup
uniform untuk merekomendasikan Interpolation Search. Skor keseragaman
dapat diestimasi dengan membandingkan varians selisih antar elemen
bertetangga terhadap varians ideal pada distribusi uniform sempurna:

```
uniformity_score = 1 - (variance(actual_gaps) / variance(expected_uniform_gaps))
```

Nilai mendekati `1.0` berarti data mendekati uniform sempurna; nilai
mendekati atau di bawah `0.0` menunjukkan data sangat mengelompok/skewed.

## 5. Rekomendasi Praktis

| Karakteristik Data                          | Strategi yang Direkomendasikan     |
|----------------------------------------------|--------------------------------------|
| Tidak terurut                                | Linear Search                        |
| Terurut, distribusi tidak diketahui/skewed   | Binary Search                        |
| Terurut, distribusi uniform, N besar         | Interpolation Search                 |
| Terurut, ukuran tidak diketahui/unbounded    | Exponential Search                   |
| Data statis, akses berulang dengan key tetap | Hash Lookup (setelah index dibangun) |

Fungsi `recommend_strategy()` pada `config/search_strategies.py`
mengimplementasikan tabel keputusan ini secara terprogram, dan hasilnya
divalidasi ulang oleh `src/analytics/search_profiler.py` yang mengukur
latensi aktual pada dataset nyata.
