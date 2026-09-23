"""
search_cmd.py
Implementasi handler untuk subcommand 'search'.
Contoh sederhana: mencari kata kunci di dalam data dummy in-memory,
lalu menampilkan hasilnya lewat komponen tabel.
"""

from typing import Any, Dict

from src.commands.base_command import BaseCommand
from src.components.tables import render_table
from src.components.spinners import run_with_spinner

# Data contoh -- pada implementasi nyata ini akan datang dari
# controller.py / lapisan bisnis, bukan hardcoded di command.
_SAMPLE_DATA = [
    {"id": 1, "name": "binary_search.py", "category": "algorithm"},
    {"id": 2, "name": "quick_sort.py", "category": "algorithm"},
    {"id": 3, "name": "hash_table.py", "category": "data-structure"},
    {"id": 4, "name": "linked_list.py", "category": "data-structure"},
]


class SearchCommand(BaseCommand):
    help_text = "Mencari data berdasarkan kata kunci. Contoh: search <query> [--format table|json] [--limit N]"

    def execute(self, args: Dict[str, Any]) -> None:
        query = args.get("query", "")
        fmt = args.get("format", "table")
        limit = args.get("limit", 20)

        results = run_with_spinner(
            "Mencari data...",
            lambda: self._search(query, limit),
        )

        if fmt == "json":
            import json
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            render_table(
                headers=["id", "name", "category"],
                rows=[[r["id"], r["name"], r["category"]] for r in results],
                theme=self.context.theme,
            )

    def _search(self, query: str, limit: int):
        matches = [row for row in _SAMPLE_DATA if query.lower() in row["name"].lower()]
        return matches[:limit]
