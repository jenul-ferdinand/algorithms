from hypothesis import given
from hypothesis import strategies as st

from fit3155.wk07.src.FibonacciHeap import FibonacciHeap
from fit3155.wk07.tests._helpers import (
    assert_valid_heap,
    drain,
    heap_of,
    roots,
)


def test_empty_heap_extract_returns_none():
    h = FibonacciHeap()
    assert h.extract_min() is None
    assert h.min is None
    assert h.n == 0


def test_extract_single_element():
    h = heap_of((7,))
    assert h.extract_min() == 7
    assert h.min is None
    assert h.n == 0
    assert h.extract_min() is None


@given(st.lists(st.integers(-1000, 1000)))
def test_insert_then_drain_is_sorted(keys):
    h = heap_of(keys)
    assert drain(h) == sorted(keys)
    assert h.min is None
    assert h.n == 0


def test_duplicate_keys_drain_sorted():
    keys = [3, 1, 3, 2, 1, 2, 3, 1]
    h = heap_of(keys)
    assert drain(h) == sorted(keys)
    assert h.n == 0


def test_root_degrees_distinct_after_extract():
    # The notes: after consolidation the root list holds at most one tree
    # of any given degree.
    h = heap_of(range(100))
    h.extract_min()
    assert_valid_heap(h)
    degrees = [r.degree for r in roots(h)]
    assert len(degrees) == len(set(degrees)), "two roots share a degree"
