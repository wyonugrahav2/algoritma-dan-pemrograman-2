"""
test_process_logic.py
Unit test untuk fungsi transformasi dan pipeline pada process_layer.
"""

import unittest

from src.domain.exceptions import PipelineBrokenError
from src.process_layer.pipelines import Pipeline
from src.process_layer.transformers import (
    compute_statistics,
    filter_outliers,
    normalize_values,
    scale_values,
    sort_values,
)


class TestTransformers(unittest.TestCase):
    def test_normalize_values_basic(self):
        result = normalize_values([0, 5, 10])
        self.assertEqual(result, [0.0, 0.5, 1.0])

    def test_normalize_values_empty_list(self):
        self.assertEqual(normalize_values([]), [])

    def test_normalize_values_all_same(self):
        self.assertEqual(normalize_values([5, 5, 5]), [0.0, 0.0, 0.0])

    def test_compute_statistics_basic(self):
        stats = compute_statistics([1, 2, 3, 4, 5])
        self.assertEqual(stats["count"], 5)
        self.assertEqual(stats["mean"], 3.0)
        self.assertEqual(stats["min"], 1)
        self.assertEqual(stats["max"], 5)

    def test_sort_values_ascending(self):
        self.assertEqual(sort_values([3, 1, 2]), [1, 2, 3])

    def test_sort_values_descending(self):
        self.assertEqual(sort_values([3, 1, 2], descending=True), [3, 2, 1])

    def test_scale_values(self):
        self.assertEqual(scale_values([1, 2, 3], 2), [2, 4, 6])

    def test_filter_outliers_removes_extreme_value(self):
        values = [10, 11, 9, 10, 500]
        result = filter_outliers(values, threshold_stdev=1.0)
        self.assertNotIn(500, result)


class TestPipeline(unittest.TestCase):
    def test_pipeline_runs_stages_in_order(self):
        pipeline = (
            Pipeline()
            .add_stage("double", lambda values: [v * 2 for v in values])
            .add_stage("sort", sort_values)
        )
        final_output, results = pipeline.run([3, 1, 2])
        self.assertEqual(final_output, [2, 4, 6])
        self.assertEqual(len(results), 2)
        self.assertTrue(all(r.success for r in results))

    def test_pipeline_stops_on_error_by_default(self):
        def failing_stage(_value):
            raise ValueError("Kesalahan simulasi.")

        pipeline = Pipeline().add_stage("gagal", failing_stage)
        with self.assertRaises(PipelineBrokenError):
            pipeline.run([1, 2, 3])


if __name__ == "__main__":
    unittest.main()
