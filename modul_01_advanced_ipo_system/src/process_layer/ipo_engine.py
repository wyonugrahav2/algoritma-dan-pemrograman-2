"""
ipo_engine.py
Engine utama yang mengorkestrasi input layer, pipeline pemrosesan,
dan menghasilkan PipelineReport akhir untuk dikirim ke output layer.
"""

import time
from typing import List

from src.domain.exceptions import ProcessExecutionError
from src.domain.models import PipelineReport, RawInput
from src.process_layer.pipelines import Pipeline
from src.process_layer.transformers import (
    compute_statistics,
    filter_outliers,
    normalize_values,
    sort_values,
)


class IPOEngine:
    """Otak eksekusi utama sistem: menerima data mentah, memprosesnya, dan
    menghasilkan laporan pemrosesan yang lengkap."""

    def __init__(self):
        self._pipeline = self._build_default_pipeline()

    @staticmethod
    def _build_default_pipeline() -> Pipeline:
        """Membangun pipeline analisis numerik standar."""
        return (
            Pipeline()
            .add_stage("filter_outliers", filter_outliers)
            .add_stage("sort_values", sort_values)
            .add_stage("normalize_values", normalize_values)
        )

    def process_numeric_dataset(self, values: List[float]) -> PipelineReport:
        """Menjalankan pipeline lengkap terhadap dataset numerik dan
        mengembalikan PipelineReport berisi ringkasan setiap tahap."""
        if not values:
            raise ProcessExecutionError("Dataset kosong tidak dapat diproses.")

        start = time.perf_counter()
        final_output, stage_results = self._pipeline.run(values)
        stats = compute_statistics(values)
        total_duration_ms = (time.perf_counter() - start) * 1000

        return PipelineReport(
            input_summary=f"{len(values)} nilai numerik | statistik: {stats}",
            stages=tuple(stage_results),
            final_output=final_output,
            total_duration_ms=total_duration_ms,
        )

    def process_raw_inputs(self, raw_inputs: List[RawInput]) -> PipelineReport:
        """Alur end-to-end: menerima RawInput mentah, mengonversinya menjadi
        angka, lalu menjalankan pipeline analisis numerik."""
        from src.input_layer.parsers import parse_to_float

        values: List[float] = []
        for raw in raw_inputs:
            validated = parse_to_float(raw)
            values.append(validated.value)

        return self.process_numeric_dataset(values)
