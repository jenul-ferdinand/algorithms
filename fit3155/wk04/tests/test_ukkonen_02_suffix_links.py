from hypothesis import given
from hypothesis import strategies as st

from fit3155.wk04.src.NaiveSuffixTree import NaiveSuffixTree
from fit3155.wk04.src.Ukkonen01Naive import UkkonenNaive
from fit3155.wk04.src.Ukkonen02SuffixLinks import (
    ActiveState,
    Node,
    UkkonenSuffixLinks,
)
from fit3155.wk04.tests._serialize import _serialize

"""
Properties of suffix links

1. Root's suffix link is to itself

2. Every internal node has a suffix link

3. Suffix links only point to internal nodes

4. If node path label is xa then node.suffix_link path is a

"""

"""
Properties of the active node and remainder, let this be called the active state

The invariant of the active state is
path(root -> state.node) + S[state.remainder...i] = S[j..i]
"""


def _collect_internal_nodes(
    root: Node, S: str
) -> tuple[list[tuple[Node, str]], dict[str, Node]]:
    internals = []
    label_to_node = {}

    def dfs(node: Node, path: str):
        if node.suffix_start is None:
            internals.append((node, path))
            assert path not in label_to_node
            label_to_node[path] = node

        for edge in node.outgoing:
            if edge is not None:
                label = S[edge.start : edge.end + 1]
                dfs(edge.child, path + label)

    dfs(root, "")

    return internals, label_to_node


# Property (1)
@given(st.text(alphabet="abc", max_size=20))
def test_roots_suffix_link_is_to_itself(S):
    S = S + "$"
    ST = UkkonenSuffixLinks(S)
    assert ST.r.suffix_link == ST.r


@given(st.text(alphabet="abc", max_size=100))
def test_no_unresolved_suffix_link_source_after_construction(S):
    S = S + "$"
    ST = UkkonenSuffixLinks(S)
    assert ST.suffix_link_source is None


# Property (2,3,4)
@given(st.text(alphabet="abc", max_size=100))
def test_internal_suffix_links_follow_definition(S):
    S = S + "$"
    ST = UkkonenSuffixLinks(S)
    root = ST.r
    internal_nodes, label_to_node = _collect_internal_nodes(root, S)
    for node, path in internal_nodes:
        # only internal nodes checked
        assert node.suffix_start is None

        if node is root:  # below doesn't apply to root node
            continue

        # node path = xa -> node.suffix_link path = a
        target_path = path[1:]
        assert target_path in label_to_node
        assert node.suffix_link is label_to_node[target_path]

        # suffix links only point to internal nodes
        assert node.suffix_link.suffix_start is None


def _collect_internal_labels(root: Node, S: str) -> dict[int, str]:
    labels = {}

    def dfs(node: Node, path: str):
        if node.suffix_start is None:
            labels[id(node)] = path

        for edge in node.outgoing:
            if edge is not None:
                dfs(edge.child, path + S[edge.start : edge.end + 1])

    dfs(root, "")
    return labels


def _walk_from_root(ST, j, i):
    return ST._walk_down(ActiveState(node=ST.r, remainder_start=j), i)


@given(st.text(alphabet="abc", min_size=10, max_size=100))
def test_find_end_of_path_active_state_invariant(S):
    S = S + "$"
    ST = UkkonenSuffixLinks(S)
    labels = _collect_internal_labels(ST.r, S)

    for i in range(len(S)):
        for j in range(i + 1):
            _, state = _walk_from_root(ST, j, i)

            active_path = labels[id(state.node)]
            remainder = S[state.remainder_start : i]

            assert active_path + remainder == S[j:i]


@given(st.text(alphabet="abc", min_size=10, max_size=100))
def test_move_to_next_extension_active_state_invariant(S):
    S = S + "$"
    ST = UkkonenSuffixLinks(S)
    labels = _collect_internal_labels(ST.r, S)

    for i in range(len(S)):
        for j in range(1, i + 1):
            # previous extension was j-1
            _, prev_state = _walk_from_root(ST, j - 1, i)
            moved_state = ST._move_to_next_extension(prev_state, i)

            active_path = labels[id(moved_state.node)]
            remainder = S[moved_state.remainder_start : i]

            assert active_path + remainder == S[j:i]


@given(st.text(alphabet="abc", min_size=10, max_size=100))
def test_walk_from_active_state_invariant(S):
    S = S + "$"
    ST = UkkonenSuffixLinks(S)
    labels = _collect_internal_labels(ST.r, S)

    for i in range(len(S)):
        for j in range(1, i + 1):
            _, prev_state = _walk_from_root(ST, j - 1, i)

            moved_state = ST._move_to_next_extension(prev_state, i)
            _, walked_state = ST._walk_down(moved_state, i)

            active_path = labels[id(walked_state.node)]
            remainder = S[walked_state.remainder_start : i]

            assert active_path + remainder == S[j:i]

# Tree correctness
@given(st.text(alphabet="abc", max_size=100))
def test_tree_structure_matches_upto_02(S):
    S = S + "$"
    stnaive = NaiveSuffixTree(S)
    uknaive = UkkonenNaive(S)
    uksuff = UkkonenSuffixLinks(S)
    assert (
        _serialize(uknaive.r, S)
        == _serialize(uksuff.r, S)
        == _serialize(stnaive.r, S)
    )
