"""
test_full_ipo_pipeline.py
Integration test untuk alur lengkap Input -> Process -> Output.
"""

import json
import tempfile
import unittest
from pathlib import Path

from src.domain.models import ExportRequest, RawInput
from src.output_layer.exporters import export_report
from src.output_layer.formatters import format_report
from src.process_layer.ipo_engine import IPOEngine


class TestFullIPOPipeline(unittest.TestCase):
    def setUp(self):
        self.engine = IPOEngine()

    def test_process_numeric_dataset_end_to_end(self):
        report = self.engine.process_numeric_dataset([5, 3, 8, 1, 9])
        self.assertTrue(report.is_successful)
        self.assertEqual(len(report.stages), 3)  # filter_outliers, sort_values, normalize_values
        self.assertIsInstance(report.final_output, list)

    def test_process_raw_inputs_end_to_end(self):
        raw_inputs = [RawInput(raw_value=str(v)) for v in ["10", "20", "30", "5"]]
        report = self.engine.process_raw_inputs(raw_inputs)
        self.assertTrue(report.is_successful)

    def test_format_report_json_is_valid_json(self):
        report = self.engine.process_numeric_dataset([1, 2, 3])
        json_output = format_report(report, "json")
        parsed = json.loads(json_output)
        self.assertIn("final_output", parsed)

    def test_export_report_to_json_file(self):
        report = self.engine.process_numeric_dataset([1, 2, 3, 4])
        with tempfile.TemporaryDirectory() as tmp_dir:
            destination_path = str(Path(tmp_dir) / "hasil.json")
            request = ExportRequest(
                file_format="json",
                destination_path=destination_path,
                payload=None,
            )
            result_path = export_report(request, report)
            self.assertTrue(result_path.exists())
            content = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertIn("final_output", content)

    def test_export_report_to_csv_file(self):
        report = self.engine.process_numeric_dataset([1, 2, 3, 4])
        with tempfile.TemporaryDirectory() as tmp_dir:
            destination_path = str(Path(tmp_dir) / "hasil.csv")
            request = ExportRequest(
                file_format="csv",
                destination_path=destination_path,
                payload=None,
            )
            result_path = export_report(request, report)
            self.assertTrue(result_path.exists())
            self.assertGreater(result_path.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
