"""
test_search_correctness.py
Memastikan semua algoritma menemukan nilai target dengan benar pada
dataset terurut standar.
"""

import pytest

from src.algorithms.linear_search import linear_search
from src.algorithms.binary_search import binary_search
from src.algorithms.interpolation_search import interpolation_search
from src.algorithms.exponential_search import exponential_search
from src.algorithms.hash_search import hash_search


SORTED_DATA = [2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78, 89, 91, 99, 105]


@pytest.mark.parametrize(
    "search_fn",
    [linear_search, binary_search, interpolation_search, exponential_search, hash_search],
)
@pytest.mark.parametrize("target,expected_index", [
    (2, 0),
    (56, 8),
    (105, 14),
    (91, 12),
])
def test_algorithm_finds_correct_index(search_fn, target, expected_index):
    result = search_fn(SORTED_DATA, target)
    assert result.found is True
    assert result.index == expected_index
    assert result.comparisons > 0


@pytest.mark.parametrize(
    "search_fn",
    [linear_search, binary_search, interpolation_search, exponential_search, hash_search],
)
def test_algorithm_reports_not_found_for_missing_value(search_fn):
    result = search_fn(SORTED_DATA, 999)
    assert result.found is False
    assert result.index == -1


def test_linear_search_works_on_unsorted_data():
    unsorted = [42, 7, 19, 3, 88, 56]
    result = linear_search(unsorted, 19)
    assert result.found is True
    assert result.index == 2


def test_binary_search_trace_has_expected_step_count():
    result = binary_search(SORTED_DATA, 105)
    assert len(result.trace) == result.comparisons
    assert result.algorithm == "binary"
