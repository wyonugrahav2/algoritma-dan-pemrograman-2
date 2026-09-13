"""
test_generator_pipeline.py
Menguji bahwa seluruh tahap pipeline benar-benar bersifat lazy (generator),
bukan struktur data yang langsung dieksekusi penuh saat dibuat.
"""

import os
import sys
import types
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipeline.stream_chain import StreamChain
from src.transformers.data_cleanser import DataCleanser
from src.transformers.enricher import Enricher


def sample_source():
    for i in range(5):
        yield {"id": str(i), "value": str(i * 10), "category": "A"}


class TestGeneratorPipeline(unittest.TestCase):

    def test_stages_are_generators(self):
        cleanser = DataCleanser(drop_invalid=False)
        result = cleanser.process(sample_source())
        self.assertIsInstance(result, types.GeneratorType)

    def test_chain_is_lazy_until_consumed(self):
        """Pipeline tidak boleh mengeksekusi apa pun sampai di-iterasi."""
        execution_flag = {"touched": False}

        def tracking_source():
            for i in range(3):
                execution_flag["touched"] = True
                yield {"id": str(i)}

        chain = StreamChain(tracking_source())
        chain.add_stage(DataCleanser(drop_invalid=False).process)
        chain.add_stage(Enricher().process)

        pipeline = chain.run()  # belum dikonsumsi
        self.assertFalse(execution_flag["touched"],
                          "Pipeline seharusnya belum mengeksekusi apa pun sebelum diiterasi")

        list(pipeline)  # konsumsi penuh
        self.assertTrue(execution_flag["touched"])

    def test_chain_output_matches_expected_count(self):
        chain = StreamChain(sample_source())
        chain.add_stage(DataCleanser(drop_invalid=False).process)
        chain.add_stage(Enricher().process)
        results = list(chain.run())
        self.assertEqual(len(results), 5)
        for row in results:
            self.assertIn("_processed_at", row)
            self.assertIn("_row_seq", row)


if __name__ == "__main__":
    unittest.main()
