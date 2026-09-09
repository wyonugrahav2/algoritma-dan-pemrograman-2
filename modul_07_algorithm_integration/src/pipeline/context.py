"""
context.py
Menyediakan ruang penyimpanan status (shared state) yang dibawa antar-stage
dalam pipeline, tanpa mengubah data asli secara langsung (immutability by
convention: tiap stage mengembalikan salinan/hasil baru, bukan mutasi in-place
terhadap payload yang datang).
"""

from dataclasses import dataclass, field
from typing import Any, List, Dict


@dataclass
class StageLog:
    """Catatan hasil eksekusi satu stage, dipakai untuk pelaporan."""

    stage_name: str
    success: bool
    duration_ms: float
    message: str = ""


@dataclass
class PipelineContext:
    """Wadah state yang mengalir dari satu stage ke stage berikutnya.

    Attributes:
        payload: Data yang sedang diproses saat ini (berubah tiap stage).
        metadata: Informasi tambahan bebas (mis. target pencarian).
        history: Daftar StageLog untuk audit/reporting.
        failed: Flag global bila terjadi kegagalan dan pipeline dihentikan.
    """

    payload: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    history: List[StageLog] = field(default_factory=list)
    failed: bool = False
    error_message: str = ""

    def record(self, stage_name: str, success: bool, duration_ms: float, message: str = "") -> None:
        self.history.append(StageLog(stage_name, success, duration_ms, message))
        if not success:
            self.failed = True
            self.error_message = message

    def with_payload(self, new_payload: Any) -> "PipelineContext":
        """Mengembalikan context baru dengan payload yang diperbarui,
        menjaga metadata & history tetap sama (menghindari mutasi silang).
        """
        return PipelineContext(
            payload=new_payload,
            metadata=self.metadata,
            history=self.history,
            failed=self.failed,
            error_message=self.error_message,
        )
