"""
list_to_hash.py
Adapter Pattern: mengubah list menjadi struktur Hash Index (dict) agar
lookup keberadaan/nilai bisa dilakukan dalam O(1) pada stage selanjutnya.
"""

from typing import Any, Dict, List


class ListToHashAdapter:
    """Stage adapter: list -> hash index (dict nilai -> daftar posisi asal)."""

    name = "list_to_hash_adapter"

    def run(self, context):
        data: List[Any] = list(context.payload)
        index: Dict[Any, List[int]] = {}
        for position, value in enumerate(data):
            index.setdefault(value, []).append(position)

        message = f"List ({len(data)} elemen) diindeks menjadi {len(index)} key unik."
        new_context = context.with_payload(index)
        return new_context, message


def list_to_hash_stage(context):
    return ListToHashAdapter().run(context)
