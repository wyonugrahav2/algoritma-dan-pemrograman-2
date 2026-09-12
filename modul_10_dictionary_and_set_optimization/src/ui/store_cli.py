"""
store_cli.py
Antarmuka interaktif CLI untuk mengeksekusi Key-Value Store (berbasis
CustomHashTable) dan operasi Set, sekaligus memvisualisasikan distribusi
bucket memori.

Jalankan langsung:  python -m src.ui.store_cli
"""

from __future__ import annotations
import sys

from src.custom_structures.custom_hash_table import CustomHashTable
from src.custom_structures.bloom_filter import BloomFilter
from src.custom_structures.lru_cache import LRUCache
from src.optimizers import set_operations as setops
from src.profiler import collision_tracker
from src.ui.memory_visualizer import render_bucket_distribution

HELP_TEXT = """
Perintah yang tersedia:
  put <key> <value>       Simpan pasangan key-value
  get <key>                Ambil value berdasarkan key
  del <key>                Hapus key dari store
  bloom-add <item>          Tambahkan item ke bloom filter
  bloom-check <item>       Cek kemungkinan keberadaan item di bloom filter
  cache-put <key> <value>  Simpan ke LRU cache
  cache-get <key>          Ambil dari LRU cache
  union <a,b,c> <x,y,z>    Operasi union dua himpunan (pisahkan koma)
  intersect <a,b,c> <x,y,z> Operasi intersection dua himpunan
  stats                     Tampilkan statistik bentrokan & load factor
  visualize                Tampilkan distribusi bucket memori
  help                      Tampilkan bantuan ini
  exit / quit              Keluar dari aplikasi
"""


class StoreCLI:
    def __init__(self) -> None:
        self.table = CustomHashTable(capacity=8, strategy="chaining")
        self.bloom = BloomFilter(expected_items=1000, false_positive_rate=0.01)
        self.cache = LRUCache(capacity=16)

    def dispatch(self, line: str) -> bool:
        """Kembalikan False jika user ingin keluar."""
        parts = line.strip().split()
        if not parts:
            return True

        cmd, *args = parts

        if cmd in ("exit", "quit"):
            print("Sampai jumpa!")
            return False
        elif cmd == "help":
            print(HELP_TEXT)
        elif cmd == "put" and len(args) >= 2:
            self.table.put(args[0], " ".join(args[1:]))
            print(f"OK: '{args[0]}' disimpan.")
        elif cmd == "get" and len(args) == 1:
            value = self.table.get(args[0])
            print(value if value is not None else "(tidak ditemukan)")
        elif cmd == "del" and len(args) == 1:
            ok = self.table.delete(args[0])
            print("Terhapus." if ok else "Key tidak ditemukan.")
        elif cmd == "bloom-add" and len(args) == 1:
            self.bloom.add(args[0])
            print(f"'{args[0]}' ditambahkan ke bloom filter.")
        elif cmd == "bloom-check" and len(args) == 1:
            result = self.bloom.might_contain(args[0])
            print("Mungkin ada." if result else "Pasti tidak ada.")
        elif cmd == "cache-put" and len(args) >= 2:
            self.cache.put(args[0], " ".join(args[1:]))
            print(f"OK: '{args[0]}' masuk LRU cache.")
        elif cmd == "cache-get" and len(args) == 1:
            value = self.cache.get(args[0])
            print(value if value is not None else "(cache miss)")
        elif cmd == "union" and len(args) == 2:
            a, b = args[0].split(","), args[1].split(",")
            print(sorted(setops.union(a, b)))
        elif cmd == "intersect" and len(args) == 2:
            a, b = args[0].split(","), args[1].split(",")
            print(sorted(setops.intersection(a, b)))
        elif cmd == "stats":
            report = collision_tracker.track(self.table)
            collision_tracker.print_report(report)
        elif cmd == "visualize":
            print(render_bucket_distribution(self.table))
        else:
            print(f"Perintah tidak dikenal atau argumen kurang: '{line}'. Ketik 'help'.")

        return True

    def run(self) -> None:
        print("=== Dictionary & Set Optimization — Interactive Store CLI ===")
        print("Ketik 'help' untuk daftar perintah, 'exit' untuk keluar.\n")
        while True:
            try:
                line = input("store> ")
            except (EOFError, KeyboardInterrupt):
                print("\nSampai jumpa!")
                break
            if not self.dispatch(line):
                break


def main() -> None:
    StoreCLI().run()


if __name__ == "__main__":
    sys.exit(main() or 0)
