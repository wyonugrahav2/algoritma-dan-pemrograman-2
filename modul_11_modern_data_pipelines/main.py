#!/usr/bin/env python3
"""
main.py
Entry Point — CLI Data Stream Pipeline (Modul 11: Modern Data Pipelines)

Contoh penggunaan:
    python main.py --input data.csv --output result.jsonl --format csv
    python main.py --input data.csv --output result.csv --agg-field value --group-by category
    cat log.txt | python main.py --stdin --output out.jsonl
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.sources.file_reader import read_csv_lazy, read_json_lines_lazy
from src.sources.stream_reader import read_stdin_json_lazy
from src.transformers.data_cleanser import DataCleanser
from src.transformers.enricher import Enricher
from src.transformers.aggregator import StreamingAggregator
from src.sinks.file_writer import write_csv, write_jsonl
from src.sinks.console_sink import print_stream
from src.pipeline.stream_chain import StreamChain
from src.pipeline.backpressure import BackpressureController
from src.ui.progress_tracker import ProgressTracker
from src.ui.metrics_presenter import present_summary, MemorySnapshot


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CLI Modern Data Pipeline & Stream Processor"
    )
    parser.add_argument("--input", "-i", help="Path berkas input (CSV atau JSONL)")
    parser.add_argument("--stdin", action="store_true",
                         help="Baca data dari standard input (JSONL) alih-alih berkas")
    parser.add_argument("--format", choices=["csv", "jsonl"], default="csv",
                         help="Format berkas input (default: csv)")
    parser.add_argument("--output", "-o", help="Path berkas output")
    parser.add_argument("--output-format", choices=["csv", "jsonl"], default="jsonl",
                         help="Format berkas output (default: jsonl)")
    parser.add_argument("--agg-field", help="Nama field numerik untuk diagregasi")
    parser.add_argument("--group-by", help="Nama field untuk pengelompokan agregat")
    parser.add_argument("--preview", type=int, default=5,
                         help="Jumlah baris yang ditampilkan di console bila tanpa --output")
    parser.add_argument("--no-backpressure", action="store_true",
                         help="Nonaktifkan backpressure controller")
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()

    if not args.stdin and not args.input:
        print("Error: berikan --input <file> atau gunakan --stdin", file=sys.stderr)
        return 1

    # 1. Source layer
    if args.stdin:
        source = read_stdin_json_lazy()
    elif args.format == "csv":
        source = read_csv_lazy(args.input)
    else:
        source = read_json_lines_lazy(args.input)

    # 2. Bangun pipeline (Lazy Evaluation — belum ada eksekusi di titik ini)
    cleanser = DataCleanser(drop_invalid=False)
    enricher = Enricher()
    aggregator = StreamingAggregator(
        numeric_field=args.agg_field or "value",
        group_by=args.group_by,
    )
    tracker = ProgressTracker(label="Pipeline")

    chain = StreamChain(source)
    chain.add_stage(cleanser.process)
    chain.add_stage(enricher.process)

    if not args.no_backpressure:
        bp = BackpressureController()
        chain.add_stage(bp.apply)

    if args.agg_field:
        chain.add_stage(aggregator.process)

    chain.add_stage(tracker.wrap)

    # 3. Sink layer — di sinilah eksekusi sesungguhnya dimulai (generator ditarik)
    with MemorySnapshot() as mem:
        if args.output:
            if args.output_format == "csv":
                total = write_csv(chain.run(), args.output)
            else:
                total = write_jsonl(chain.run(), args.output)
        else:
            total = print_stream(chain.run(), limit=args.preview)

    summary = {
        "Total baris diproses": tracker.count,
        "Baris valid (cleansed)": cleanser.stats["cleaned"],
        "Baris dibuang (invalid)": cleanser.stats["dropped"],
        "Baris ditulis/ditampilkan": total,
    }
    summary.update(mem.summary())
    present_summary("Ringkasan Eksekusi Pipeline", summary)

    if args.agg_field:
        print("\nRingkasan Agregasi:")
        for key, stats in aggregator.summary().items():
            print(f"  {key}: {stats}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
