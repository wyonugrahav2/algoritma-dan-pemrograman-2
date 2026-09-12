"""
settings.py
Konfigurasi ambang batas faktor beban (Load Factor threshold), kapasitas awal
tabel hash, dan parameter umum lain yang dipakai lintas modul.
"""

import os

# --- Hash Table Configuration -------------------------------------------------
INITIAL_CAPACITY: int = int(os.getenv("HASH_INITIAL_CAPACITY", 8))
LOAD_FACTOR_THRESHOLD: float = float(os.getenv("HASH_LOAD_FACTOR_THRESHOLD", 0.7))
RESIZE_MULTIPLIER: int = int(os.getenv("HASH_RESIZE_MULTIPLIER", 2))

# --- Collision Strategy --------------------------------------------------------
# "chaining" atau "open_addressing"
COLLISION_STRATEGY: str = os.getenv("HASH_COLLISION_STRATEGY", "chaining")

# --- Bloom Filter Configuration -------------------------------------------------
BLOOM_DEFAULT_SIZE: int = int(os.getenv("BLOOM_DEFAULT_SIZE", 10_000))
BLOOM_DEFAULT_HASH_COUNT: int = int(os.getenv("BLOOM_DEFAULT_HASH_COUNT", 5))
BLOOM_FALSE_POSITIVE_RATE: float = float(os.getenv("BLOOM_FALSE_POSITIVE_RATE", 0.01))

# --- LRU Cache Configuration -----------------------------------------------------
LRU_DEFAULT_CAPACITY: int = int(os.getenv("LRU_DEFAULT_CAPACITY", 128))

# --- Benchmark Configuration ------------------------------------------------------
BENCHMARK_SAMPLE_SIZES = [10, 100, 1_000, 10_000, 100_000]
BENCHMARK_REPEAT: int = int(os.getenv("BENCHMARK_REPEAT", 3))
