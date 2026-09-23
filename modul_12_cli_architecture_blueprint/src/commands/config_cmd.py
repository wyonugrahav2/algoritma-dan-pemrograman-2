"""
config_cmd.py
Implementasi handler untuk subcommand 'config'.
Mengelola konfigurasi aplikasi yang disimpan di AppContext (in-memory
untuk contoh ini; pada implementasi nyata bisa dipersiskan ke berkas).
"""

from typing import Any, Dict

from src.commands.base_command import BaseCommand, CommandError


class ConfigCommand(BaseCommand):
    help_text = "Mengelola konfigurasi. Contoh: config get <key> | config set <key> <value> | config list"

    def execute(self, args: Dict[str, Any]) -> None:
        action = args.get("config_action")

        if action == "get":
            key = args["key"]
            value = self.context.config.get(key)
            if value is None:
                raise CommandError(f"Kunci konfigurasi '{key}' tidak ditemukan.")
            print(value)

        elif action == "set":
            key, value = args["key"], args["value"]
            self.context.config[key] = value
            self.context.presenter_success(f"'{key}' diset menjadi '{value}'")

        elif action == "list":
            if not self.context.config:
                print("(belum ada konfigurasi)")
            for k, v in self.context.config.items():
                print(f"{k} = {v}")

        else:
            raise CommandError("Aksi config tidak dikenali. Gunakan get/set/list.")
