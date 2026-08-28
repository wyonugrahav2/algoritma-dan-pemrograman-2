"""
tree_traversal.py (recursive)
--------------------------------
Implementasi murni berbasis rekursi untuk traversal pohon biner
(pre-order, in-order, post-order).

Kompleksitas:
    Time  : O(N)
    Space : O(H) — H adalah tinggi pohon (call stack)
"""

from typing import Optional, List


class TreeNode:
    """Node pohon biner sederhana."""

    def __init__(self, value, left: Optional["TreeNode"] = None,
                 right: Optional["TreeNode"] = None):
        self.value = value
        self.left = left
        self.right = right


def preorder_recursive(root: Optional[TreeNode]) -> List:
    """Traversal pre-order (root -> left -> right) secara rekursif."""
    if root is None:
        return []
    return [root.value] + preorder_recursive(root.left) + preorder_recursive(root.right)


def inorder_recursive(root: Optional[TreeNode]) -> List:
    """Traversal in-order (left -> root -> right) secara rekursif."""
    if root is None:
        return []
    return inorder_recursive(root.left) + [root.value] + inorder_recursive(root.right)


def postorder_recursive(root: Optional[TreeNode]) -> List:
    """Traversal post-order (left -> right -> root) secara rekursif."""
    if root is None:
        return []
    return postorder_recursive(root.left) + postorder_recursive(root.right) + [root.value]


def build_balanced_tree(depth: int, counter_start: int = 1) -> Optional[TreeNode]:
    """
    Membangun pohon biner seimbang (balanced) dengan kedalaman tertentu.
    Digunakan untuk keperluan benchmarking traversal.

    Args:
        depth: kedalaman pohon yang diinginkan.
        counter_start: nilai awal untuk value node (increment per node).

    Returns:
        Root TreeNode dari pohon yang dibangun, atau None jika depth <= 0.
    """
    counter = [counter_start]

    def _build(d: int) -> Optional[TreeNode]:
        if d <= 0:
            return None
        node = TreeNode(counter[0])
        counter[0] += 1
        node.left = _build(d - 1)
        node.right = _build(d - 1)
        return node

    return _build(depth)
