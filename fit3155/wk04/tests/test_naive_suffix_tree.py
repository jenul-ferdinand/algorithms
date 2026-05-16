from hypothesis import given
from hypothesis import strategies as st

from fit3155.common.constants import ALPHABET, TERMINAL_CHAR
import importlib

_mod = importlib.import_module("fit3155.wk04.src.02_NaiveSuffixTree")
TreeEdge = _mod.TreeEdge
TreeNode = _mod.TreeNode
NaiveSuffixTree = _mod.NaiveSuffixTree

"""
Suffix Tree Properties

For S[0..n-1] is a tree with

1. exactly n leaves numbered 1..n
2. all internal nodes have at least two children
3. each edge is labelled with a substring of S
4. the same node can't have two or more outgoing whose labels start with the
   same character
5. if you start at the root node and walk to leaf i, the characters you read
   along the way spell out suffix S[i..n]
"""


def _collect_leaves(root: TreeNode):
    stack = [root]
    leaves: list[TreeNode] = []

    while stack:
        node: TreeNode = stack.pop()
        print(node)
        print([edge for edge in node.outgoing if edge is not None])
        available_edges = [edge for edge in node.outgoing if edge is not None]
        if len(available_edges) <= 0:
            leaves.append(node)
        else:
            all_children_of_edges = [edge.child for edge in available_edges]
            stack.extend(all_children_of_edges)

    return sorted(leaves, key=lambda x: x.j)


def _collect_edges(root: TreeNode):
    stack = [root]
    edges: list[TreeEdge] = []

    while stack:
        node = stack.pop()
        available_edges = [edge for edge in node.outgoing if edge is not None]
        for edge in available_edges:
            edges.append(edge)
            all_children_of_edges = [edge.child for edge in available_edges]
            stack.extend(all_children_of_edges)

    return edges


def _collect_internal_nodes(root: TreeNode):
    nodes: list[TreeNode] = []
    stack: list[TreeNode] = [root]

    while stack:
        node = stack.pop()
        nodes.append(node)
        available_edges = [edge for edge in node.outgoing if edge is not None]
        for _ in available_edges:
            all_children_of_edges = [edge.child for edge in available_edges]
            stack.extend(all_children_of_edges)

    # Filter out leaf nodes
    internal_nodes = []
    for node in nodes[1:]:
        if node.j is not None:
            internal_nodes.append(node)

    return internal_nodes


# Property (1)
def test_sames_no_leaves_as_no_suffixes():
    string = "aabaa$"
    n = len(string)
    root = NaiveSuffixTree(string).get_root()
    leaves = _collect_leaves(root)

    assert len(leaves) == n


@given(st.text(alphabet=ALPHABET, max_size=100))
def test_tree_has_same_number_of_leaves_as_suffixes_in_total(string):
    string = string + TERMINAL_CHAR
    n = len(string)
    root = NaiveSuffixTree(string).get_root()
    leaves = _collect_leaves(root)

    assert len(leaves) == n


# Property (2)
@given(st.text(alphabet=ALPHABET, max_size=100))
def test_all_internal_nodes_have_at_least_two_children(string):
    string = string + TERMINAL_CHAR
    root = NaiveSuffixTree(string).get_root()
    internal_nodes: list[TreeNode] = _collect_internal_nodes(root)
    for node in internal_nodes:
        assert len(node.outgoing) >= 2


# Property (3)
@given(st.text(alphabet=ALPHABET, max_size=100))
def test_all_edges_have_start_index_less_than_or_equal_to_end_index(string):
    string = string + TERMINAL_CHAR
    root = NaiveSuffixTree(string).get_root()
    edges = _collect_edges(root)
    for edge in edges:
        assert edge.j <= edge.i


# Property (4)
# the same node can't have two or more outgoing whose labels start with the
# same character
@given(st.text(alphabet=ALPHABET, max_size=100, min_size=10))
def test_a_node_cant_have_duplicate_edges_starting_with_same_char(string):
    string = string + TERMINAL_CHAR
    root = NaiveSuffixTree(string).get_root()

    stack = [root]
    while stack:
        node = stack.pop()
        outgoing: list[TreeEdge] = [
            edge for edge in node.outgoing if edge is not None
        ]

        for i in range(len(outgoing)):
            for j in range(len(outgoing)):
                if i == j:
                    continue
                assert outgoing[i].j != outgoing[j].j

        children: list[TreeNode] = [edge.child for edge in outgoing]
        stack.extend(children)


# Property (5)
# if you start at the root node and walk to leaf i, the characters you read
# along the way spell out suffix S[i..n]
@given(st.text(alphabet=ALPHABET, max_size=100, min_size=10))
def test_walking_from_root_to_leaf_i_spells_out_suffix_i(string):
    string = string + TERMINAL_CHAR
    root = NaiveSuffixTree(string).get_root() # noqa
