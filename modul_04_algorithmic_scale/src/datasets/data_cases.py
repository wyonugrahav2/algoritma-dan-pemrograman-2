"""
data_cases.py
Menyediakan skenario data Best Case, Average Case, dan Worst Case
untuk menguji konsistensi kinerja algoritma terhadap urutan data awal.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List

from src.datasets.generators import (
    generate_random_integers,
    generate_reversed_integers,
    generate_sorted_integers,
)


class CaseType(str, Enum):
    BEST = "best_case"
    AVERAGE = "average_case"
    WORST = "worst_case"


@dataclass
class DataCase:
    """Bungkusan data uji beserta metadatanya."""
    case_type: CaseType
    n: int
    data: List[int]

    @property
    def label(self) -> str:
        mapping = {
            CaseType.BEST: "Best Case (terurut sempurna)",
            CaseType.AVERAGE: "Average Case (acak)",
            CaseType.WORST: "Worst Case (terbalik total)",
        }
        return mapping[self.case_type]


def build_best_case(n: int) -> DataCase:
    """Data sudah terurut naik sempurna — biasanya skenario tercepat untuk sorting."""
    return DataCase(case_type=CaseType.BEST, n=n, data=generate_sorted_integers(n))


def build_average_case(n: int, seed: int = None) -> DataCase:
    """Data acak — merepresentasikan kondisi nyata rata-rata."""
    return DataCase(case_type=CaseType.AVERAGE, n=n, data=generate_random_integers(n, seed=seed))


def build_worst_case(n: int) -> DataCase:
    """Data terbalik total — biasanya skenario terlambat untuk sorting berbasis perbandingan."""
    return DataCase(case_type=CaseType.WORST, n=n, data=generate_reversed_integers(n))


def build_all_cases(n: int, seed: int = None) -> List[DataCase]:
    """Mengembalikan ketiga skenario (best, average, worst) sekaligus untuk N tertentu."""
    return [
        build_best_case(n),
        build_average_case(n, seed=seed),
        build_worst_case(n),
    ]
