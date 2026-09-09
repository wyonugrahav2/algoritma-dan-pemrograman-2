"""
settings.py
-----------
Threshold ukuran data & batasan visualisasi untuk Modul 06 - Basic Sorting Blueprints.
Semua nilai konfigurasi disentralisasi di sini agar tidak ada "magic number"
yang tersembunyi di dalam logika bisnis.
"""

import os

# --- Batas Ukuran Data ---
MAX_VISUAL_ARRAY_SIZE = int(os.getenv("MAX_VISUAL_ARRAY_SIZE", 60))
DEFAULT_ARRAY_SIZE = int(os.getenv("DEFAULT_ARRAY_SIZE", 15))

# --- Batasan Animasi ---
ANIMATION_DELAY_SECONDS = float(os.getenv("ANIMATION_DELAY_SECONDS", 0.05))
MAX_BAR_WIDTH = int(os.getenv("MAX_BAR_WIDTH", 40))

# --- Batas Nilai Elemen Array ---
RANDOM_VALUE_MIN = 1
RANDOM_VALUE_MAX = 999

# --- Mode Verbose ---
VERBOSE_MODE = os.getenv("VERBOSE_MODE", "false").lower() == "true"
