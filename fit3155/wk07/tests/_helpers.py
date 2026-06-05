"""Shared helpers for the Fibonacci heap tests."""

from __future__ import annotations

from fit3155.wk07.src.FibonacciHeap import FibonacciHeap, Node


def _walk_ring(start: Node) -> list[Node]:
    """Return a ring's nodes, checking left/right pointers are inverses."""
    nodes: list[Node] = []
    node = start
    while True:
        assert node.right.left is node, "broken ring: right.left"
        assert node.left.right is node, "broken ring: left.right"
        nodes.append(node)
        node = node.right
        assert len(nodes) <= 100_000, "ring is not circular"
        if node is start:
            break
    return nodes


def _check_tree(node: Node) -> int:
    """Validate the subtree at node (heap order, degree); return its size."""
    size = 1
    if node.child is None:
        assert node.degree == 0, "no children but degree != 0"
        return size
    children = _walk_ring(node.child)
    assert len(children) == node.degree, "degree != child count"
    for c in children:
        assert c.parent is node, "child.parent wrong"
        assert c.key >= node.key, "heap order violated"
        size += _check_tree(c)
    return size


def assert_valid_heap(heap: FibonacciHeap) -> None:
    """Assert every structural invariant holds for the whole heap."""
    if heap.min is None:
        assert heap.n == 0, "empty heap must have n == 0"
        return

    assert heap.min.parent is None, "min must be a root"
    forest = _walk_ring(heap.min)

    size = 0
    smallest = heap.min.key
    for r in forest:
        assert r.parent is None, "root has a parent"
        smallest = min(smallest, r.key)
        size += _check_tree(r)

    assert heap.min.key == smallest, "min is not the smallest root"
    assert size == heap.n, "n != real node count"


def roots(heap: FibonacciHeap) -> list[Node]:
    """Return the heap's root nodes (empty list if the heap is empty)."""
    if heap.min is None:
        return []
    return _walk_ring(heap.min)


def heap_of(keys) -> FibonacciHeap:
    """Build a heap from an iterable of keys (no node handles returned)."""
    heap = FibonacciHeap()
    for key in keys:
        heap.insert(key)
    return heap


def drain(heap: FibonacciHeap) -> list[int]:
    """Extract every key in order, returning them as a list."""
    out: list[int] = []
    while heap.min is not None:
        out.append(heap.extract_min())
    return out
