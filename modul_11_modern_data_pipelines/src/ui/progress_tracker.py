"""
progress_tracker.py
Menampilkan indikator kemajuan real-time dan kecepatan pemrosesan
(throughput rows/sec) selama pipeline berjalan.
"""

import sys
import time
from typing import Iterator, Dict, Any, Optional

from config.settings import settings


class ProgressTracker:
    """Membungkus stream untuk melaporkan progres tanpa mengubah datanya."""

    def __init__(self, total: Optional[int] = None,
                 report_interval: int = None, label: str = "Processing"):
        self.total = total
        self.report_interval = report_interval or settings.PROGRESS_REPORT_INTERVAL
        self.label = label
        self._count = 0
        self._start_time = None

    def wrap(self, stream: Iterator[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
        self._start_time = time.perf_counter()
        for record in stream:
            self._count += 1
            if self._count % self.report_interval == 0:
                self._report()
            yield record
        self._report(final=True)

    def _report(self, final: bool = False) -> None:
        elapsed = max(time.perf_counter() - self._start_time, 1e-9)
        throughput = self._count / elapsed
        progress_str = (
            f"[{self.label}] {self._count} baris"
            + (f" / {self.total}" if self.total else "")
            + f" | {throughput:,.1f} rows/sec | {elapsed:.2f}s"
        )
        end = "\n" if final else "\r"
        print(progress_str, end=end, file=sys.stderr, flush=True)

    @property
    def count(self) -> int:
        return self._count
