"""
test_interactive_prompts.py
Menguji kelancaran interaksi dialog prompt (confirm & select_option)
dengan mensimulasikan input pengguna lewat monkeypatch pada builtins.input.
"""

import unittest
from unittest.mock import patch

from src.components.prompts import confirm, select_option


class TestInteractivePrompts(unittest.TestCase):
    @patch("builtins.input", return_value="y")
    def test_confirm_yes(self, _mock_input):
        self.assertTrue(confirm("Lanjutkan?"))

    @patch("builtins.input", return_value="")
    def test_confirm_default_false(self, _mock_input):
        self.assertFalse(confirm("Lanjutkan?", default=False))

    @patch("builtins.input", return_value="")
    def test_confirm_default_true(self, _mock_input):
        self.assertTrue(confirm("Lanjutkan?", default=True))

    @patch("builtins.input", side_effect=["99", "2"])
    def test_select_option_retries_on_invalid_input(self, _mock_input):
        result = select_option("Pilih algoritma:", ["bubble_sort", "quick_sort"])
        self.assertEqual(result, "quick_sort")

    def test_select_option_empty_list_returns_none(self):
        self.assertIsNone(select_option("Pilih:", []))


if __name__ == "__main__":
    unittest.main()
