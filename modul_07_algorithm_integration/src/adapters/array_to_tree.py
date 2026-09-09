"""
array_to_tree.py
Adapter Pattern: mentransformasi luaran dari satu algoritma (array terurut,
hasil dari sorter_component) menjadi struktur data yang dibutuhkan oleh
algoritma berikutnya, dalam hal ini Binary Search Tree (BST) seimbang.
"""

from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class TreeNode:
    value: Any
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def _build_balanced_bst(sorted_arr: List[Any]) -> Optional[TreeNode]:
    if not sorted_arr:
        return None
    mid = len(sorted_arr) // 2
    node = TreeNode(value=sorted_arr[mid])
    node.left = _build_balanced_bst(sorted_arr[:mid])
    node.right = _build_balanced_bst(sorted_arr[mid + 1:])
    return node


def inorder(node: Optional[TreeNode], acc: Optional[List[Any]] = None) -> List[Any]:
    """Utilitas verifikasi: traversal in-order harus mengembalikan array terurut."""
    if acc is None:
        acc = []
    if node is None:
        return acc
    inorder(node.left, acc)
    acc.append(node.value)
    inorder(node.right, acc)
    return acc


class ArrayToTreeAdapter:
    """Stage adapter: array terurut -> pohon BST seimbang."""

    name = "array_to_tree_adapter"

    def run(self, context):
        sorted_arr = list(context.payload)
        root = _build_balanced_bst(sorted_arr)
        message = f"Array ({len(sorted_arr)} elemen) diubah menjadi BST seimbang."
        new_context = context.with_payload(root)
        return new_context, message


def array_to_tree_stage(context):
    return ArrayToTreeAdapter().run(context)
