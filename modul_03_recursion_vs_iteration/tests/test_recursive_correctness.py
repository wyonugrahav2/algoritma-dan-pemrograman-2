"""
test_recursive_correctness.py
--------------------------------
Memastikan hasil implementasi rekursif valid dan sesuai ekspektasi.
"""

import pytest

from src.algorithms.recursive.fibonacci import fibonacci_recursive
from src.algorithms.recursive.tail_recursion import (
    fibonacci_tail_recursive,
    factorial_tail_recursive,
)
from src.algorithms.recursive.tree_traversal import (
    TreeNode,
    preorder_recursive,
    inorder_recursive,
    postorder_recursive,
    build_balanced_tree,
)


@pytest.mark.parametrize("n, expected", [
    (0, 0), (1, 1), (2, 1), (3, 2), (5, 5), (10, 55),
])
def test_fibonacci_recursive(n, expected):
    assert fibonacci_recursive(n) == expected


def test_fibonacci_recursive_negative_raises():
    with pytest.raises(ValueError):
        fibonacci_recursive(-1)


@pytest.mark.parametrize("n, expected", [
    (0, 0), (1, 1), (2, 1), (3, 2), (5, 5), (10, 55),
])
def test_fibonacci_tail_recursive(n, expected):
    assert fibonacci_tail_recursive(n) == expected


def test_factorial_tail_recursive():
    assert factorial_tail_recursive(0) == 1
    assert factorial_tail_recursive(5) == 120


def test_tree_traversal_recursive():
    #        1
    #       / \
    #      2   3
    root = TreeNode(1, TreeNode(2), TreeNode(3))

    assert preorder_recursive(root) == [1, 2, 3]
    assert inorder_recursive(root) == [2, 1, 3]
    assert postorder_recursive(root) == [2, 3, 1]


def test_build_balanced_tree_node_count():
    depth = 4
    root = build_balanced_tree(depth)
    nodes = preorder_recursive(root)
    expected_count = 2 ** depth - 1
    assert len(nodes) == expected_count
