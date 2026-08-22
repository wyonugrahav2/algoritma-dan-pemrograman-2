"""
models.py
Entitas data murni (Data Transfer Objects) untuk domain IPO.
Tidak memiliki dependensi eksternal (framework, I/O, dsb).
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class InputDataType(Enum):
    """Tipe data masukan yang diizinkan oleh sistem."""
    INTEGER = "integer"
    FLOAT = "float"
    STRING = "string"
    LIST = "list"


@dataclass(frozen=True)
class RawInput:
    """Representasi masukan mentah dari pengguna sebelum divalidasi."""
    raw_value: str
    source: str = "cli"
    received_at: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class ValidatedInput:
    """Masukan yang sudah lolos validasi dan siap diparsing."""
    value: Any
    data_type: InputDataType
    original: RawInput


@dataclass(frozen=True)
class ProcessResult:
    """Hasil dari satu tahap pemrosesan di dalam pipeline."""
    stage_name: str
    output_value: Any
    success: bool
    error_message: Optional[str] = None
    duration_ms: float = 0.0


@dataclass(frozen=True)
class PipelineReport:
    """Ringkasan lengkap dari seluruh rantai pemrosesan IPO."""
    input_summary: str
    stages: tuple[ProcessResult, ...]
    final_output: Any
    total_duration_ms: float
    generated_at: datetime = field(default_factory=datetime.now)

    @property
    def is_successful(self) -> bool:
        return all(stage.success for stage in self.stages)


@dataclass(frozen=True)
class ExportRequest:
    """Permintaan ekspor hasil ke berkas eksternal."""
    file_format: str
    destination_path: str
    payload: Any
