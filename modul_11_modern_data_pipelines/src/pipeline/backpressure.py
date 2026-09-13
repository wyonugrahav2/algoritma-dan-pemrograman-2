"""
backpressure.py
Mengendalikan laju aliran data antara pembaca (source) dan penulis (sink)
agar alokasi memori RAM tetap stabil menggunakan buffer bounded (queue).
"""

import time
from collections import deque
from typing import Iterator, Dict, Any

from config.settings import settings


class BackpressureController:
    """
    Menyisipkan buffer terbatas (bounded queue) di antara dua tahap pipeline.
    Jika buffer terisi melewati high watermark, source diberi jeda (throttle)
    hingga buffer turun ke bawah low watermark — mencegah memori membengkak
    saat producer lebih cepat dari consumer.
    """

    def __init__(self, capacity: int = None,
                 high_watermark: float = None,
                 low_watermark: float = None,
                 throttle_seconds: float = 0.01):
        self.capacity = capacity or settings.BUFFER_CAPACITY
        self.high_watermark = high_watermark or settings.BACKPRESSURE_HIGH_WATERMARK
        self.low_watermark = low_watermark or settings.BACKPRESSURE_LOW_WATERMARK
        self.throttle_seconds = throttle_seconds
        self._buffer: deque = deque()
        self._throttled_count = 0

    @property
    def fill_ratio(self) -> float:
        return len(self._buffer) / self.capacity if self.capacity else 0.0

    def apply(self, stream: Iterator[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
        """
        Generator yang menyangga stream masukan dan menerapkan jeda otomatis
        (throttling) bila buffer mendekati penuh.
        """
        is_throttling = False
        for record in stream:
            self._buffer.append(record)

            if self.fill_ratio >= self.high_watermark:
                is_throttling = True
            elif self.fill_ratio <= self.low_watermark:
                is_throttling = False

            if is_throttling:
                self._throttled_count += 1
                time.sleep(self.throttle_seconds)

            yield self._buffer.popleft()

        # Kuras sisa buffer setelah source habis
        while self._buffer:
            yield self._buffer.popleft()

    @property
    def throttled_count(self) -> int:
        return self._throttled_count
