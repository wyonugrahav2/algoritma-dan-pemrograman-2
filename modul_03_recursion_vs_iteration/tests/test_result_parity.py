"""
test_result_parity.py
------------------------
Memverifikasi bahwa masukan N yang sama menghasilkan luaran bernilai
persis sama pada kedua pendekatan (rekursif vs iteratif).
"""

import pytest

from src.algorithms.recursive.fibonacci import fibonacci_recursive
from src.algorithms.iterative.fibonacci import fibonacci_recursive as fibonacci_iterative
from src.algorithms.recursive.tree_traversal import (
    TreeNode,
    build_balanced_tree,
    preorder_recursive,
    inorder_recursive,
    postorder_recursive,
)
from src.algorithms.iterative.tree_traversal import (
    preorder_recursive as preorder_iterative,
    inorder_recursive as inorder_iterative,
    postorder_recursive as postorder_iterative,
)


@pytest.mark.parametrize("n", [0, 1, 2, 3, 5, 8, 10, 15, 20])
def test_fibonacci_parity(n):
    assert fibonacci_recursive(n) == fibonacci_iterative(n)


@pytest.mark.parametrize("depth", [1, 2, 3, 4, 5])
def test_tree_traversal_parity(depth):
    root = build_balanced_tree(depth)

    assert preorder_recursive(root) == preorder_iterative(root)
    assert inorder_recursive(root) == inorder_iterative(root)
    assert postorder_recursive(root) == postorder_iterative(root)


def test_empty_tree_parity():
    root = None
    assert preorder_recursive(root) == preorder_iterative(root) == []
    assert inorder_recursive(root) == inorder_iterative(root) == []
    assert postorder_recursive(root) == postorder_iterative(root) == []
