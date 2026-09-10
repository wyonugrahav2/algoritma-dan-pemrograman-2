"""Menampilkan pesan kesalahan yang rapi dan mudah dipahami pengguna."""
from __future__ import annotations

from config.error_codes import ERROR_MESSAGES
from src.exceptions.base_exceptions import AppException


def present_error(exc: BaseException) -> str:
    """Mengubah sebuah exception menjadi pesan yang ramah pengguna."""
    if isinstance(exc, AppException):
        friendly = ERROR_MESSAGES.get(exc.error_code, exc.message)
        lines = [
            "=" * 50,
            f"  Terjadi Kesalahan [{exc.error_code}]",
            "=" * 50,
            f"  {friendly}",
        ]
        if exc.message and exc.message != friendly:
            lines.append(f"  Detail: {exc.message}")
        lines.append("=" * 50)
        return "\n".join(lines)

    return (
        "=" * 50
        + "\n  Terjadi Kesalahan Tak Terduga\n"
        + "=" * 50
        + f"\n  {exc}\n"
        + "=" * 50
    )
