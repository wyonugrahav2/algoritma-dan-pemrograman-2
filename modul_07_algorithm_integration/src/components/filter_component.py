"""
filter_component.py
Komponen pembersih data: menyaring entri yang tidak valid sebelum masuk
ke tahap pengolahan berikutnya (sorting, searching, dsb).
"""

from typing import Any, Callable, Iterable, List


class FilterComponent:
    """Membungkus logika filtering ke dalam antarmuka stage yang seragam.

    Sebuah stage cukup punya method .run(context) -> context, sehingga bisa
    dipasang langsung ke PipelineBuilder.
    """

    name = "filter_component"

    def __init__(self, predicate: Callable[[Any], bool] = None):
        # Default predicate: buang None dan string kosong.
        self.predicate = predicate or (lambda x: x is not None and x != "")

    def run(self, context):
        data: Iterable = context.payload
        cleaned: List[Any] = [item for item in data if self.predicate(item)]
        removed = len(list(data)) - len(cleaned) if hasattr(data, "__len__") else None
        message = f"{len(cleaned)} item lolos filter" + (
            f", {removed} item dibuang" if removed else ""
        )
        new_context = context.with_payload(cleaned)
        return new_context, message


def remove_invalid(context):
    """Fungsi stage siap pakai: hapus None, string kosong, dan NaN-like."""
    component = FilterComponent()
    return component.run(context)
