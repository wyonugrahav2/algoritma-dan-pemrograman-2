"""
console_sink.py
Menampilkan luaran aliran data langsung ke layar CLI, baik dalam mode
ringkas (satu baris per record) maupun mode preview terbatas.
"""

from typing import Iterator, Dict, Any, Optional


def print_stream(stream: Iterator[Dict[str, Any]], limit: Optional[int] = None) -> int:
    """
    Mencetak tiap record ke stdout. Jika `limit` diberikan, hanya `limit`
    record pertama yang dicetak namun seluruh stream tetap dikonsumsi
    (agar generator hulu tuntas dieksekusi, mis. untuk keperluan agregasi).
    """
    count = 0
    for record in stream:
        if limit is None or count < limit:
            print(record)
        count += 1
    if limit is not None and count > limit:
        print(f"... ({count - limit} baris lainnya tidak ditampilkan)")
    return count
