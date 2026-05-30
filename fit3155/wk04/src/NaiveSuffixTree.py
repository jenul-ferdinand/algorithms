"""
Naive Suffix Tree (notes section 1)

For construction we insert each full suffix S[i..n] into T_{i-1} one at a time.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from fit3155.common.constants import ALPHABET_SIZE, TERMINAL_CHAR, ascii_order


@dataclass
class TreeNode:
    outgoing: list[TreeEdge | None] = field(
        default_factory=lambda: [None] * ALPHABET_SIZE
    )
    suffix_start: int | None = None

    def __repr__(self):
        outgoing = [edge for edge in self.outgoing if edge is not None]
        return f"Node(j={self.suffix_start}, outgoing_edges={len(outgoing)})"


@dataclass
class TreeEdge:
    start: int
    end: int
    child: TreeNode

    def __repr__(self):
        return f"Edge(j={self.start}, i={self.end}, child={self.child})"


class NaiveSuffixTree:
    """
    Constructs a Suffix Tree Naively (notes section 1)

    For construction we insert each full suffix S[i..n] into T_{i-1} one at a
    time.

    Time complexity: O(n^2)
        - Iterating through each of the n suffixes, and,
        - Walking down at most O(n) characters per suffix to find its
          insertion point (splitting an edge or attaching a new leaf).
    Space complexity: O(n)
        - Edge labels are stored implicitly as (start, end) index pairs into
          S rather than as explicit substrings.
        - The tree has at most 2n - 1 nodes for a string of length n.
    """

    def __init__(self, S: str):
        if S[-1] != TERMINAL_CHAR:
            S = S + TERMINAL_CHAR

        self.S: str = S
        self.n: int = len(S)
        self.r: TreeNode = TreeNode()

        # Insert all n suffixes of string S
        n = len(S)
        for i in range(n):
            self._insert_suffix(i)

    def get_root(self) -> TreeNode:
        return self.r

    def _insert_suffix(self, i: int) -> None:
        S: str = self.S
        n: int = self.n
        curr: TreeNode = self.r

        k = i  # where we are in the current suffix
        while k < n:
            edge: TreeEdge | None = curr.outgoing[ascii_order(S[k])]

            if edge is None:
                # First char of label doesn't match first char of suffix
                # so we create a new leaf node with long edge containing the
                # whole suffix.
                leaf_node = TreeNode(suffix_start=i)
                leaf_edge = TreeEdge(start=k, end=n - 1, child=leaf_node)
                curr.outgoing[ascii_order(S[k])] = leaf_edge
                break

            # Edge comparisons + pointer progression down the edge
            e = edge.start
            while e <= edge.end and S[k] == S[e]:
                e += 1
                k += 1

            if e <= edge.end:
                self._split_edge(e, i, k, n, edge)
                break

            # Full Match: e > edge.i matched the whole edge label
            # so we go to the next node
            curr = edge.child

    def _split_edge(self, e: int, i: int, k: int, n: int, edge: TreeEdge):
        # Edge splitting on a mismatch
        # a new internal node is created, with a new edge and leaf node
        # for the remaining characters
        S = self.S
        original_i = edge.end
        original_child = edge.child
        u = TreeNode()

        # the original edge becomes a shortened trunk
        edge.child = u
        edge.end = e - 1

        # add remaining edge from internal node to original node
        remainder_edge = TreeEdge(
            start=e,
            end=original_i,
            child=original_child,
        )
        u.outgoing[ascii_order(S[e])] = remainder_edge

        # create the leaf node for the suffix edge
        new_leaf = TreeNode(suffix_start=i)
        new_edge = TreeEdge(start=k, end=n - 1, child=new_leaf)
        u.outgoing[ascii_order(S[k])] = new_edge
