"""
constants.py
-------------
Parameter pengujian: skala sampel data (data sizes) dan batas iterasi
yang digunakan oleh engine benchmarking.
"""

# Skala N yang diuji untuk fungsi fibonacci (rekursif vs iteratif).
FIBONACCI_TEST_SIZES = [5, 10, 15, 20, 25, 30]

# Skala kedalaman pohon (tree) yang diuji untuk tree traversal.
TREE_DEPTH_TEST_SIZES = [3, 5, 7, 10, 12]

# Jumlah node acak yang dibangkitkan untuk pengujian tree traversal.
TREE_NODE_COUNT = 500

# Batas iterasi maksimum untuk versi iteratif (safety net).
MAX_ITERATION_LIMIT = 1_000_000

# Label kolom yang digunakan pada tabel hasil perbandingan.
RESULT_TABLE_COLUMNS = [
    "N",
    "Recursive Time (µs)",
    "Iterative Time (µs)",
    "Recursive Stack Depth",
    "Iterative Memory (O(1))",
    "Result Match",
]

# Karakter yang digunakan untuk chart ASCII.
ASCII_BAR_CHAR = "█"
ASCII_CHART_MAX_WIDTH = 50
