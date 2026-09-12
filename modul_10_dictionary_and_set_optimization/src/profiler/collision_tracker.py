"""
collision_tracker.py
Melacak frekuensi bentrokan hash dan mengukur rasio Load Factor dari
sebuah instance CustomHashTable, untuk kebutuhan analisis performa.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.custom_structures.custom_hash_table import CustomHashTable


@dataclass
class CollisionReport:
    total_entries: int
    capacity: int
    load_factor: float
    collision_count: int
    collision_rate: float  # collisions / total_entries


def track(table: "CustomHashTable") -> CollisionReport:
    """Ambil snapshot statistik bentrokan dari sebuah hash table."""
    total = table.size
    collisions = table.collision_count
    rate = collisions / total if total else 0.0
    return CollisionReport(
        total_entries=total,
        capacity=table.capacity,
        load_factor=table.load_factor,
        collision_count=collisions,
        collision_rate=rate,
    )


def print_report(report: CollisionReport) -> None:
    print("=== Collision Report ===")
    print(f"Total entries   : {report.total_entries}")
    print(f"Capacity        : {report.capacity}")
    print(f"Load factor     : {report.load_factor:.2%}")
    print(f"Collisions      : {report.collision_count}")
    print(f"Collision rate  : {report.collision_rate:.2%}")


if __name__ == "__main__":
    from src.custom_structures.custom_hash_table import CustomHashTable

    table = CustomHashTable(capacity=8, strategy="chaining")
    for i in range(50):
        table.put(f"user-{i}", i)

    print_report(track(table))
