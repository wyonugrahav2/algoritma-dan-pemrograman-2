"""
tables.py
Custom table renderer -- mencetak data tabular ke terminal tanpa
dependensi eksternal, dengan lebar kolom otomatis dan pewarnaan header
sesuai tema aktif.
"""

from typing import List, Sequence


def render_table(headers: Sequence[str], rows: List[Sequence], theme: dict = None) -> None:
    """Mencetak tabel rapi ke stdout berdasarkan headers dan rows."""
    theme = theme or {"primary": "", "reset": "", "muted": ""}

    if not rows:
        print(f"{theme.get('muted', '')}(tidak ada data){theme.get('reset', '')}")
        return

    str_rows = [[str(cell) for cell in row] for row in rows]
    col_widths = [
        max(len(str(headers[i])), *(len(row[i]) for row in str_rows))
        for i in range(len(headers))
    ]

    header_line = " | ".join(
        str(headers[i]).ljust(col_widths[i]) for i in range(len(headers))
    )
    separator = "-+-".join("-" * w for w in col_widths)

    print(f"{theme.get('primary', '')}{header_line}{theme.get('reset', '')}")
    print(separator)
    for row in str_rows:
        print(" | ".join(row[i].ljust(col_widths[i]) for i in range(len(headers))))
