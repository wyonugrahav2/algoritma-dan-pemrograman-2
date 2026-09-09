"""
bar_chart_renderer.py
-----------------------
Merender animasi grafik batang ASCII (menggunakan karakter blok seperti
'█') secara live di terminal CLI, untuk memvisualisasikan pergerakan
elemen array saat proses pengurutan berlangsung.
"""

import os
import sys
import time

from config.settings import MAX_BAR_WIDTH, ANIMATION_DELAY_SECONDS

BAR_CHAR = "█"
HIGHLIGHT_CHAR = "▓"


def _clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def render_frame(array: list[int], highlight: tuple[int, ...] = ()) -> str:
    """Membentuk satu frame teks bar chart dari sebuah array."""
    if not array:
        return "(array kosong)"

    max_val = max(array)
    lines = []
    for idx, val in enumerate(array):
        bar_len = max(1, int((val / max_val) * MAX_BAR_WIDTH)) if max_val > 0 else 1
        char = HIGHLIGHT_CHAR if idx in highlight else BAR_CHAR
        lines.append(f"{val:>4} | {char * bar_len}")
    return "\n".join(lines)


def play_animation(snapshot, delay: float = ANIMATION_DELAY_SECONDS, clear: bool = True) -> None:
    """
    Memutar seluruh frame yang tercatat di dalam objek StateSnapshot secara
    berurutan, memberi efek animasi di terminal.
    """
    if len(snapshot) == 0:
        print("Tidak ada frame untuk dianimasikan (snapshot kosong).")
        return

    for frame, highlight in zip(snapshot.frames, snapshot.highlighted_indices):
        if clear:
            _clear_screen()
        print(render_frame(frame, highlight))
        sys.stdout.flush()
        time.sleep(delay)
