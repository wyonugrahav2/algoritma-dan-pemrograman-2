"""
ascii_plotter.py
Merender grafik garis (growth curve) tren pertumbuhan Big-O langsung
di terminal CLI menggunakan karakter ASCII, tanpa dependensi eksternal.
"""

from typing import List, Tuple

from config.settings import Settings


def plot_growth_curve(
    points: List[Tuple[int, float]],
    width: int = None,
    height: int = None,
    title: str = "Growth Curve",
    y_label: str = "waktu (s)",
) -> str:
    """
    Merender grafik garis ASCII dari daftar titik (n, value).
    Mengembalikan string multi-baris siap-print.
    """
    width = width or Settings.ASCII_PLOT_WIDTH
    height = height or Settings.ASCII_PLOT_HEIGHT

    if not points:
        return f"{title}\n(tidak ada data untuk diplot)"

    values = [v for _, v in points]
    min_val, max_val = min(values), max(values)
    val_range = max_val - min_val or 1.0

    grid = [[" " for _ in range(width)] for _ in range(height)]

    n_points = len(points)
    for idx, (_, value) in enumerate(points):
        col = int((idx / max(n_points - 1, 1)) * (width - 1))
        normalized = (value - min_val) / val_range
        row = height - 1 - int(normalized * (height - 1))
        row = max(0, min(height - 1, row))
        grid[row][col] = "*"

    lines = [f"{title}"]
    lines.append(f"{y_label} max: {max_val:.6f} | min: {min_val:.6f}")
    lines.append("+" + "-" * width + "+")
    for row in grid:
        lines.append("|" + "".join(row) + "|")
    lines.append("+" + "-" * width + "+")

    n_labels = " ".join(str(n) for n, _ in points)
    lines.append(f"N: {n_labels}")

    return "\n".join(lines)


def plot_bar_comparison(
    labels: List[str],
    values: List[float],
    width: int = None,
    unit: str = "s",
) -> str:
    """
    Merender grafik batang horizontal ASCII sederhana untuk
    membandingkan beberapa nilai (mis. waktu eksekusi tiap algoritma).
    """
    width = width or Settings.ASCII_PLOT_WIDTH
    if not values:
        return "(tidak ada data untuk diplot)"

    max_val = max(values) or 1.0
    max_label_len = max(len(label) for label in labels)

    lines = []
    for label, value in zip(labels, values):
        bar_len = int((value / max_val) * width) if max_val > 0 else 0
        bar = "#" * max(bar_len, 0)
        lines.append(f"{label.rjust(max_label_len)} | {bar} {value:.6f}{unit}")

    return "\n".join(lines)
