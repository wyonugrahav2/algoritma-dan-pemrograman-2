#!/usr/bin/env python3
"""
main.py
Entry Point Interaktif untuk KV-Store CLI (Modul 10: Dictionary and Set
Optimization).

Penggunaan:
    python main.py            # masuk ke mode interaktif store_cli
    python main.py --demo     # jalankan demo cepat semua komponen
"""

from __future__ import annotations
import sys

from src.ui.store_cli import StoreCLI
from src.custom_structures.custom_hash_table import CustomHashTable
from src.custom_structures.bloom_filter import BloomFilter
from src.custom_structures.lru_cache import LRUCache
from src.optimizers import deduplicator, set_operations
from src.profiler import collision_tracker, lookup_benchmarker
from src.ui.memory_visualizer import render_bucket_distribution


def run_demo() -> None:
    print("=== DEMO: Modul 10 - Dictionary and Set Optimization ===\n")

    print("-- Custom Hash Table --")
    table = CustomHashTable(capacity=4, strategy="chaining")
    for i in range(15):
        table.put(f"user-{i}", i)
    print(table)
    print(render_bucket_distribution(table))
    print()

    print("-- Bloom Filter --")
    bloom = BloomFilter(expected_items=100, false_positive_rate=0.01)
    for word in ["python", "hashing", "bloom"]:
        bloom.add(word)
    print(bloom)
    print("'python' mungkin ada?", bloom.might_contain("python"))
    print("'golang' mungkin ada?", bloom.might_contain("golang"))
    print()

    print("-- LRU Cache --")
    cache = LRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")
    cache.put("c", 3)  # 'b' harus terbuang (LRU)
    print(cache, "| order:", cache.ordered_keys())
    print()

    print("-- Set Operations --")
    a, b = ["alice", "bob", "carol"], ["carol", "dave"]
    print("Union       :", set_operations.union(a, b))
    print("Intersection:", set_operations.intersection(a, b))
    print()

    print("-- Deduplicator --")
    data = ["x", "y", "x", "z", "y"]
    print("Dedup result:", deduplicator.deduplicate_exact(data))
    print()

    print("-- Lookup Benchmark (Dict vs List) --")
    results = lookup_benchmarker.run_suite([1_000, 10_000], repeat=200)
    lookup_benchmarker.print_suite(results)
    print()

    print("-- Collision Report --")
    collision_tracker.print_report(collision_tracker.track(table))


def main() -> int:
    if "--demo" in sys.argv:
        run_demo()
    else:
        StoreCLI().run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
