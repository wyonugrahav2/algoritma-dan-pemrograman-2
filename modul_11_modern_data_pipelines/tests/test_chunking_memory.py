"""
test_chunking_memory.py
Menguji bahwa pemrosesan berkas besar tidak membuat konsumsi memori
membengkak linear terhadap jumlah baris (karena pendekatan streaming).
"""

import os
import sys
import csv
import tempfile
import tracemalloc
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.sources.file_reader import read_csv_lazy, read_chunks
from src.pipeline.stream_chain import StreamChain
from src.transformers.data_cleanser import DataCleanser


def _make_large_csv(path: str, n_rows: int) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "value", "category"])
        for i in range(n_rows):
            writer.writerow([i, i * 1.5, "cat_%d" % (i % 5)])


class TestChunkingMemory(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            suffix=".csv", delete=False, mode="w"
        )
        self.tmp.close()
        _make_large_csv(self.tmp.name, n_rows=20000)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_read_chunks_groups_correctly(self):
        stream = read_csv_lazy(self.tmp.name)
        chunks = list(read_chunks(stream, chunk_size=1000))
        total_rows = sum(len(c) for c in chunks)
        self.assertEqual(total_rows, 20000)
        self.assertEqual(len(chunks), 20)  # 20000 / 1000

    def test_memory_stays_bounded_during_streaming(self):
        """
        Memori puncak saat streaming 20.000 baris tidak boleh proporsional
        dengan memuat seluruh dataset ke list Python sekaligus.
        """
        tracemalloc.start()

        chain = StreamChain(read_csv_lazy(self.tmp.name))
        chain.add_stage(DataCleanser(drop_invalid=False).process)

        count = 0
        for _ in chain.run():
            count += 1

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        self.assertEqual(count, 20000)
        # Sanity bound: pemrosesan streaming 20rb baris sederhana semestinya
        # jauh di bawah 50MB peak — bukan angka presisi, hanya guard kasar.
        self.assertLess(peak, 50 * 1024 * 1024)


if __name__ == "__main__":
    unittest.main()
