"""
main.py
Entry Point Utama Aplikasi CLI Architecture Blueprint.

Alur eksekusi:
1. parser.py mengekstrak argumen dari sys.argv -> ParsedCommand
2. router.py meneruskan ParsedCommand ke handler command yang sesuai
3. Handler (mewarisi BaseCommand) mengeksekusi logika dan memakai
   komponen UI (tables/prompts/spinners) untuk menampilkan hasil
"""

import sys

from src.cli.parser import parse_args
from src.cli.router import CommandRouter, CommandNotFoundError
from src.core.context import AppContext


def main() -> int:
    context = AppContext()
    parsed_command = parse_args()

    router = CommandRouter(context=context)
    try:
        return router.dispatch(parsed_command)
    except CommandNotFoundError as exc:
        context.presenter_error(str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
