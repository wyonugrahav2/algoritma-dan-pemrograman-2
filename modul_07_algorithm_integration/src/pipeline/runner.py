"""
runner.py
Runner bertugas mengeksekusi urutan stage secara berurutan, mencatat
durasi tiap tahap (stage profiling), dan menangani mekanisme
pemulihan/pembatalan (rollback) jika terjadi kegagalan di salah satu tahap.
"""

import time
from typing import Callable, List, Tuple

from src.pipeline.context import PipelineContext


class StageExecutionError(Exception):
    """Dilempar saat sebuah stage gagal dieksekusi."""

    def __init__(self, stage_name: str, original_error: Exception):
        self.stage_name = stage_name
        self.original_error = original_error
        super().__init__(f"Stage '{stage_name}' gagal: {original_error}")


class PipelineRunner:
    """Eksekutor rantai tugas (Execution Chain).

    Setiap stage adalah callable dengan signature:
        fn(context: PipelineContext) -> (PipelineContext, message: str)

    Jika stage melempar exception dan stop_on_failure=True, pipeline
    berhenti dan context.failed diset True (rollback: payload terakhir
    yang valid tetap dipertahankan, bukan payload yang gagal diproses).
    """

    def __init__(self, stages: List[Tuple[str, Callable]], stop_on_failure: bool = True):
        self.stages = stages
        self.stop_on_failure = stop_on_failure

    def run(self, initial_payload, metadata: dict = None) -> PipelineContext:
        context = PipelineContext(payload=initial_payload, metadata=metadata or {})

        for stage_name, stage_fn in self.stages:
            start = time.perf_counter()
            try:
                new_context, message = stage_fn(context)
                duration_ms = (time.perf_counter() - start) * 1000
                new_context.record(stage_name, success=True, duration_ms=duration_ms, message=message)
                context = new_context
            except Exception as exc:  # noqa: BLE001 - sengaja luas untuk isolasi kegagalan stage
                duration_ms = (time.perf_counter() - start) * 1000
                context.record(
                    stage_name,
                    success=False,
                    duration_ms=duration_ms,
                    message=str(exc),
                )
                if self.stop_on_failure:
                    # Rollback: hentikan eksekusi, payload tetap di kondisi
                    # terakhir sebelum stage yang gagal.
                    break
                # Jika tidak stop_on_failure, lanjut ke stage berikutnya
                # dengan payload yang sama (skip stage yang gagal).
                continue

        return context
