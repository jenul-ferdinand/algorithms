import pytest

from fit3155.wk07.src.FibonacciHeap import FibonacciHeap
from fit3155.wk07.tests._helpers import assert_valid_heap, heap_of, roots


def test_decrease_key_raises_on_increase():
    h = FibonacciHeap()
    node = h.insert(5)
    with pytest.raises(ValueError):
        h.decrease_key(node, 9)


def test_decrease_key_without_violation_does_not_cut():
    # Notes case 1: the new key still respects the parent, so nothing moves.
    h = heap_of(range(8))
    h.extract_min()  # consolidate so some root gains children
    assert_valid_heap(h)
    parent = next(r for r in roots(h) if r.child is not None)
    child = parent.child
    h.decrease_key(child, parent.key)  # equal key keeps heap order
    assert child.parent is parent, "node was cut despite no violation"
    assert_valid_heap(h)


def test_decrease_key_to_new_minimum():
    # Notes case 2: the new key breaks heap order, so x is cut to the root.
    h = FibonacciHeap()
    nodes = {k: h.insert(k) for k in (10, 20, 30, 40, 50)}
    h.extract_min()  # remove 10, building a tree with real parents
    assert_valid_heap(h)
    h.decrease_key(nodes[50], 1)
    assert_valid_heap(h)
    assert h.minimum() == 1
    assert [h.extract_min() for _ in range(4)] == [1, 20, 30, 40]


def test_cascading_cuts_keep_heap_valid():
    h = FibonacciHeap()
    nodes = [h.insert(k) for k in range(50)]
    h.extract_min()  # removes key 0 and builds multi-level trees
    assert_valid_heap(h)
    for node in nodes[1:]:
        h.decrease_key(node, node.key - 100)
        assert_valid_heap(h)
    assert h.n == 49
