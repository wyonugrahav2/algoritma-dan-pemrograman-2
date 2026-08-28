"""
fibonacci.py (iterative)
--------------------------
Implementasi murni berbasis perulangan (loop) untuk deret Fibonacci.
Signature fungsi identik secara isomorfis dengan versi rekursif agar
mudah dibandingkan oleh engine benchmarking.

Kompleksitas:
    Time  : O(N)
    Space : O(1)
"""


def fibonacci_recursive(n: int) -> int:
    """
    Menghitung nilai Fibonacci ke-n secara iteratif.
    (Nama fungsi disamakan dengan versi rekursif agar dapat dipanggil
    secara isomorfis oleh runner.py)

    Args:
        n: indeks Fibonacci yang ingin dihitung (n >= 0).

    Returns:
        Nilai Fibonacci ke-n.

    Raises:
        ValueError: jika n negatif.
    """
    if n < 0:
        raise ValueError("n tidak boleh negatif")
    if n in (0, 1):
        return n

    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr


def fibonacci_recursive_with_depth(n: int, depth: int = 0):
    """
    Variasi fibonacci iteratif yang mengembalikan tuple (nilai, "kedalaman")
    agar signature-nya konsisten dengan versi rekursif. Karena iteratif
    tidak memiliki stack depth yang bertumbuh, nilai kedalaman selalu 0
    (menunjukkan O(1) space usage).

    Args:
        n: indeks Fibonacci yang ingin dihitung.
        depth: tidak digunakan, disediakan untuk kompatibilitas signature.

    Returns:
        Tuple (nilai_fibonacci, 0).
    """
    return fibonacci_recursive(n), 0
