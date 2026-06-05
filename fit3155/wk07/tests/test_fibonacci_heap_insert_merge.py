from hypothesis import given
from hypothesis import strategies as st

from fit3155.wk07.src.FibonacciHeap import FibonacciHeap
from fit3155.wk07.tests._helpers import assert_valid_heap, drain, heap_of


def test_single_element():
    h = FibonacciHeap()
    h.insert(42)
    assert_valid_heap(h)
    assert h.minimum() == 42
    assert h.n == 1


def test_minimum_is_non_destructive():
    h = heap_of((5, 2, 8))
    assert h.minimum() == 2
    assert h.minimum() == 2
    assert h.n == 3


@given(st.lists(st.integers(-1000, 1000)))
def test_insert_keeps_structure_valid(keys):
    h = heap_of(keys)
    assert_valid_heap(h)
    assert h.n == len(keys)


def test_merge_into_empty():
    empty = FibonacciHeap()
    other = heap_of((4, 1, 7))
    empty.merge(other)
    assert_valid_heap(empty)
    assert empty.n == 3
    assert empty.minimum() == 1


def test_merge_empty_into_nonempty():
    h = heap_of((4, 1, 7))
    h.merge(FibonacciHeap())
    assert_valid_heap(h)
    assert h.n == 3
    assert h.minimum() == 1


@given(
    st.lists(st.integers(-1000, 1000)),
    st.lists(st.integers(-1000, 1000)),
)
def test_merge_drains_to_combined_sorted(a, b):
    ha = heap_of(a)
    hb = heap_of(b)
    ha.merge(hb)
    assert_valid_heap(ha)
    assert ha.n == len(a) + len(b)
    assert drain(ha) == sorted(a + b)
