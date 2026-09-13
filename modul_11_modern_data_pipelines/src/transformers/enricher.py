"""
enricher.py
Menambahkan metadata pendukung ke tiap record yang mengalir melalui pipeline,
seperti timestamp pemrosesan, nomor urut baris, atau nilai turunan lainnya.
"""

import time
from typing import Iterator, Dict, Any, Callable, Optional


class Enricher:
    """Menambahkan field metadata ke tiap record secara streaming."""

    def __init__(self, extra_fields: Optional[Dict[str, Callable[[Dict], Any]]] = None):
        """
        extra_fields: mapping nama_field -> fungsi(record) -> nilai
        Contoh: {"row_upper": lambda r: r["category"].upper()}
        """
        self.extra_fields = extra_fields or {}
        self._row_counter = 0

    def enrich_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        self._row_counter += 1
        enriched = dict(record)
        enriched["_processed_at"] = time.time()
        enriched["_row_seq"] = self._row_counter
        for field_name, fn in self.extra_fields.items():
            try:
                enriched[field_name] = fn(record)
            except Exception:
                enriched[field_name] = None
        return enriched

    def process(self, stream: Iterator[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
        for record in stream:
            yield self.enrich_record(record)
