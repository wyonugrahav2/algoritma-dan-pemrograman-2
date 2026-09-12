"""Menguji keakuratan pemetaan key-value pada CustomHashTable."""

import unittest

from src.custom_structures.custom_hash_table import CustomHashTable


class TestHashCorrectness(unittest.TestCase):
    def test_put_and_get_chaining(self):
        table = CustomHashTable(capacity=4, strategy="chaining")
        table.put("a", 1)
        table.put("b", 2)
        self.assertEqual(table.get("a"), 1)
        self.assertEqual(table.get("b"), 2)

    def test_put_and_get_open_addressing(self):
        table = CustomHashTable(capacity=4, strategy="open_addressing")
        table.put("a", 1)
        table.put("b", 2)
        self.assertEqual(table.get("a"), 1)
        self.assertEqual(table.get("b"), 2)

    def test_overwrite_existing_key(self):
        table = CustomHashTable(capacity=4)
        table.put("x", 1)
        table.put("x", 2)
        self.assertEqual(table.get("x"), 2)
        self.assertEqual(table.size, 1)

    def test_missing_key_returns_default(self):
        table = CustomHashTable(capacity=4)
        self.assertIsNone(table.get("nope"))
        self.assertEqual(table.get("nope", "fallback"), "fallback")

    def test_delete_key(self):
        table = CustomHashTable(capacity=4)
        table.put("x", 1)
        self.assertTrue(table.delete("x"))
        self.assertFalse(table.contains("x"))
        self.assertFalse(table.delete("x"))  # sudah terhapus


if __name__ == "__main__":
    unittest.main()
