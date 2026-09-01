"""
test_edge_cases.py
Menguji kasus batas: data kosong, elemen di ujung array, dan data
yang sama sekali tidak mengandung target.
"""

import pytest

from src.algorithms.linear_search import linear_search
from src.algorithms.binary_search import binary_search
from src.algorithms.interpolation_search import interpolation_search
from src.algorithms.exponential_search import exponential_search
from src.algorithms.hash_search import hash_search
from src.indexer.sorter import is_sorted, sort_data, uniformity_score, ensure_sorted


ALL_ALGORITHMS = [linear_search, binary_search, interpolation_search, exponential_search, hash_search]


@pytest.mark.parametrize("search_fn", ALL_ALGORITHMS)
def test_empty_data_returns_not_found(search_fn):
    result = search_fn([], 10)
    assert result.found is False
    assert result.index == -1


@pytest.mark.parametrize("search_fn", ALL_ALGORITHMS)
def test_single_element_found(search_fn):
    result = search_fn([42], 42)
    assert result.found is True
    assert result.index == 0


@pytest.mark.parametrize("search_fn", ALL_ALGORITHMS)
def test_single_element_not_found(search_fn):
    result = search_fn([42], 7)
    assert result.found is False


@pytest.mark.parametrize(
    "search_fn", [linear_search, binary_search, interpolation_search, exponential_search, hash_search]
)
def test_target_at_last_position(search_fn):
    data = [1, 3, 5, 7, 9, 11, 13]
    result = search_fn(data, 13)
    assert result.found is True
    assert result.index == len(data) - 1


@pytest.mark.parametrize(
    "search_fn", [binary_search, interpolation_search, exponential_search]
)
def test_target_at_first_position(search_fn):
    data = [1, 3, 5, 7, 9, 11, 13]
    result = search_fn(data, 1)
    assert result.found is True
    assert result.index == 0


def test_is_sorted_detects_unsorted_data():
    assert is_sorted([1, 2, 3]) is True
    assert is_sorted([3, 1, 2]) is False


def test_ensure_sorted_sorts_when_needed():
    result = ensure_sorted([5, 1, 4, 2, 3])
    assert result == [1, 2, 3, 4, 5]


def test_uniformity_score_high_for_uniform_data():
    uniform_data = list(range(0, 100, 5))
    score = uniformity_score(uniform_data)
    assert score > 0.8


def test_uniformity_score_low_for_skewed_data():
    skewed_data = [1, 2, 3, 4, 5, 1_000_000]
    score = uniformity_score(skewed_data)
    assert score < 0.5


def test_duplicate_values_are_handled():
    data = [1, 2, 2, 2, 3, 4]
    result = binary_search(data, 2)
    assert result.found is True
    assert data[result.index] == 2
