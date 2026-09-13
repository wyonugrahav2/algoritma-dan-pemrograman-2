"""
aggregator.py
Menghitung nilai agregat (sum, avg, min, max, count) secara streaming
tanpa perlu menyimpan seluruh dataset di memori (running aggregation).
"""

from typing import Iterator, Dict, Any, Optional


class StreamingAggregator:
    """Menghitung statistik agregat berjalan (running stats) per field numerik."""

    def __init__(self, numeric_field: str, group_by: Optional[str] = None):
        self.numeric_field = numeric_field
        self.group_by = group_by
        # struktur: {group_key: {"count", "sum", "min", "max"}}
        self._stats: Dict[Any, Dict[str, float]] = {}

    def _update(self, key: Any, value: float) -> None:
        s = self._stats.setdefault(
            key, {"count": 0, "sum": 0.0, "min": float("inf"), "max": float("-inf")}
        )
        s["count"] += 1
        s["sum"] += value
        s["min"] = min(s["min"], value)
        s["max"] = max(s["max"], value)

    def process(self, stream: Iterator[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
        """
        Pass-through generator: tetap meneruskan tiap record ke tahap
        berikutnya (agar pipeline tidak terhenti), sambil memperbarui
        agregat secara internal di belakang layar.
        """
        for record in stream:
            key = record.get(self.group_by) if self.group_by else "_all"
            raw_value = record.get(self.numeric_field)
            try:
                value = float(raw_value)
                self._update(key, value)
            except (TypeError, ValueError):
                pass
            yield record

    def summary(self) -> Dict[Any, Dict[str, float]]:
        """Mengembalikan ringkasan agregat: count, sum, avg, min, max per grup."""
        result = {}
        for key, s in self._stats.items():
            avg = s["sum"] / s["count"] if s["count"] else 0.0
            result[key] = {
                "count": s["count"],
                "sum": s["sum"],
                "avg": avg,
                "min": s["min"] if s["count"] else 0.0,
                "max": s["max"] if s["count"] else 0.0,
            }
        return result
