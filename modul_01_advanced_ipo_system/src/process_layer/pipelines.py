"""
pipelines.py
Pipeline rantai pemrosesan data (stream execution) yang menjalankan
serangkaian fungsi transformasi secara berurutan sambil mencatat hasil
setiap tahap ke dalam ProcessResult.
"""

import time
from typing import Any, Callable, List

from src.domain.exceptions import PipelineBrokenError
from src.domain.models import ProcessResult


StageFunction = Callable[[Any], Any]


class Pipeline:
    """Menjalankan rantai fungsi pemrosesan secara berurutan (sequential stream)."""

    def __init__(self):
        self._stages: List[tuple[str, StageFunction]] = []

    def add_stage(self, name: str, func: StageFunction) -> "Pipeline":
        """Menambahkan satu tahap pemrosesan ke pipeline. Mendukung method chaining."""
        self._stages.append((name, func))
        return self

    def run(self, initial_value: Any, stop_on_error: bool = True) -> tuple[Any, List[ProcessResult]]:
        """
        Menjalankan seluruh tahap secara berurutan.
        Mengembalikan (nilai_akhir, daftar_ProcessResult).
        """
        current_value = initial_value
        results: List[ProcessResult] = []

        for stage_name, stage_func in self._stages:
            start = time.perf_counter()
            try:
                current_value = stage_func(current_value)
                duration_ms = (time.perf_counter() - start) * 1000
                results.append(
                    ProcessResult(
                        stage_name=stage_name,
                        output_value=current_value,
                        success=True,
                        duration_ms=duration_ms,
                    )
                )
            except Exception as exc:  # noqa: BLE001 - sengaja generik untuk menangkap semua tahap
                duration_ms = (time.perf_counter() - start) * 1000
                results.append(
                    ProcessResult(
                        stage_name=stage_name,
                        output_value=None,
                        success=False,
                        error_message=str(exc),
                        duration_ms=duration_ms,
                    )
                )
                if stop_on_error:
                    raise PipelineBrokenError(
                        f"Pipeline terhenti pada tahap '{stage_name}': {exc}"
                    ) from exc

        return current_value, results
