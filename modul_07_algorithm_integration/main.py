"""
main.py
Entry Point (Interactive Pipeline CLI Exec) untuk Modul 07:
Algorithm Integration Blueprint.

Contoh pemakaian:
    python main.py --route clean_sort_search --target 42
    python main.py --route sort_to_tree
    python main.py --route dedupe_to_hash
"""

import argparse
import random
import sys

from config.pipeline_routes import resolve_route
from config.settings import DEFAULT_SETTINGS
from src.pipeline.builder import build_from_route
from src.ui.pipeline_visualizer import print_pipeline_status
from src.ui.stage_reporter import print_report


def generate_sample_data(size: int = 15, with_noise: bool = True):
    data = [random.randint(1, 100) for _ in range(size)]
    if with_noise:
        # Sisipkan beberapa entri "kotor" untuk didemokan oleh filter_component.
        data = data[:5] + [None, "", None] + data[5:]
    return data


def parse_args():
    parser = argparse.ArgumentParser(
        description="CLI Data Pipeline & Multi-Algorithm Orchestrator (Modul 07)"
    )
    parser.add_argument(
        "--route",
        default="clean_sort_search",
        help="Nama route pipeline yang terdaftar di config/pipeline_routes.py",
    )
    parser.add_argument(
        "--target",
        type=int,
        default=None,
        help="Nilai yang dicari (dipakai oleh stage search:binary)",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=15,
        help="Jumlah elemen data sampel yang dibangkitkan",
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Lanjutkan pipeline meski satu stage gagal (skip stage tsb.)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        stage_names = resolve_route(args.route)
    except KeyError as exc:
        print(f"[ERROR] {exc}")
        sys.exit(1)

    data = generate_sample_data(size=args.size)
    print(f"Route dipilih   : {args.route}")
    print(f"Stage terpasang : {stage_names}")
    print(f"Data awal (sampel {len(data)} elemen): {data[:DEFAULT_SETTINGS.preview_limit]} ...")

    pipeline = build_from_route(stage_names, stop_on_failure=not args.continue_on_error)

    metadata = {}
    if args.target is not None:
        metadata["search_target"] = args.target

    context = pipeline.run(initial_payload=data, metadata=metadata)

    print_pipeline_status(context)
    print_report(context)

    preview = context.payload
    if isinstance(preview, list):
        preview = preview[: DEFAULT_SETTINGS.preview_limit]
    print(f"\nPayload akhir (preview): {preview}")

    if "search_result" in context.metadata:
        print(f"Hasil pencarian target={args.target}: indeks {context.metadata['search_result']}")


if __name__ == "__main__":
    main()
