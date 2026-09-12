"""
lru_cache.py
Implementasi Least Recently Used (LRU) Cache berkecepatan O(1) per operasi
menggunakan kombinasi Hash Map (dict) + Doubly Linked List.

Ide inti:
- dict menyimpan pemetaan key -> Node, sehingga akses node dalam O(1).
- Doubly Linked List menjaga urutan penggunaan: head = paling baru
  digunakan (Most Recently Used), tail = paling lama tidak dipakai
  (Least Recently Used). Saat cache penuh, node di tail dibuang.
"""

from __future__ import annotations
from typing import Any, Optional


class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: Any = None, value: Any = None):
        self.key = key
        self.value = value
        self.prev: Optional["_Node"] = None
        self.next: Optional["_Node"] = None


class LRUCache:
    def __init__(self, capacity: int = 128):
        if capacity <= 0:
            raise ValueError("capacity harus > 0")
        self.capacity = capacity
        self._map: dict[Any, _Node] = {}

        # Sentinel head/tail memudahkan operasi linked list tanpa None-check.
        self._head = _Node()
        self._tail = _Node()
        self._head.next = self._tail
        self._tail.prev = self._head

        self.hits = 0
        self.misses = 0

    # ------------------------------------------------------------------ #
    # Operasi linked list internal
    # ------------------------------------------------------------------ #
    def _remove(self, node: _Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_at_front(self, node: _Node) -> None:
        node.next = self._head.next
        node.prev = self._head
        self._head.next.prev = node
        self._head.next = node

    def _move_to_front(self, node: _Node) -> None:
        self._remove(node)
        self._insert_at_front(node)

    # ------------------------------------------------------------------ #
    # API publik
    # ------------------------------------------------------------------ #
    def get(self, key: Any) -> Any:
        node = self._map.get(key)
        if node is None:
            self.misses += 1
            return None
        self.hits += 1
        self._move_to_front(node)
        return node.value

    def put(self, key: Any, value: Any) -> None:
        node = self._map.get(key)
        if node is not None:
            node.value = value
            self._move_to_front(node)
            return

        if len(self._map) >= self.capacity:
            lru_node = self._tail.prev
            self._remove(lru_node)
            del self._map[lru_node.key]

        new_node = _Node(key, value)
        self._map[key] = new_node
        self._insert_at_front(new_node)

    def contains(self, key: Any) -> bool:
        return key in self._map

    def __len__(self) -> int:
        return len(self._map)

    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total else 0.0

    def ordered_keys(self) -> list:
        """Kembalikan key dari MRU ke LRU, berguna untuk visualisasi/testing."""
        keys = []
        node = self._head.next
        while node is not self._tail:
            keys.append(node.key)
            node = node.next
        return keys

    def __repr__(self) -> str:
        return f"LRUCache(size={len(self)}/{self.capacity}, hit_rate={self.hit_rate():.2%})"


if __name__ == "__main__":
    cache = LRUCache(capacity=3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    cache.get("a")          # 'a' jadi paling baru dipakai
    cache.put("d", 4)       # 'b' adalah LRU -> dibuang
    print(cache)
    print("order (MRU->LRU):", cache.ordered_keys())
    print("b masih ada?", cache.contains("b"))
