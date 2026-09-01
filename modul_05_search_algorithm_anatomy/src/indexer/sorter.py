"""
sorter.py
Melakukan pre-sorting data mentah — prasyarat mutlak bagi algoritma
Binary Search, Interpolation Search, dan Exponential Search.

Modul ini juga menyediakan utilitas untuk memeriksa apakah data sudah
terurut dan untuk menghitung skor keseragaman (uniformity score) yang
dipakai oleh config/search_strategies.py::recommend_strategy().
"""

import statistics
from typing import List, Sequence, Tuple


def is_sorted(data: Sequence[float]) -> bool:
    """Mengecek apakah data sudah terurut ascending."""
    return all(data[i] <= data[i + 1] for i in range(len(data) - 1))


def sort_data(data: Sequence[float], reverse: bool = False) -> List[float]:
    """
    Mengurutkan data secara ascending (default) menggunakan Timsort
    bawaan Python (stabil, O(N log N) kasus terburuk).
    """
    return sorted(data, reverse=reverse)


def sort_with_original_index(data: Sequence[float]) -> List[Tuple[int, float]]:
    """
    Mengurutkan data sambil mempertahankan indeks asli setiap elemen.
    Berguna ketika hasil pencarian perlu dikembalikan berdasarkan posisi
    pada dataset asli (sebelum diurutkan), bukan posisi setelah sorting.

    Mengembalikan list of (original_index, value) yang terurut
    berdasarkan value.
    """
    indexed = list(enumerate(data))
    indexed.sort(key=lambda pair: pair[1])
    return indexed


def uniformity_score(data: Sequence[float]) -> float:
    """
    Menghitung estimasi skor keseragaman distribusi data (0.0 - 1.0+).

    Skor dihitung dengan membandingkan varians selisih antar elemen
    bertetangga (gap) pada data aktual terhadap varians ideal apabila
    data terdistribusi uniform sempurna (gap konstan).

    Skor mendekati 1.0 -> distribusi mendekati uniform.
    Skor mendekati atau di bawah 0.0 -> distribusi sangat skewed/cluster.

    Lihat docs/data_distribution_impact.md untuk penjelasan matematis.
    """
    if len(data) < 3:
        # Data terlalu kecil untuk mengukur keseragaman secara bermakna.
        return 1.0

    sorted_data = sort_data(data)
    gaps = [sorted_data[i + 1] - sorted_data[i] for i in range(len(sorted_data) - 1)]

    if not gaps or all(g == 0 for g in gaps):
        return 1.0

    mean_gap = statistics.mean(gaps)
    if mean_gap == 0:
        return 1.0

    actual_variance = statistics.pvariance(gaps)
    # Varians ideal pada distribusi uniform sempurna dianggap 0,
    # sehingga kita menormalisasi actual_variance relatif terhadap
    # kuadrat rata-rata gap agar skor berada pada skala yang wajar.
    normalized_variance = actual_variance / (mean_gap ** 2)

    score = 1.0 - normalized_variance
    # Batasi skor ke rentang yang masuk akal untuk pelaporan.
    return max(-1.0, min(1.0, score))


def ensure_sorted(data: Sequence[float]) -> List[float]:
    """
    Memastikan data terurut sebelum diserahkan ke algoritma yang
    mensyaratkan pre-sorting. Jika data belum terurut, akan diurutkan
    ulang; jika sudah terurut, dikembalikan sebagai list baru tanpa
    biaya sorting tambahan.
    """
    data_list = list(data)
    if is_sorted(data_list):
        return data_list
    return sort_data(data_list)
