"""
data_cleanser.py
Komponen pembersih dan pemvalidasi tipe data pada aliran data yang berjalan.
Beroperasi sebagai generator agar tetap kompatibel dengan Lazy Evaluation
Pipeline (stream_chain.py).
"""

from typing import Iterator, Dict, Any, Optional

from config.pipeline_configs import PipelineSchema, DEFAULT_SCHEMA


class DataCleanser:
    """Membersihkan dan memvalidasi tiap record berdasarkan skema."""

    def __init__(self, schema: Optional[PipelineSchema] = None,
                 drop_invalid: bool = True):
        self.schema = schema or DEFAULT_SCHEMA
        self.drop_invalid = drop_invalid
        self.stats = {"processed": 0, "cleaned": 0, "dropped": 0}

    def _coerce(self, value: Any, dtype: type, default: Any) -> Any:
        if value is None or value == "":
            return default
        try:
            return dtype(value)
        except (ValueError, TypeError):
            return default

    def clean_record(self, record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        cleaned: Dict[str, Any] = {}
        for f in self.schema.fields:
            raw = record.get(f.name)
            if raw is None and f.required and self.drop_invalid:
                return None
            cleaned[f.name] = self._coerce(raw, f.dtype, f.default)
        return cleaned

    def process(self, stream: Iterator[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
        """Generator yang membersihkan tiap record secara streaming."""
        for record in stream:
            self.stats["processed"] += 1
            cleaned = self.clean_record(record)
            if cleaned is None:
                self.stats["dropped"] += 1
                continue
            self.stats["cleaned"] += 1
            yield cleaned
