"""Model-based stress test driving random sequences of every operation."""

from hypothesis import settings
from hypothesis import strategies as st
from hypothesis.stateful import (
    RuleBasedStateMachine,
    invariant,
    precondition,
    rule,
)

from fit3155.wk07.src.FibonacciHeap import FibonacciHeap
from fit3155.wk07.tests._helpers import assert_valid_heap


class FibonacciHeapMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.heap = FibonacciHeap()
        self.live: list[list] = []  # entries are [node, key]

    def _keys(self) -> set[int]:
        return {key for _, key in self.live}

    @rule(base=st.integers(-1000, 1000))
    def insert(self, base):
        key = base
        used = self._keys()
        while key in used:
            key += 1
        node = self.heap.insert(key)
        self.live.append([node, key])

    @precondition(lambda self: self.live)
    @rule()
    def extract_min(self):
        expected = min(key for _, key in self.live)
        assert self.heap.extract_min() == expected
        idx = next(i for i, (_, k) in enumerate(self.live) if k == expected)
        self.live.pop(idx)

    @precondition(lambda self: self.live)
    @rule(data=st.data(), drop=st.integers(0, 500))
    def decrease_key(self, data, drop):
        i = data.draw(st.integers(0, len(self.live) - 1))
        node, key = self.live[i]
        used = self._keys() - {key}
        target = key - drop
        while target in used:
            target -= 1
        self.heap.decrease_key(node, target)
        self.live[i][1] = target

    @precondition(lambda self: self.live)
    @rule(data=st.data())
    def delete(self, data):
        i = data.draw(st.integers(0, len(self.live) - 1))
        node = self.live[i][0]
        self.heap.delete(node)
        self.live.pop(i)

    @invariant()
    def matches_model(self):
        assert_valid_heap(self.heap)
        assert self.heap.n == len(self.live)
        if self.live:
            assert self.heap.minimum() == min(k for _, k in self.live)


TestFibonacciHeapMachine = FibonacciHeapMachine.TestCase
TestFibonacciHeapMachine.settings = settings(
    max_examples=150, stateful_step_count=40, deadline=None
)
