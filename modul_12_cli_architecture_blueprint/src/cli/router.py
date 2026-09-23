"""
router.py
Pengarah perintah (Command Router). Menerima ParsedCommand dari parser
dan meneruskan eksekusi ke handler command yang sesuai, secara dinamis,
berdasarkan config/commands_registry.py.

Router tidak tahu-menahu detail implementasi tiap command -- ia hanya
tahu bahwa setiap handler terdaftar mengimplementasikan kontrak
BaseCommand.run(args, context).
"""

from typing import Optional

from config.commands_registry import get_registered_commands
from src.core.context import AppContext
from src.cli.theme import get_theme


class CommandNotFoundError(Exception):
    """Dilempar ketika nama command tidak ditemukan di registry."""


class CommandRouter:
    def __init__(self, context: Optional[AppContext] = None):
        self.registry = get_registered_commands()
        self.context = context or AppContext()

    def dispatch(self, parsed_command) -> int:
        """
        Mengeksekusi command sesuai hasil parsing.
        Mengembalikan exit code (0 = sukses, non-zero = gagal).
        """
        name = parsed_command.name

        if name is None:
            self._print_available_commands()
            return 1

        if name not in self.registry:
            raise CommandNotFoundError(f"Perintah '{name}' tidak dikenali.")

        self.context.theme = get_theme(parsed_command.theme)
        self.context.verbose = parsed_command.verbose

        handler_class, _description = self.registry[name]
        handler = handler_class(context=self.context)
        return handler.run(parsed_command.args)

    def _print_available_commands(self) -> None:
        theme = get_theme("default")
        print(f"{theme['primary']}Perintah yang tersedia:{theme['reset']}")
        for name, (_cls, desc) in self.registry.items():
            print(f"  {theme['primary']}{name:<10}{theme['reset']} {desc}")
