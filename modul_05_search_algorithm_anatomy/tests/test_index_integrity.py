"""
test_index_integrity.py
Menguji integritas struktur Hash Index dan Inverted Index yang
dibangun oleh src/indexer/index_builder.py.
"""

from src.indexer.index_builder import (
    build_hash_index,
    build_inverted_index,
    validate_index_integrity,
)


def test_hash_index_maps_values_to_correct_positions():
    data = [10, 20, 30, 40, 50]
    hash_index = build_hash_index(data)

    assert hash_index.get(30) == [2]
    assert hash_index.get(999) == []
    assert hash_index.contains(10) is True
    assert hash_index.contains(999) is False


def test_hash_index_handles_duplicate_values():
    data = [5, 10, 5, 15, 5]
    hash_index = build_hash_index(data)

    assert hash_index.get(5) == [0, 2, 4]
    assert hash_index.total_keys_inserted == 5


def test_hash_index_integrity_validation_passes_for_correct_index():
    data = [3, 1, 4, 1, 5, 9, 2, 6]
    hash_index = build_hash_index(data)

    assert validate_index_integrity(hash_index, data) is True


def test_hash_index_integrity_validation_fails_for_corrupted_index():
    data = [3, 1, 4, 1, 5, 9, 2, 6]
    hash_index = build_hash_index(data)

    # Merusak indeks secara sengaja untuk memastikan validator peka.
    hash_index.table[3].append(999)  # posisi di luar rentang data

    assert validate_index_integrity(hash_index, data) is False


def test_hash_index_load_factor_within_expected_range():
    data = list(range(100))
    hash_index = build_hash_index(data, initial_buckets=16)

    load_factor = hash_index.load_factor()
    assert load_factor > 0


def test_inverted_index_groups_records_by_field_value():
    records = [
        {"id": 1, "category": "fruit", "value": "apple"},
        {"id": 2, "category": "fruit", "value": "banana"},
        {"id": 3, "category": "vegetable", "value": "carrot"},
    ]
    inverted = build_inverted_index(records, fields=["category", "value"])

    assert inverted.index["category"]["fruit"] == [0, 1]
    assert inverted.index["category"]["vegetable"] == [2]
    assert inverted.index["value"]["carrot"] == [2]


def test_inverted_index_handles_missing_field_gracefully():
    records = [{"id": 1, "category": "fruit"}, {"id": 2}]
    inverted = build_inverted_index(records, fields=["category"])

    assert inverted.index["category"]["fruit"] == [0]
    assert 1 not in inverted.index["category"].get("fruit", [])
