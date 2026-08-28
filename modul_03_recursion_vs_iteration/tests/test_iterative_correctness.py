"""
test_iterative_correctness.py
--------------------------------
Memastikan hasil implementasi iteratif valid dan sesuai ekspektasi.
"""

import pytest

from src.algorithms.iterative.fibonacci import fibonacci_recursive as fibonacci_iterative
from src.algorithms.recursive.tree_traversal import TreeNode, build_balanced_tree
from src.algorithms.iterative.tree_traversal import (
    preorder_recursive as preorder_iterative,
    inorder_recursive as inorder_iterative,
    postorder_recursive as postorder_iterative,
)


@pytest.mark.parametrize("n, expected", [
    (0, 0), (1, 1), (2, 1), (3, 2), (5, 5), (10, 55),
])
def test_fibonacci_iterative(n, expected):
    assert fibonacci_iterative(n) == expected


def test_fibonacci_iterative_negative_raises():
    with pytest.raises(ValueError):
        fibonacci_iterative(-1)


def test_tree_traversal_iterative():
    #        1
    #       / \
    #      2   3
    root = TreeNode(1, TreeNode(2), TreeNode(3))

    assert preorder_iterative(root) == [1, 2, 3]
    assert inorder_iterative(root) == [2, 1, 3]
    assert postorder_iterative(root) == [2, 3, 1]


def test_build_balanced_tree_node_count_iterative():
    depth = 4
    root = build_balanced_tree(depth)
    nodes = preorder_iterative(root)
    expected_count = 2 ** depth - 1
    assert len(nodes) == expected_count
