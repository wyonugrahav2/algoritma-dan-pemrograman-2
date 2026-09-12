"""Menguji penanganan sistem saat terjadi bentrokan hash, untuk kedua strategi."""

import unittest

from src.custom_structures.custom_hash_table import CustomHashTable


class TestCollisionHandling(unittest.TestCase):
    def test_chaining_handles_many_collisions(self):
        # Kapasitas sengaja dibuat kecil agar bentrokan sering terjadi.
        table = CustomHashTable(capacity=2, strategy="chaining")
        for i in range(20):
            table.put(f"key-{i}", i)
        for i in range(20):
            self.assertEqual(table.get(f"key-{i}"), i)

    def test_open_addressing_handles_many_collisions(self):
        table = CustomHashTable(capacity=2, strategy="open_addressing")
        for i in range(20):
            table.put(f"key-{i}", i)
        for i in range(20):
            self.assertEqual(table.get(f"key-{i}"), i)

    def test_auto_resize_on_high_load_factor(self):
        table = CustomHashTable(capacity=4, strategy="chaining")
        initial_capacity = table.capacity
        for i in range(10):
            table.put(f"k{i}", i)
        self.assertGreater(table.capacity, initial_capacity)
        # Data tetap valid setelah rehash
        for i in range(10):
            self.assertEqual(table.get(f"k{i}"), i)

    def test_open_addressing_delete_then_reinsert(self):
        table = CustomHashTable(capacity=4, strategy="open_addressing")
        table.put("a", 1)
        table.put("b", 2)
        table.delete("a")
        table.put("c", 3)  # harus bisa memakai slot tombstone bekas 'a'
        self.assertEqual(table.get("b"), 2)
        self.assertEqual(table.get("c"), 3)
        self.assertIsNone(table.get("a"))


if __name__ == "__main__":
    unittest.main()
