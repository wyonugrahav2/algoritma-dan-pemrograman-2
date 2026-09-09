"""
test_adapter_conversions.py
Uji validitas transformasi struktur data oleh Adapter Pattern:
array terurut -> BST, dan list -> hash index.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pipeline.context import PipelineContext
from src.adapters.array_to_tree import ArrayToTreeAdapter, inorder
from src.adapters.list_to_hash import ListToHashAdapter


def test_array_to_tree_preserves_order():
    sorted_arr = [1, 2, 3, 4, 5, 6, 7]
    context = PipelineContext(payload=sorted_arr)
    new_context, message = ArrayToTreeAdapter().run(context)

    root = new_context.payload
    assert inorder(root) == sorted_arr
    assert "BST" in message


def test_array_to_tree_empty():
    context = PipelineContext(payload=[])
    new_context, _ = ArrayToTreeAdapter().run(context)
    assert new_context.payload is None


def test_list_to_hash_indexes_all_positions():
    data = ["a", "b", "a", "c", "b", "a"]
    context = PipelineContext(payload=data)
    new_context, message = ListToHashAdapter().run(context)

    index = new_context.payload
    assert index["a"] == [0, 2, 5]
    assert index["b"] == [1, 4]
    assert index["c"] == [3]
    assert "3 key unik" in message


if __name__ == "__main__":
    test_array_to_tree_preserves_order()
    test_array_to_tree_empty()
    test_list_to_hash_indexes_all_positions()
    print("Semua test_adapter_conversions.py PASSED")
