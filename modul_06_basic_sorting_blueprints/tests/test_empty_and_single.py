"""
test_empty_and_single.py
---------------------------
Test edge case: array kosong atau cuma 1 elemen. Kasus batas ini sering
menjadi sumber bug (misal IndexError pada implementasi partition Quick Sort
atau off-by-one pada Insertion Sort).
"""

import pytest

from config.sort_strategies import SORT_STRATEGIES


@pytest.mark.parametrize("name,strategy", SORT_STRATEGIES.items())
def test_empty_array(name, strategy):
    assert strategy["function"]([]) == []


@pytest.mark.parametrize("name,strategy", SORT_STRATEGIES.items())
def test_single_element_array(name, strategy):
    assert strategy["function"]([42]) == [42]


@pytest.mark.parametrize("name,strategy", SORT_STRATEGIES.items())
def test_two_element_arrays(name, strategy):
    assert strategy["function"]([2, 1]) == [1, 2]
    assert strategy["function"]([1, 2]) == [1, 2]
    assert strategy["function"]([1, 1]) == [1, 1]


@pytest.mark.parametrize("name,strategy", SORT_STRATEGIES.items())
def test_all_elements_identical(name, strategy):
    data = [7, 7, 7, 7, 7]
    assert strategy["function"](data) == data


@pytest.mark.parametrize("name,strategy", SORT_STRATEGIES.items())
def test_already_sorted_array(name, strategy):
    data = list(range(20))
    assert strategy["function"](data) == data
