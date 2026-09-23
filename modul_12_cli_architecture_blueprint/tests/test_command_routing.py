"""
test_command_routing.py
Pengujian unit untuk memverifikasi bahwa CommandRouter meneruskan
eksekusi ke handler yang sesuai, dan menolak perintah yang tidak dikenal.
"""

import unittest

from src.cli.parser import parse_args
from src.cli.router import CommandRouter, CommandNotFoundError
from src.core.context import AppContext


class TestCommandRouting(unittest.TestCase):
    def setUp(self):
        self.router = CommandRouter(context=AppContext())

    def test_dispatch_config_list_succeeds(self):
        parsed = parse_args(["config", "list"])
        exit_code = self.router.dispatch(parsed)
        self.assertEqual(exit_code, 0)

    def test_dispatch_search_succeeds(self):
        parsed = parse_args(["search", "sort", "--format", "json"])
        exit_code = self.router.dispatch(parsed)
        self.assertEqual(exit_code, 0)

    def test_dispatch_unknown_command_raises(self):
        parsed = parse_args([])
        parsed.name = "does-not-exist"
        with self.assertRaises(CommandNotFoundError):
            self.router.dispatch(parsed)

    def test_dispatch_process_missing_file_returns_error_code(self):
        parsed = parse_args(["process", "/no/such/file.txt", "--dry-run"])
        exit_code = self.router.dispatch(parsed)
        self.assertEqual(exit_code, 1)


if __name__ == "__main__":
    unittest.main()
