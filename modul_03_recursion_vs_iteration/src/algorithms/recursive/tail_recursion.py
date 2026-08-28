"""
tail_recursion.py
--------------------
Implementasi Fibonacci dengan gaya Tail Call Recursion.

Catatan penting:
    CPython TIDAK melakukan Tail Call Optimization (TCO) secara otomatis.
    Artinya, walau ditulis dalam gaya tail-recursive, setiap pemanggilan
    tetap menambah stack frame baru. Implementasi ini disertakan untuk
    tujuan perbandingan gaya kode, bukan sebagai solusi nyata untuk
    menghindari stack overflow di Python.

Kompleksitas:
    Time  : O(N)
    Space : O(N) di Python (bukan O(1) seperti pada bahasa ber-TCO)
"""


def fibonacci_tail_recursive(n: int, a: int = 0, b: int = 1) -> int:
    """
    Menghitung Fibonacci ke-n menggunakan gaya tail recursion.

    Args:
        n: indeks Fibonacci yang ingin dihitung.
        a: akumulator nilai fib(0) pada pemanggilan awal.
        b: akumulator nilai fib(1) pada pemanggilan awal.

    Returns:
        Nilai Fibonacci ke-n.
    """
    if n < 0:
        raise ValueError("n tidak boleh negatif")
    if n == 0:
        return a
    return fibonacci_tail_recursive(n - 1, b, a + b)


def factorial_tail_recursive(n: int, accumulator: int = 1) -> int:
    """
    Contoh tambahan tail recursion: faktorial.

    Args:
        n: bilangan yang ingin dihitung faktorialnya.
        accumulator: akumulator hasil perkalian (internal).

    Returns:
        Nilai n!.
    """
    if n < 0:
        raise ValueError("n tidak boleh negatif")
    if n in (0, 1):
        return accumulator
    return factorial_tail_recursive(n - 1, accumulator * n)
