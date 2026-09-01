"""
main.py
Entry Point — Interactive Search CLI Engine.

Menghubungkan seluruh layer: query_parser (input) -> indexer (prep data)
-> algorithms (eksekusi) -> analytics (pengukuran) -> result_presenter &
step_visualizer (output).
"""

import sys
from typing import List

from config.settings import settings
from config.search_strategies import (
    STRATEGY_REGISTRY,
    get_strategy,
    recommend_strategy,
)
from src.algorithms.linear_search import SearchResult
from src.analytics.search_profiler import profile_search
from src.analytics.step_counter import compare_algorithms
from src.indexer.sorter import ensure_sorted, is_sorted, uniformity_score
from src.ui.query_parser import ParsedQuery, parse_query
from src.ui.result_presenter import (
    present_comparison_table,
    present_profile_reports,
    present_result,
)
from src.ui.step_visualizer import animate_search, render_reduction_summary


DEMO_DATA = [4, 8, 15, 16, 23, 42, 56, 67, 71, 88, 94, 101, 118, 129, 142, 156, 171, 190]


def load_dataset(query: ParsedQuery) -> List[float]:
    """Memuat dataset sesuai --source; 'demo' memakai data contoh bawaan."""
    if query.source == "demo":
        return list(DEMO_DATA)

    if query.source.endswith(".json"):
        from src.indexer.data_loader import load_from_json, coerce_numeric

        raw = load_from_json(query.source)
        return coerce_numeric(raw)

    if query.source.endswith(".csv"):
        from src.indexer.data_loader import load_from_csv, coerce_numeric

        raw = load_from_csv(query.source, column=query.column)
        return coerce_numeric(raw, field_name=query.column)

    raise ValueError(f"Format sumber data tidak didukung: {query.source}")


def run_single_algorithm(algo_key: str, data: List[float], target: float) -> SearchResult:
    strategy = get_strategy(algo_key)
    return strategy.handler(data, target)


def run_benchmark(data: List[float], target: float) -> List[SearchResult]:
    """Menjalankan seluruh algoritma terdaftar terhadap dataset yang sama."""
    results = []
    for key in STRATEGY_REGISTRY:
        results.append(run_single_algorithm(key, data, target))
    return results


def main(argv=None) -> int:
    query = parse_query(argv)

    print(f"{settings.app_name} v{settings.version}")
    print("=" * 50)

    try:
        raw_data = load_dataset(query)
    except Exception as exc:  # noqa: BLE001 - CLI top-level error boundary
        print(f"Gagal memuat data: {exc}", file=sys.stderr)
        return 1

    sorted_data = ensure_sorted(raw_data)
    data_was_sorted = is_sorted(raw_data)
    uniformity = uniformity_score(sorted_data)

    print(f"Jumlah elemen  : {len(sorted_data)}")
    print(f"Data asli sudah terurut? : {data_was_sorted}")
    print(f"Skor keseragaman (uniformity) : {round(uniformity, 3)}")

    if query.benchmark:
        results = run_benchmark(sorted_data, query.target)
        reports = compare_algorithms(results, len(sorted_data))
        print()
        print(present_comparison_table(reports))

        if settings.enable_profiler:
            print()
            profiles = [
                profile_search(get_strategy(k).handler, sorted_data, query.target)
                for k in STRATEGY_REGISTRY
            ]
            print(present_profile_reports(profiles))
        return 0

    algo_key = query.algorithm or recommend_strategy(
        n=len(sorted_data),
        is_sorted=True,
        is_uniform_distribution=uniformity >= settings.thresholds.uniformity_tolerance,
    )
    print(f"Algoritma dipakai : {get_strategy(algo_key).display_name}")

    result = run_single_algorithm(algo_key, sorted_data, query.target)

    print()
    print(present_result(result, sorted_data))
    print()
    print("Ringkasan penyusutan ruang pencarian:")
    print(render_reduction_summary(result))

    if query.visualize and settings.enable_step_visualizer:
        animate_search(sorted_data, result)

    return 0


if __name__ == "__main__":
    sys.exit(main())
