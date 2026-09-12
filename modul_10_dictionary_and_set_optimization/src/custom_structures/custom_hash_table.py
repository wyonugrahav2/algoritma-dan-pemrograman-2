"""
custom_hash_table.py
Implementasi Hash Table dari nol untuk mempelajari kalkulasi indeks
(index = hash(key) % capacity) dan mekanisme rehashing.

Mendukung dua strategi penanganan bentrokan:
- "chaining"        : setiap bucket adalah list of [key, value]
- "open_addressing" : linear probing dengan tombstone untuk delete
"""

from __future__ import annotations
from typing import Any, Callable, Iterator, List, Optional, Tuple

try:
    from config.hash_functions import get_hash_function
    from config.settings import (
        INITIAL_CAPACITY,
        LOAD_FACTOR_THRESHOLD,
        RESIZE_MULTIPLIER,
        COLLISION_STRATEGY,
    )
except ImportError:  # fallback jika dijalankan tanpa root project di sys.path
    def get_hash_function(name: str = "fnv1a") -> Callable[[str], int]:
        return lambda k: hash(k) & 0xFFFFFFFF

    INITIAL_CAPACITY = 8
    LOAD_FACTOR_THRESHOLD = 0.7
    RESIZE_MULTIPLIER = 2
    COLLISION_STRATEGY = "chaining"


_TOMBSTONE = object()  # marker slot yang sudah dihapus (open addressing)


class CustomHashTable:
    """Hash table edukatif dengan chaining atau open addressing."""

    def __init__(
        self,
        capacity: int = INITIAL_CAPACITY,
        strategy: str = COLLISION_STRATEGY,
        hash_function_name: str = "fnv1a",
    ) -> None:
        if capacity <= 0:
            raise ValueError("capacity harus > 0")
        if strategy not in ("chaining", "open_addressing"):
            raise ValueError("strategy harus 'chaining' atau 'open_addressing'")

        self._capacity = capacity
        self._strategy = strategy
        self._hash_fn = get_hash_function(hash_function_name)
        self._size = 0
        self.collision_count = 0  # dipakai oleh collision_tracker.py

        if strategy == "chaining":
            self._buckets: List[List[Tuple[str, Any]]] = [[] for _ in range(capacity)]
        else:
            self._slots: List[Any] = [None] * capacity  # None = kosong

    # ------------------------------------------------------------------ #
    # Properti dasar
    # ------------------------------------------------------------------ #
    @property
    def size(self) -> int:
        return self._size

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def load_factor(self) -> float:
        return self._size / self._capacity

    def _index_for(self, key: str, capacity: Optional[int] = None) -> int:
        cap = capacity if capacity is not None else self._capacity
        return self._hash_fn(str(key)) % cap

    # ------------------------------------------------------------------ #
    # API publik: put / get / delete / contains
    # ------------------------------------------------------------------ #
    def put(self, key: str, value: Any) -> None:
        if self._strategy == "chaining":
            self._put_chaining(key, value)
        else:
            self._put_open_addressing(key, value)

        if self.load_factor > LOAD_FACTOR_THRESHOLD:
            self._resize()

    def get(self, key: str, default: Any = None) -> Any:
        if self._strategy == "chaining":
            index = self._index_for(key)
            for k, v in self._buckets[index]:
                if k == key:
                    return v
            return default
        else:
            idx = self._probe_index(key)
            if idx is not None and self._slots[idx] is not None and self._slots[idx] is not _TOMBSTONE:
                return self._slots[idx][1]
            return default

    def delete(self, key: str) -> bool:
        if self._strategy == "chaining":
            index = self._index_for(key)
            bucket = self._buckets[index]
            for i, (k, _) in enumerate(bucket):
                if k == key:
                    bucket.pop(i)
                    self._size -= 1
                    return True
            return False
        else:
            idx = self._probe_index(key)
            if idx is not None and self._slots[idx] not in (None, _TOMBSTONE):
                self._slots[idx] = _TOMBSTONE
                self._size -= 1
                return True
            return False

    def contains(self, key: str) -> bool:
        _MISSING = object()
        return self.get(key, _MISSING) is not _MISSING

    # ------------------------------------------------------------------ #
    # Strategi: Chaining
    # ------------------------------------------------------------------ #
    def _put_chaining(self, key: str, value: Any) -> None:
        index = self._index_for(key)
        bucket = self._buckets[index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        if bucket:  # bucket sudah terisi -> ini bentrokan
            self.collision_count += 1
        bucket.append((key, value))
        self._size += 1

    # ------------------------------------------------------------------ #
    # Strategi: Open Addressing (Linear Probing)
    # ------------------------------------------------------------------ #
    def _put_open_addressing(self, key: str, value: Any) -> None:
        index = self._index_for(key)
        start = index
        first_tombstone = None
        probes = 0
        while self._slots[index] is not None:
            if self._slots[index] is _TOMBSTONE:
                if first_tombstone is None:
                    first_tombstone = index
            elif self._slots[index][0] == key:
                self._slots[index] = (key, value)
                return
            else:
                probes += 1
            index = (index + 1) % self._capacity
            if index == start:
                raise RuntimeError("Hash table penuh, resize seharusnya sudah terjadi")
        if probes > 0:
            self.collision_count += 1
        target = first_tombstone if first_tombstone is not None else index
        self._slots[target] = (key, value)
        self._size += 1

    def _probe_index(self, key: str) -> Optional[int]:
        index = self._index_for(key)
        start = index
        while self._slots[index] is not None:
            if self._slots[index] is not _TOMBSTONE and self._slots[index][0] == key:
                return index
            index = (index + 1) % self._capacity
            if index == start:
                break
        return None

    # ------------------------------------------------------------------ #
    # Rehashing
    # ------------------------------------------------------------------ #
    def _resize(self) -> None:
        old_items = list(self.items())
        self._capacity *= RESIZE_MULTIPLIER
        self._size = 0
        self.collision_count = 0
        if self._strategy == "chaining":
            self._buckets = [[] for _ in range(self._capacity)]
        else:
            self._slots = [None] * self._capacity
        for k, v in old_items:
            self.put(k, v)

    # ------------------------------------------------------------------ #
    # Iterasi
    # ------------------------------------------------------------------ #
    def items(self) -> Iterator[Tuple[str, Any]]:
        if self._strategy == "chaining":
            for bucket in self._buckets:
                for k, v in bucket:
                    yield k, v
        else:
            for slot in self._slots:
                if slot is not None and slot is not _TOMBSTONE:
                    yield slot

    def keys(self) -> Iterator[str]:
        for k, _ in self.items():
            yield k

    def values(self) -> Iterator[Any]:
        for _, v in self.items():
            yield v

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return (
            f"CustomHashTable(strategy={self._strategy!r}, size={self._size}, "
            f"capacity={self._capacity}, load_factor={self.load_factor:.2f})"
        )


if __name__ == "__main__":
    table = CustomHashTable(capacity=4, strategy="chaining")
    for i in range(10):
        table.put(f"key-{i}", i * i)
    print(table)
    print("key-3 ->", table.get("key-3"))
    print("collisions:", table.collision_count)
