"""
Pengujian unit terisolasi untuk AnalyticsModule.

Modul ini diuji sendiri tanpa menjalankan transformation atau
validation, sesuai prinsip isolasi pengujian.
"""

import unittest

from src.modules.analytics.analyzer import AnalyticsModule


class TestAnalyticsModule(unittest.TestCase):
    def setUp(self) -> None:
        self.module = AnalyticsModule()

    def test_summary_basic_values(self) -> None:
        result = self.module.run({"values": [1, 2, 3, 4, 5]})

        self.assertEqual(result["count"], 5)
        self.assertEqual(result["mean"], 3)
        self.assertEqual(result["median"], 3)
        self.assertEqual(result["min"], 1)
        self.assertEqual(result["max"], 5)

    def test_summary_empty_values(self) -> None:
        result = self.module.run({"values": []})

        self.assertEqual(result["count"], 0)
        self.assertEqual(result["mean"], 0.0)
        self.assertEqual(result["min"], 0.0)
        self.assertEqual(result["max"], 0.0)

    def test_module_name_is_analytics(self) -> None:
        self.assertEqual(self.module.name, "analytics")

    def test_cleanup_resets_ready_flag(self) -> None:
        self.module.run({"values": [1, 2, 3]})
        self.assertFalse(self.module._ready)


if __name__ == "__main__":
    unittest.main()
