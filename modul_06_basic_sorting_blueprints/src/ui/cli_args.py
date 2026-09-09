"""
cli_args.py
-----------
Parser perintah pengurutan dari terminal, menggunakan modul bawaan
`argparse`. Menerjemahkan argumen baris perintah menjadi objek konfigurasi
yang siap dipakai oleh main.py.
"""

import argparse

from config.sort_strategies import list_strategies


def parse_args():
    parser = argparse.ArgumentParser(
        prog="basic-sorting-blueprints",
        description="CLI Data Sorting Engine & Mutation Visualizer (Modul 06)",
    )

    parser.add_argument(
        "--algorithm",
        "-a",
        choices=list_strategies() + ["all"],
        default="all",
        help="Algoritma sorting yang ingin dijalankan (default: all).",
    )
    parser.add_argument(
        "--size",
        "-n",
        type=int,
        default=15,
        help="Ukuran array uji yang akan digenerate (default: 15).",
    )
    parser.add_argument(
        "--case",
        "-c",
        choices=["random", "nearly_sorted", "reversed"],
        default="random",
        help="Kondisi awal data uji (default: random).",
    )
    parser.add_argument(
        "--animate",
        action="store_true",
        help="Tampilkan animasi bar chart ASCII saat proses sorting berjalan.",
    )
    parser.add_argument(
        "--descending",
        action="store_true",
        help="Urutkan secara descending (default: ascending).",
    )

    return parser.parse_args()
