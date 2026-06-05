"""Deterministic work-profile checks for the suffix-tree implementations.

These tests intentionally avoid wall-clock timing.  The point is not that the
linear-time rapid implementation must beat every simpler implementation at a
small fixed n; Python constants can easily make the naive suffix tree faster
there.  Instead, we count the algorithmic work that the wk04 notes say each
optimisation removes.
"""

from fit3155.common.constants import ascii_order
from fit3155.wk04.src import Ukkonen03SkipCount as skip_mod
from fit3155.wk04.src import Ukkonen05RapidLeafExtension as rapid_mod
from fit3155.wk04.src.NaiveSuffixTree import (
    NaiveSuffixTree,
    TreeEdge,
    TreeNode,
)
from fit3155.wk04.src.Ukkonen01Naive import UkkonenNaive
from fit3155.wk04.src.Ukkonen02SuffixLinks import UkkonenSuffixLinks
from fit3155.wk04.src.Ukkonen03SkipCount import UkkonenSkipCount
from fit3155.wk04.src.Ukkonen04ShowStopper import UkkonenShowStopper
from fit3155.wk04.src.Ukkonen05RapidLeafExtension import (
    UkkonenRapidLeafExtension,
)


def _periodic_string(n: int) -> str:
    return ("abcd" * ((n + 3) // 4))[:n] + "$"


def _unary_string(n: int) -> str:
    return ("a" * n) + "$"


def _full_ukkonen_extension_count(S: str) -> int:
    n = len(S)
    return n * (n + 1) // 2


class _CountingNaiveSuffixTree(NaiveSuffixTree):
    def __init__(self, S: str):
        self.suffix_insertions = 0
        self.edge_lookups = 0
        self.char_comparisons = 0
        super().__init__(S)

    def _insert_suffix(self, i: int) -> None:
        self.suffix_insertions += 1

        S: str = self.S
        n: int = self.n
        curr: TreeNode = self.r

        k = i
        while k < n:
            self.edge_lookups += 1
            edge: TreeEdge | None = curr.outgoing[ascii_order(S[k])]

            if edge is None:
                leaf_node = TreeNode(suffix_start=i)
                leaf_edge = TreeEdge(start=k, end=n - 1, child=leaf_node)
                curr.outgoing[ascii_order(S[k])] = leaf_edge
                break

            e = edge.start
            while e <= edge.end and k < n:
                self.char_comparisons += 1
                if S[k] != S[e]:
                    break
                e += 1
                k += 1

            if e <= edge.end:
                self._split_edge(e, i, k, n, edge)
                break

            curr = edge.child


class _CountingUkkonenNaive(UkkonenNaive):
    def __init__(self, S: str):
        self.extension_count = 0
        self.root_walk_chars = 0
        super().__init__(S)

    def _find_end_of_path(self, j: int, i: int):
        self.root_walk_chars += i - j
        return super()._find_end_of_path(j, i)

    def _apply_extension(self, extension_point, j: int, i: int) -> None:
        self.extension_count += 1
        super()._apply_extension(extension_point, j, i)


class _CountingSuffixLinks(UkkonenSuffixLinks):
    def __init__(self, S: str):
        self.extension_count = 0
        self.suffix_link_moves = 0
        self.remainder_chars_walked = 0
        super().__init__(S)

    def _walk_down(self, state, i: int):
        self.remainder_chars_walked += i - state.remainder_start
        return super()._walk_down(state, i)

    def _move_to_next_extension(self, state, i: int):
        self.suffix_link_moves += 1
        return super()._move_to_next_extension(state, i)

    def _apply_extension(self, extension_point, j: int, i: int) -> None:
        self.extension_count += 1
        super()._apply_extension(extension_point, j, i)


class _CountingSkipCount(UkkonenSkipCount):
    def __init__(self, S: str):
        self.extension_count = 0
        self.suffix_link_moves = 0
        self.logical_remainder_chars = 0
        self.walk_edge_lookups = 0
        self._inside_walk = False

        original_find_edge = skip_mod.Node.find_edge

        def counted_find_edge(node, c: str):
            if self._inside_walk:
                self.walk_edge_lookups += 1
            return original_find_edge(node, c)

        skip_mod.Node.find_edge = counted_find_edge
        try:
            super().__init__(S)
        finally:
            skip_mod.Node.find_edge = original_find_edge

    def _walk_down(self, state, i: int):
        self.logical_remainder_chars += i - state.remainder_start
        self._inside_walk = True
        try:
            return super()._walk_down(state, i)
        finally:
            self._inside_walk = False

    def _move_to_next_extension(self, state, i: int):
        self.suffix_link_moves += 1
        return super()._move_to_next_extension(state, i)

    def _apply_extension(self, extension_point, j: int, i: int) -> None:
        self.extension_count += 1
        super()._apply_extension(extension_point, j, i)


class _CountingShowStopper(UkkonenShowStopper):
    def __init__(self, S: str):
        self.extension_count = 0
        super().__init__(S)

    def _apply_extension(self, extension_point, j: int, i: int) -> bool:
        self.extension_count += 1
        return super()._apply_extension(extension_point, j, i)


class _CountingRapid(UkkonenRapidLeafExtension):
    def __init__(self, S: str):
        self.extension_count = 0
        self.suffix_link_moves = 0
        self.logical_remainder_chars = 0
        self.walk_edge_lookups = 0
        self._inside_walk = False

        original_find_edge = rapid_mod.Node.find_edge

        def counted_find_edge(node, c: str):
            if self._inside_walk:
                self.walk_edge_lookups += 1
            return original_find_edge(node, c)

        rapid_mod.Node.find_edge = counted_find_edge
        try:
            super().__init__(S)
        finally:
            rapid_mod.Node.find_edge = original_find_edge

    def _walk_down(self, state, i: int):
        self.logical_remainder_chars += i - state.remainder_start
        self._inside_walk = True
        try:
            return super()._walk_down(state, i)
        finally:
            self._inside_walk = False

    def _move_to_next_extension(self, state, i: int):
        self.suffix_link_moves += 1
        return super()._move_to_next_extension(state, i)

    def _apply_extension(self, extension_point, j: int, i: int) -> bool:
        self.extension_count += 1
        return super()._apply_extension(extension_point, j, i)


def test_ukkonen_extension_counts_show_rule_optimisations():
    S = _periodic_string(120)
    full_extensions = _full_ukkonen_extension_count(S)

    naive = _CountingUkkonenNaive(S)
    suffix_links = _CountingSuffixLinks(S)
    skip_count = _CountingSkipCount(S)
    showstopper = _CountingShowStopper(S)
    rapid = _CountingRapid(S)

    assert naive.extension_count == full_extensions
    assert suffix_links.extension_count == full_extensions
    assert skip_count.extension_count == full_extensions

    assert showstopper.extension_count < full_extensions
    assert rapid.extension_count < showstopper.extension_count
    assert rapid.extension_count <= 2 * len(S)


def test_skip_count_replaces_character_remainder_walks_with_edge_hops():
    S = _periodic_string(240)

    suffix_links = _CountingSuffixLinks(S)
    skip_count = _CountingSkipCount(S)

    assert suffix_links.remainder_chars_walked > 0
    assert skip_count.walk_edge_lookups > 0
    assert (
        suffix_links.remainder_chars_walked > 3 * skip_count.walk_edge_lookups
    )


def test_rapid_explicit_extensions_are_linear_not_quadratic():
    S = _periodic_string(400)
    full_extensions = _full_ukkonen_extension_count(S)
    rapid = _CountingRapid(S)

    assert rapid.extension_count <= 2 * len(S)
    assert full_extensions > 50 * rapid.extension_count


def test_rapid_work_scales_linearly_without_wall_clock_timing():
    small = _CountingRapid(_periodic_string(100))
    large = _CountingRapid(_periodic_string(400))

    assert large.extension_count <= 5 * small.extension_count
    assert large.walk_edge_lookups <= 5 * small.walk_edge_lookups


def test_naive_suffix_tree_can_win_constants_but_has_quadratic_work_profile():
    small_naive = _CountingNaiveSuffixTree(_unary_string(80))
    large_naive = _CountingNaiveSuffixTree(_unary_string(320))

    small_rapid = _CountingRapid(_unary_string(80))
    large_rapid = _CountingRapid(_unary_string(320))

    assert small_naive.suffix_insertions == len(_unary_string(80))
    assert large_naive.char_comparisons > 8 * small_naive.char_comparisons
    assert large_rapid.extension_count <= 5 * small_rapid.extension_count
