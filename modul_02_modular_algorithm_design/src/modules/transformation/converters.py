"""
Fungsi-fungsi konversi format data.

Terpisah dari cleansers.py karena tanggung jawabnya berbeda:
cleansers.py membersihkan data, converters.py mengubah bentuk/format data.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List


def to_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, default=str)


def from_json(text: str) -> Any:
    return json.loads(text)


def list_of_dicts_to_columns(rows: List[Dict[str, Any]]) -> Dict[str, List[Any]]:
    """Ubah list of dict (row-oriented) menjadi dict of list (column-oriented)."""
    if not rows:
        return {}
    columns: Dict[str, List[Any]] = {key: [] for key in rows[0].keys()}
    for row in rows:
        for key in columns:
            columns[key].append(row.get(key))
    return columns


def columns_to_list_of_dicts(columns: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
    """Kebalikan dari list_of_dicts_to_columns."""
    if not columns:
        return []
    length = len(next(iter(columns.values())))
    return [
        {key: values[i] for key, values in columns.items()}
        for i in range(length)
    ]
