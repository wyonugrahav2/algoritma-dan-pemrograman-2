"""
stream_reader.py
Pembaca aliran data secara real-time dari standard input (stdin) atau
berkas log sistem, digunakan untuk skenario tail -f / streaming log.
"""

import sys
import time
import json
from typing import Iterator, Dict, Any, Optional


def read_stdin_lazy() -> Iterator[str]:
    """Membaca baris demi baris dari stdin secara lazy hingga EOF."""
    for line in sys.stdin:
        line = line.rstrip("\n")
        if line:
            yield line


def read_stdin_json_lazy() -> Iterator[Dict[str, Any]]:
    """Membaca stdin sebagai aliran objek JSON per baris (JSONL over stdin)."""
    for line in read_stdin_lazy():
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            # Baris rusak/tidak valid diabaikan agar stream tidak terhenti
            continue


def tail_log(path: str, poll_interval: float = 0.5,
             stop_after_idle: Optional[float] = None) -> Iterator[str]:
    """
    Mengikuti pertumbuhan berkas log secara real-time (mirip `tail -f`).

    stop_after_idle: jika diset (detik), generator berhenti otomatis setelah
    tidak ada baris baru selama durasi tersebut — berguna untuk pengujian
    otomatis agar tidak menunggu tanpa batas.
    """
    idle_time = 0.0
    with open(path, "r", encoding="utf-8") as f:
        f.seek(0, 2)  # loncat ke akhir berkas
        while True:
            line = f.readline()
            if line:
                idle_time = 0.0
                yield line.rstrip("\n")
            else:
                time.sleep(poll_interval)
                idle_time += poll_interval
                if stop_after_idle is not None and idle_time >= stop_after_idle:
                    return
