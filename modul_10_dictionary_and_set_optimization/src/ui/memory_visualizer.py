"""
memory_visualizer.py
Visualisasi distribusi bucket memori dan load factor sebuah CustomHashTable
langsung di terminal, menggunakan karakter ASCII sederhana (tanpa dependensi
eksternal seperti Rich, agar tetap portable).
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.custom_structures.custom_hash_table import CustomHashTable


def render_bucket_distribution(table: "CustomHashTable", max_width: int = 40) -> str:
    """
    Hanya berlaku untuk strategi 'chaining', di mana setiap bucket memiliki
    panjang list yang bervariasi (indikasi bentrokan).
    """
    if table._strategy != "chaining":  # noqa: SLF001 (akses internal untuk visualisasi)
        return "Visualisasi distribusi bucket hanya tersedia untuk strategi 'chaining'."

    lengths = [len(bucket) for bucket in table._buckets]  # noqa: SLF001
    max_len = max(lengths) if lengths else 1
    max_len = max(max_len, 1)

    lines = ["=== Distribusi Bucket (Memory Visualizer) ==="]
    for i, length in enumerate(lengths):
        bar_len = int((length / max_len) * max_width) if max_len else 0
        bar = "█" * bar_len
        lines.append(f"bucket[{i:>3}] |{bar:<{max_width}}| {length} item")

    lines.append(f"\nLoad factor : {table.load_factor:.2%}")
    lines.append(f"Total item  : {table.size}")
    lines.append(f"Capacity    : {table.capacity}")
    lines.append(f"Collisions  : {table.collision_count}")
    return "\n".join(lines)


def render_load_factor_bar(load_factor: float, width: int = 40) -> str:
    filled = int(min(load_factor, 1.0) * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {load_factor:.1%}"


if __name__ == "__main__":
    from src.custom_structures.custom_hash_table import CustomHashTable

    table = CustomHashTable(capacity=8, strategy="chaining")
    for i in range(30):
        table.put(f"item-{i}", i)

    print(render_bucket_distribution(table))
    print()
    print("Load factor bar:", render_load_factor_bar(table.load_factor))
