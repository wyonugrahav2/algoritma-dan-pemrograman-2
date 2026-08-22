"""
file_storage.py
Membaca/menyimpan state ke disk untuk keperluan persistensi sederhana
(mis. cache hasil, checkpoint pipeline).
"""

import json
from pathlib import Path
from typing import Any


def save_state(data: Any, path: str) -> Path:
    """Menyimpan objek data (harus JSON-serializable) ke berkas."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    return destination


def load_state(path: str) -> Any:
    """Memuat kembali objek data dari berkas JSON."""
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"Berkas state '{path}' tidak ditemukan.")
    return json.loads(source.read_text(encoding="utf-8"))


def state_exists(path: str) -> bool:
    """Memeriksa apakah berkas state sudah ada di disk."""
    return Path(path).exists()


def delete_state(path: str) -> bool:
    """Menghapus berkas state jika ada. Mengembalikan True jika berhasil dihapus."""
    target = Path(path)
    if target.exists():
        target.unlink()
        return True
    return False
