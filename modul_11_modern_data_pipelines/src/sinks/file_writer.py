"""
file_writer.py
Penulis data ter-buffer ke berkas luaran (CSV/JSON) menggunakan pendekatan
generator-consuming agar konsumsi memori tetap stabil pada dataset besar.
"""

import csv
import json
from typing import Iterator, Dict, Any, List, Optional

from config.settings import settings


def write_csv(stream: Iterator[Dict[str, Any]], path: str,
              fieldnames: Optional[List[str]] = None,
              buffer_size: int = None) -> int:
    """
    Menulis stream record ke berkas CSV dengan buffered write.
    Mengembalikan jumlah baris yang berhasil ditulis.
    """
    buffer_size = buffer_size or settings.CHUNK_SIZE
    count = 0
    buffer: List[Dict[str, Any]] = []
    writer = None

    with open(path, "w", encoding=settings.FILE_ENCODING, newline="") as f:
        for record in stream:
            if writer is None:
                cols = fieldnames or list(record.keys())
                writer = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
                writer.writeheader()
            buffer.append(record)
            count += 1
            if len(buffer) >= buffer_size:
                writer.writerows(buffer)
                buffer.clear()
        if writer is not None and buffer:
            writer.writerows(buffer)
    return count


def write_jsonl(stream: Iterator[Dict[str, Any]], path: str,
                 buffer_size: int = None) -> int:
    """Menulis stream record ke berkas JSON Lines (.jsonl) secara buffered."""
    buffer_size = buffer_size or settings.CHUNK_SIZE
    count = 0
    buffer: List[str] = []

    with open(path, "w", encoding=settings.FILE_ENCODING) as f:
        for record in stream:
            buffer.append(json.dumps(record, ensure_ascii=False))
            count += 1
            if len(buffer) >= buffer_size:
                f.write("\n".join(buffer) + "\n")
                buffer.clear()
        if buffer:
            f.write("\n".join(buffer) + "\n")
    return count
