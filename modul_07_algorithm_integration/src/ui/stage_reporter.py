"""
stage_reporter.py
Menghasilkan laporan ringkas performa tiap stage (stage profiling)
untuk mendeteksi titik lambat sistem (bottleneck).
"""

from src.pipeline.context import PipelineContext


def build_report(context: PipelineContext) -> dict:
    """Mengembalikan ringkasan performa dalam bentuk dict, siap dipakai
    untuk ekspor JSON atau ditampilkan sebagai tabel.
    """
    total_ms = sum(log.duration_ms for log in context.history)
    slowest = max(context.history, key=lambda log: log.duration_ms, default=None)

    return {
        "total_stages": len(context.history),
        "total_duration_ms": round(total_ms, 4),
        "slowest_stage": slowest.stage_name if slowest else None,
        "slowest_duration_ms": round(slowest.duration_ms, 4) if slowest else None,
        "status": "FAILED" if context.failed else "SUCCESS",
        "stages": [
            {
                "name": log.stage_name,
                "success": log.success,
                "duration_ms": round(log.duration_ms, 4),
                "message": log.message,
            }
            for log in context.history
        ],
    }


def print_report(context: PipelineContext) -> None:
    report = build_report(context)
    print("\n=== Laporan Profiling Stage ===")
    print(f"Total stage dieksekusi : {report['total_stages']}")
    print(f"Total durasi           : {report['total_duration_ms']} ms")
    print(f"Stage paling lambat    : {report['slowest_stage']} "
          f"({report['slowest_duration_ms']} ms)")
    print(f"Status akhir           : {report['status']}")
    print("================================")
