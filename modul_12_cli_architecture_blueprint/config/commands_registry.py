"""
commands_registry.py
Mendaftarkan seluruh subcommand yang aktif dalam sistem CLI.
Router (src/cli/router.py) membaca registry ini untuk memetakan
nama perintah -> handler class, tanpa perlu hardcode di parser.
"""

from src.commands.search_cmd import SearchCommand
from src.commands.process_cmd import ProcessCommand
from src.commands.config_cmd import ConfigCommand

# Mapping: nama_perintah -> (handler_class, deskripsi singkat untuk --help)
COMMAND_REGISTRY = {
    "search": (SearchCommand, "Mencari data berdasarkan kata kunci"),
    "process": (ProcessCommand, "Memproses/mentransformasi data masukan"),
    "config": (ConfigCommand, "Mengelola konfigurasi aplikasi"),
}


def get_registered_commands():
    """Mengembalikan salinan dictionary registry perintah aktif."""
    return dict(COMMAND_REGISTRY)


def is_command_registered(name: str) -> bool:
    return name in COMMAND_REGISTRY
