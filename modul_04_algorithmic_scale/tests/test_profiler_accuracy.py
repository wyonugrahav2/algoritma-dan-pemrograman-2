"""
test_profiler_accuracy.py
Memastikan timer profiler dan memory profiler bekerja presisi,
serta memvalidasi bahwa complexity_analyzer dapat menebak kelas
Big-O dengan benar dari data waktu yang terkontrol (sintetis, bukan
hasil benchmark nyata) agar pengujian ini deterministik.
"""

import time
import unittest

from src.profiler.time_profiler import profile_execution_time, ExecutionTimeoutError
from src.profiler.memory_profiler import profile_memory_usage
from src.profiler.complexity_analyzer import classify_series, ComplexityClass
from src.algorithms.linear_ops import sum_all
from src.algorithms.quadratic_ops import has_duplicate_naive


class TestTimeProfiler(unittest.TestCase):
    def test_measures_positive_duration(self):
        result = profile_execution_time(sum_all, n=1000, args=([1] * 1000,), repeats=2)
        self.assertGreaterEqual(result.mean_seconds, 0.0)
        self.assertEqual(len(result.durations_seconds), 2)
        self.assertFalse(result.timed_out)

    def test_repeats_respected(self):
        result = profile_execution_time(sum_all, n=100, args=(list(range(100)),), repeats=5)
        self.assertEqual(len(result.durations_seconds), 5)

    def test_timeout_detected(self):
        def _slow_function():
            time.sleep(0.5)

        result = profile_execution_time(_slow_function, n=1, repeats=1, timeout_seconds=0.05)
        self.assertTrue(result.timed_out)


class TestMemoryProfiler(unittest.TestCase):
    def test_measures_nonnegative_memory(self):
        result = profile_memory_usage(has_duplicate_naive, n=200, args=(list(range(200)),))
        self.assertGreaterEqual(result.peak_bytes, 0)
        self.assertGreaterEqual(result.peak_mb, 0.0)

    def test_flags_exceeded_limit(self):
        def _allocate_list():
            return [0] * (10 ** 6)

        result = profile_memory_usage(_allocate_list, n=1, max_memory_mb=0.001)
        self.assertTrue(result.exceeded_limit)


class TestComplexityAnalyzer(unittest.TestCase):
    def test_detects_constant_growth(self):
        # Waktu konstan di semua N -> harus terdeteksi O(1)
        measurements = [(10, 0.001), (100, 0.0011), (1000, 0.00105), (10000, 0.00102)]
        estimate = classify_series(measurements)
        self.assertEqual(estimate.predicted_class, ComplexityClass.CONSTANT)

    def test_detects_linear_growth(self):
        # Waktu proporsional dengan N -> harus terdeteksi O(N)
        measurements = [(1000, 0.001), (2000, 0.002), (4000, 0.004), (8000, 0.008)]
        estimate = classify_series(measurements)
        self.assertEqual(estimate.predicted_class, ComplexityClass.LINEAR)

    def test_detects_quadratic_growth(self):
        # Waktu proporsional dengan N^2 -> harus terdeteksi O(N^2)
        measurements = [(1000, 0.001), (2000, 0.004), (4000, 0.016), (8000, 0.064)]
        estimate = classify_series(measurements)
        self.assertEqual(estimate.predicted_class, ComplexityClass.QUADRATIC)

    def test_insufficient_data_returns_unknown(self):
        estimate = classify_series([(100, 0.001)])
        self.assertEqual(estimate.predicted_class, ComplexityClass.UNKNOWN)
        self.assertEqual(estimate.confidence, 0.0)


if __name__ == "__main__":
    unittest.main()
