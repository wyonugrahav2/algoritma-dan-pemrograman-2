"""
query_parser.py
Memproses argumen pencarian dari baris perintah terminal (CLI) menjadi
struktur data yang siap dikonsumsi oleh main.py.
"""

import argparse
from dataclasses import dataclass
from typing import Optional

from config.search_strategies import STRATEGY_REGISTRY


@dataclass
class ParsedQuery:
    """Hasil parsing argumen CLI menjadi query pencarian yang terstruktur."""

    source: str  # path ke berkas data, atau "demo" untuk data contoh
    target: float
    algorithm: Optional[str]  # None -> auto-recommend
    benchmark: bool
    visualize: bool
    column: str


def build_arg_parser() -> argparse.ArgumentParser:
    """Membangun argparse.ArgumentParser untuk CLI Search Engine."""
    available_algos = ", ".join(STRATEGY_REGISTRY.keys())

    parser = argparse.ArgumentParser(
        prog="search-anatomy",
        description=(
            "CLI Search Engine & Search Space Inspector — membedah anatomi "
            "internal algoritma pencarian (penyusutan ruang pencarian, "
            "pointer tracking, dan jumlah perbandingan)."
        ),
    )
    parser.add_argument(
        "--source",
        default="demo",
        help="Path ke berkas data (.json/.csv), atau 'demo' untuk data contoh.",
    )
    parser.add_argument(
        "--target",
        type=float,
        required=True,
        help="Nilai target yang dicari.",
    )
    parser.add_argument(
        "--algo",
        choices=list(STRATEGY_REGISTRY.keys()),
        default=None,
        help=f"Algoritma pencarian yang dipakai ({available_algos}). "
        "Jika tidak diisi, sistem akan merekomendasikan otomatis.",
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Jalankan seluruh algoritma sekaligus dan bandingkan performanya.",
    )
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Tampilkan animasi visual pergeseran pointer di terminal.",
    )
    parser.add_argument(
        "--column",
        default="value",
        help="Nama kolom yang dijadikan nilai pencarian jika --source berupa CSV.",
    )
    return parser


def parse_query(argv: Optional[list] = None) -> ParsedQuery:
    """Mem-parsing sys.argv (atau `argv` yang diberikan) menjadi ParsedQuery."""
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    return ParsedQuery(
        source=args.source,
        target=args.target,
        algorithm=args.algo,
        benchmark=args.benchmark,
        visualize=args.visualize,
        column=args.column,
    )
