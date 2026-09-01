"""
search_strategies.py
Strategy Pattern: memetakan nama strategi pencarian (string) ke
handler algoritma yang sesuai di src/algorithms/.

Modul ini menjadi "registry" tunggal yang dipakai oleh main.py
dan src/ui/query_parser.py untuk memilih algoritma secara dinamis
berdasarkan input pengguna (misal: --algo binary).
"""

from dataclasses import dataclass
from typing import Callable, Dict, List

from src.algorithms.linear_search import linear_search
from src.algorithms.binary_search import binary_search
from src.algorithms.interpolation_search import interpolation_search
from src.algorithms.exponential_search import exponential_search
from src.algorithms.hash_search import hash_search


@dataclass(frozen=True)
class StrategyMeta:
    """Metadata satu strategi pencarian untuk ditampilkan di CLI/help."""

    key: str
    display_name: str
    complexity: str
    requires_sorted_data: bool
    handler: Callable
    description: str


STRATEGY_REGISTRY: Dict[str, StrategyMeta] = {
    "linear": StrategyMeta(
        key="linear",
        display_name="Linear Search",
        complexity="O(N)",
        requires_sorted_data=False,
        handler=linear_search,
        description="Sequential scan, cocok untuk data tak terurut atau berukuran kecil.",
    ),
    "binary": StrategyMeta(
        key="binary",
        display_name="Binary Search",
        complexity="O(log N)",
        requires_sorted_data=True,
        handler=binary_search,
        description="Divide & conquer, memotong ruang pencarian menjadi setengah tiap iterasi.",
    ),
    "interpolation": StrategyMeta(
        key="interpolation",
        display_name="Interpolation Search",
        complexity="O(log log N) rata-rata",
        requires_sorted_data=True,
        handler=interpolation_search,
        description="Menebak posisi target berdasarkan distribusi nilai, optimal pada data uniform.",
    ),
    "exponential": StrategyMeta(
        key="exponential",
        display_name="Exponential Search",
        complexity="O(log N)",
        requires_sorted_data=True,
        handler=exponential_search,
        description="Menemukan rentang via pelipatgandaan bound, lalu binary search di rentang tersebut.",
    ),
    "hash": StrategyMeta(
        key="hash",
        display_name="Hash Lookup",
        complexity="O(1) rata-rata",
        requires_sorted_data=False,
        handler=hash_search,
        description="Pencarian langsung via key-value map, membutuhkan indeks hash yang sudah dibangun.",
    ),
}


def get_strategy(name: str) -> StrategyMeta:
    """Mengambil metadata strategi berdasarkan nama key (case-insensitive)."""
    key = name.strip().lower()
    if key not in STRATEGY_REGISTRY:
        available = ", ".join(STRATEGY_REGISTRY.keys())
        raise ValueError(f"Strategi '{name}' tidak dikenal. Pilihan tersedia: {available}")
    return STRATEGY_REGISTRY[key]


def list_strategies() -> List[StrategyMeta]:
    """Mengembalikan seluruh strategi yang terdaftar, untuk ditampilkan di --help."""
    return list(STRATEGY_REGISTRY.values())


def recommend_strategy(n: int, is_sorted: bool, is_uniform_distribution: bool = False) -> str:
    """
    Merekomendasikan key strategi terbaik berdasarkan karakteristik data.
    Logika ini mencerminkan analisis di docs/search_space_reduction.md
    dan docs/data_distribution_impact.md.
    """
    if not is_sorted:
        return "linear"
    if is_uniform_distribution and n >= 64:
        return "interpolation"
    if n > 10_000:
        return "exponential"
    return "binary"
