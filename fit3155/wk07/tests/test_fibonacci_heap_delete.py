from fit3155.wk07.src.FibonacciHeap import FibonacciHeap
from fit3155.wk07.tests._helpers import assert_valid_heap, drain


def test_delete_arbitrary_nodes():
    h = FibonacciHeap()
    keys = [5, 1, 8, 3, 9, 2, 7, 4, 6]
    nodes = {k: h.insert(k) for k in keys}
    h.delete(nodes[8])
    h.delete(nodes[1])
    assert_valid_heap(h)
    assert h.n == len(keys) - 2
    assert drain(h) == sorted(set(keys) - {1, 8})


def test_delete_current_minimum():
    h = FibonacciHeap()
    nodes = {k: h.insert(k) for k in (3, 1, 4, 5, 2)}
    h.delete(nodes[1])  # delete the current minimum
    assert_valid_heap(h)
    assert h.minimum() == 2
    assert drain(h) == [2, 3, 4, 5]


def test_delete_every_node_one_by_one():
    h = FibonacciHeap()
    nodes = [h.insert(k) for k in range(20)]
    h.extract_min()  # consolidate first so deletes also hit internal nodes
    remaining = 19
    for node in nodes[1:]:
        h.delete(node)
        remaining -= 1
        assert_valid_heap(h)
        assert h.n == remaining
    assert h.min is None
