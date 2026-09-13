"""
test_data_integrity.py
Menguji integritas data dari baris awal hingga akhir pipeline — memastikan
tidak ada baris yang hilang, terduplikasi, atau rusak selama proses
streaming, transformasi, dan penulisan ke sink.
"""

import os
import sys
import csv
import json
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.sources.file_reader import read_csv_lazy
from src.transformers.data_cleanser import DataCleanser
from src.sinks.file_writer import write_jsonl
from src.pipeline.stream_chain import StreamChain


class TestDataIntegrity(unittest.TestCase):

    def setUp(self):
        self.input_csv = tempfile.NamedTemporaryFile(
            suffix=".csv", delete=False, mode="w"
        )
        writer = csv.writer(self.input_csv)
        writer.writerow(["id", "value", "category"])
        self.expected_ids = [str(i) for i in range(100)]
        for i in range(100):
            writer.writerow([i, i * 2, "cat"])
        self.input_csv.close()

        self.output_jsonl = tempfile.NamedTemporaryFile(
            suffix=".jsonl", delete=False
        )
        self.output_jsonl.close()

    def tearDown(self):
        os.unlink(self.input_csv.name)
        os.unlink(self.output_jsonl.name)

    def test_no_rows_lost_end_to_end(self):
        chain = StreamChain(read_csv_lazy(self.input_csv.name))
        chain.add_stage(DataCleanser(drop_invalid=False).process)

        total_written = write_jsonl(chain.run(), self.output_jsonl.name)
        self.assertEqual(total_written, 100)

        with open(self.output_jsonl.name, "r", encoding="utf-8") as f:
            lines = [json.loads(line) for line in f if line.strip()]

        self.assertEqual(len(lines), 100)
        output_ids = sorted(row["id"] for row in lines)
        self.assertEqual(output_ids, sorted(self.expected_ids))

    def test_no_duplicate_ids(self):
        chain = StreamChain(read_csv_lazy(self.input_csv.name))
        chain.add_stage(DataCleanser(drop_invalid=False).process)
        results = list(chain.run())
        ids = [r["id"] for r in results]
        self.assertEqual(len(ids), len(set(ids)), "Ditemukan id duplikat")


if __name__ == "__main__":
    unittest.main()
