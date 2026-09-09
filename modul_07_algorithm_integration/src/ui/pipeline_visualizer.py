"""
pipeline_visualizer.py
Menampilkan status eksekusi tiap tahap secara visual di terminal CLI.
Tidak bergantung pada library eksternal (Rich dsb.) agar proyek tetap
ringan dan mudah dijalankan di lingkungan mana pun.
"""

from src.pipeline.context import PipelineContext


def render_pipeline_status(context: PipelineContext) -> str:
    """Mengembalikan string representasi visual dari riwayat eksekusi pipeline."""
    lines = ["", "=== Status Eksekusi Pipeline ==="]
    for i, log in enumerate(context.history, start=1):
        icon = "✔" if log.success else "✘"
        lines.append(
            f"  [{icon}] Stage {i}: {log.stage_name:<28} "
            f"({log.duration_ms:.3f} ms) - {log.message}"
        )

    lines.append("---------------------------------")
    if context.failed:
        lines.append(f"Hasil akhir: GAGAL -> {context.error_message}")
    else:
        lines.append("Hasil akhir: SUKSES")
    lines.append("=================================")
    return "\n".join(lines)


def print_pipeline_status(context: PipelineContext) -> None:
    print(render_pipeline_status(context))
