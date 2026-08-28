"""
tree_traversal.py (iterative)
--------------------------------
Implementasi murni berbasis perulangan (loop) untuk traversal pohon
biner (pre-order, in-order, post-order) menggunakan stack eksplisit.

Kompleksitas:
    Time  : O(N)
    Space : O(N) — menggunakan stack eksplisit di heap, bukan call stack
"""

from typing import Optional, List
from src.algorithms.recursive.tree_traversal import TreeNode


def preorder_recursive(root: Optional[TreeNode]) -> List:
    """
    Traversal pre-order (root -> left -> right) secara iteratif
    menggunakan stack eksplisit.
    (Nama fungsi disamakan dengan versi rekursif untuk isomorfisme
    signature terhadap runner.py)
    """
    if root is None:
        return []

    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.value)
        # Push kanan dulu agar kiri diproses lebih dulu (LIFO)
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)
    return result


def inorder_recursive(root: Optional[TreeNode]) -> List:
    """Traversal in-order (left -> root -> right) secara iteratif."""
    result = []
    stack = []
    current = root

    while current is not None or stack:
        while current is not None:
            stack.append(current)
            current = current.left
        current = stack.pop()
        result.append(current.value)
        current = current.right

    return result


def postorder_recursive(root: Optional[TreeNode]) -> List:
    """Traversal post-order (left -> right -> root) secara iteratif."""
    if root is None:
        return []

    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.value)
        if node.left is not None:
            stack.append(node.left)
        if node.right is not None:
            stack.append(node.right)

    return result[::-1]
