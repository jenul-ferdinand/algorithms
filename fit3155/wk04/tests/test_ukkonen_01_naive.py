from hypothesis import given
from hypothesis import strategies as st

from fit3155.common.constants import ascii_order
from fit3155.wk04.src.Ukkonen01Naive import Edge, Node, UkkonenNaive


def assert_implicit_suffix_tree(root: Node, S):
    n = len(S)
    for j in range(n):
        assert can_trace(root, S, j, n - 1), f"Suffix S[{j}..n-1] not in tree"


def can_trace(root: Node, S: str, start: int, end: int):
    """Walk S[start..end] from root. Return True if fully consumed"""
    curr = root
    k = start
    while k <= end:
        edge: Edge = curr.outgoing[ascii_order(S[k])]
        print(curr)
        print(edge)
        if edge is None:
            return False
        e = edge.start
        while e <= edge.end and k <= end:
            if S[e] != S[k]:
                return False
            e += 1
            k += 1
        if k > end:
            return True
        curr = edge.child
        if curr is None:
            return False
    return True


def collect_leaves_with_paths(root: Node, S):
    """DFS the tree, return list of (leaf_node, path_label) pairs."""
    results = []

    def dfs(node: Node, path):
        if node.suffix_start is not None:  # leaf
            results.append((node, path))
            return
        for edge in node.outgoing:
            if edge is None:
                continue
            label = S[edge.start : edge.end + 1]
            dfs(edge.child, path + label)

    dfs(root, "")
    return results


@given(st.text(alphabet="abc", min_size=1, max_size=20))
def test_every_suffix_traceable(S):
    tree = UkkonenNaive(S).r
    for j in range(len(S)):
        assert can_trace(tree, S, j, len(S) - 1)


@given(st.text(alphabet="abc", min_size=1, max_size=20))
def test_with_terminal_becomes_valid_suffix_tree(S):
    S_term = S + "$"
    tree = UkkonenNaive(S_term).r
    leaf_paths = [path for _, path in collect_leaves_with_paths(tree, S_term)]
    expected = [S_term[j:] for j in range(len(S_term))]
    assert sorted(leaf_paths) == sorted(expected)
