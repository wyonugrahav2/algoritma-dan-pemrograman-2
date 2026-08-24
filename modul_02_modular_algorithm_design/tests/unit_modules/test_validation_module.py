"""
Pengujian unit terisolasi untuk ValidationModule, memakai
Mocking/Stubbing pada rule agar logika internal modul lain
(analytics, transformation) tidak ikut dijalankan.
"""

import unittest
from unittest.mock import MagicMock

from src.modules.validation.rules import (
    ValidationModule,
    rule_is_numeric,
    rule_not_empty,
    rule_positive,
)


class TestValidationModule(unittest.TestCase):
    def test_valid_data_passes_default_rules(self) -> None:
        module = ValidationModule()
        result = module.run({"data": "hello"})
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

    def test_empty_data_fails_not_empty_rule(self) -> None:
        module = ValidationModule()
        result = module.run({"data": ""})
        self.assertFalse(result["valid"])
        self.assertIn("Nilai tidak boleh kosong.", result["errors"])

    def test_custom_rules_are_used_when_provided(self) -> None:
        module = ValidationModule(rules=[rule_not_empty, rule_is_numeric, rule_positive])
        result = module.run({"data": -5})
        self.assertFalse(result["valid"])
        self.assertIn("Nilai harus lebih besar dari nol.", result["errors"])

    def test_stubbed_rule_is_called_exactly_once(self) -> None:
        stub_rule = MagicMock(return_value=(True, ""))
        module = ValidationModule(rules=[stub_rule])

        module.run({"data": 123})

        stub_rule.assert_called_once_with(123)

    def test_cleanup_clears_rules(self) -> None:
        module = ValidationModule()
        module.run({"data": "x"})
        self.assertEqual(module.rules, [])


if __name__ == "__main__":
    unittest.main()
