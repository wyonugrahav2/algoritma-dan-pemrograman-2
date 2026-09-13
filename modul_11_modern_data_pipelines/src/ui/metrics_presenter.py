"""
metrics_presenter.py
Memvisualisasikan pemakaian RAM dan kecepatan I/O dalam bentuk ringkasan
tabel sederhana di terminal setelah pipeline selesai berjalan.
"""

import tracemalloc
from typing import Dict, Any


def format_bytes(num_bytes: float) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.2f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.2f} TB"


def present_summary(title: str, metrics: Dict[str, Any]) -> None:
    """Mencetak ringkasan metrik dalam format tabel teks sederhana."""
    width = max(len(title), max((len(f"{k}: {v}") for k, v in metrics.items()), default=0)) + 4
    print("=" * width)
    print(title)
    print("-" * width)
    for key, value in metrics.items():
        print(f"{key:<28}: {value}")
    print("=" * width)


class MemorySnapshot:
    """Context manager untuk mengukur puncak penggunaan memori (tracemalloc)."""

    def __enter__(self):
        tracemalloc.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        current, peak = tracemalloc.get_traced_memory()
        self.current = current
        self.peak = peak
        tracemalloc.stop()

    def summary(self) -> Dict[str, str]:
        return {
            "Current memory": format_bytes(self.current),
            "Peak memory": format_bytes(self.peak),
        }
