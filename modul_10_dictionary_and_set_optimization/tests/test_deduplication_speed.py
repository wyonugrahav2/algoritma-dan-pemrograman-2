"""Menguji kebenaran dan kecepatan pembersihan data unik (deduplicator)."""

import time
import unittest

from src.optimizers.deduplicator import (
    deduplicate_exact,
    deduplicate_approximate,
    duplicate_ratio,
)


class TestDeduplicationSpeed(unittest.TestCase):
    def test_deduplicate_exact_preserves_order(self):
        data = ["b", "a", "b", "c", "a", "d"]
        result = deduplicate_exact(data)
        self.assertEqual(result, ["b", "a", "c", "d"])

    def test_deduplicate_exact_empty_input(self):
        self.assertEqual(deduplicate_exact([]), [])

    def test_duplicate_ratio_calculation(self):
        data = ["a", "a", "a", "b"]
        # 4 total, 2 unik -> rasio duplikat = 1 - 2/4 = 0.5
        self.assertAlmostEqual(duplicate_ratio(data), 0.5)

    def test_deduplicate_approximate_mostly_unique(self):
        data = [str(i) for i in range(5000)]
        result = deduplicate_approximate(data, expected_items=5000, false_positive_rate=0.001)
        # Dengan FP rate sangat rendah, hasil harus mendekati jumlah asli
        self.assertGreater(len(result), 4900)

    def test_large_dataset_runs_fast(self):
        data = [str(i % 1000) for i in range(100_000)]  # banyak duplikat
        start = time.perf_counter()
        result = deduplicate_exact(data)
        elapsed = time.perf_counter() - start
        self.assertEqual(len(result), 1000)
        self.assertLess(elapsed, 2.0)  # harus tetap cepat walau data besar


if __name__ == "__main__":
    unittest.main()
