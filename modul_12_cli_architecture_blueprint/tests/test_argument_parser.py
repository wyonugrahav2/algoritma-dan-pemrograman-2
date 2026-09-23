"""
test_argument_parser.py
Pengujian unit untuk memverifikasi keakuratan ekstraksi argumen terminal.
"""

import unittest

from src.cli.parser import parse_args


class TestArgumentParser(unittest.TestCase):
    def test_search_command_basic(self):
        parsed = parse_args(["search", "binary"])
        self.assertEqual(parsed.name, "search")
        self.assertEqual(parsed.args["query"], "binary")
        self.assertEqual(parsed.args["format"], "table")
        self.assertEqual(parsed.args["limit"], 20)

    def test_search_command_with_flags(self):
        parsed = parse_args(["search", "sort", "--format", "json", "--limit", "5"])
        self.assertEqual(parsed.args["format"], "json")
        self.assertEqual(parsed.args["limit"], 5)

    def test_process_command_dry_run(self):
        parsed = parse_args(["process", "input.txt", "--dry-run"])
        self.assertEqual(parsed.name, "process")
        self.assertEqual(parsed.args["input"], "input.txt")
        self.assertTrue(parsed.args["dry_run"])

    def test_config_get(self):
        parsed = parse_args(["config", "get", "theme"])
        self.assertEqual(parsed.name, "config")
        self.assertEqual(parsed.args["config_action"], "get")
        self.assertEqual(parsed.args["key"], "theme")

    def test_global_flags(self):
        parsed = parse_args(["--verbose", "--theme", "mono", "search", "x"])
        self.assertTrue(parsed.verbose)
        self.assertEqual(parsed.theme, "mono")

    def test_no_command_returns_none_name(self):
        parsed = parse_args([])
        self.assertIsNone(parsed.name)


if __name__ == "__main__":
    unittest.main()
