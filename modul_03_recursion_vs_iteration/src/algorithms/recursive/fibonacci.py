"""
fibonacci.py (recursive)
--------------------------
Implementasi murni berbasis rekursi untuk deret Fibonacci.

Kompleksitas:
    Time  : O(2^N) — rekursi naif tanpa memoization
    Space : O(N)   — kedalaman call stack sebanding dengan N
"""


def fibonacci_recursive(n: int) -> int:
    """
    Menghitung nilai Fibonacci ke-n secara rekursif murni (naive).

    Args:
        n: indeks Fibonacci yang ingin dihitung (n >= 0).

    Returns:
        Nilai Fibonacci ke-n.

    Raises:
        ValueError: jika n negatif.
        RecursionError: jika n melebihi batas kedalaman rekursi interpreter.
    """
    if n < 0:
        raise ValueError("n tidak boleh negatif")
    if n in (0, 1):
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_recursive_with_depth(n: int, depth: int = 0):
    """
    Variasi fibonacci rekursif yang juga melacak kedalaman stack maksimum
    yang tercapai selama eksekusi. Berguna untuk keperluan profiling.

    Args:
        n: indeks Fibonacci yang ingin dihitung.
        depth: kedalaman rekursi saat ini (internal, jangan diisi manual).

    Returns:
        Tuple (nilai_fibonacci, kedalaman_maksimum).
    """
    if n < 0:
        raise ValueError("n tidak boleh negatif")
    if n in (0, 1):
        return n, depth

    left_val, left_depth = fibonacci_recursive_with_depth(n - 1, depth + 1)
    right_val, right_depth = fibonacci_recursive_with_depth(n - 2, depth + 1)

    return left_val + right_val, max(left_depth, right_depth)
