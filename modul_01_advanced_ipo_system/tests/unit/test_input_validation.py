"""
test_input_validation.py
Unit test untuk fungsi-fungsi validasi dan parsing pada input_layer.
"""

import unittest

from src.domain.exceptions import (
    EmptyInputError,
    ParsingError,
    ValueOutOfRangeError,
)
from src.domain.models import RawInput
from src.input_layer.parsers import parse_to_float, parse_to_int, parse_to_list
from src.input_layer.validators import (
    sanitize_raw_string,
    validate_max_length,
    validate_numeric_range,
)


class TestValidators(unittest.TestCase):
    def test_sanitize_raw_string_strips_whitespace(self):
        self.assertEqual(sanitize_raw_string("  hello  "), "hello")

    def test_sanitize_raw_string_raises_on_empty(self):
        with self.assertRaises(EmptyInputError):
            sanitize_raw_string("   ")

    def test_validate_numeric_range_within_bounds(self):
        self.assertEqual(validate_numeric_range(50, 0, 100), 50)

    def test_validate_numeric_range_out_of_bounds_raises(self):
        with self.assertRaises(ValueOutOfRangeError):
            validate_numeric_range(150, 0, 100)

    def test_validate_max_length_raises_when_exceeded(self):
        with self.assertRaises(Exception):
            validate_max_length("a" * 10, 5)


class TestParsers(unittest.TestCase):
    def test_parse_to_int_success(self):
        result = parse_to_int(RawInput(raw_value="42"))
        self.assertEqual(result.value, 42)

    def test_parse_to_int_invalid_raises_parsing_error(self):
        with self.assertRaises(ParsingError):
            parse_to_int(RawInput(raw_value="abc"))

    def test_parse_to_float_success(self):
        result = parse_to_float(RawInput(raw_value="3.14"))
        self.assertAlmostEqual(result.value, 3.14)

    def test_parse_to_list_success(self):
        result = parse_to_list(RawInput(raw_value="1, 2, 3.5"))
        self.assertEqual(result.value, [1.0, 2.0, 3.5])

    def test_parse_to_list_invalid_element_raises(self):
        with self.assertRaises(ParsingError):
            parse_to_list(RawInput(raw_value="1, abc, 3"))


if __name__ == "__main__":
    unittest.main()
