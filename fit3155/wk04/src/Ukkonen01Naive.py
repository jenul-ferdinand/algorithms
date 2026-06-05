"""
Naive Implicit Suffix Tree (notes section 3.2)

Note: the notes write edge labels as (j, i) tuples, but we use (start, end)
on Edge to avoid clashing with the phase/extension indices i and j.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeAlias

from fit3155.common.constants import ALPHABET_SIZE, ascii_order
from fit3155.wk04.src._suffix_tree_rendering import render_suffix_tree


@dataclass
class Node:
    outgoing: list[Edge | None] = field(
        default_factory=lambda: [None] * ALPHABET_SIZE
    )
    suffix_start: int | None = None

    @property
    def is_leaf(self) -> bool:
        return self.suffix_start is not None

    def create_edge(self, c: str, start: int, end: int, child: Node):
        self.outgoing[ascii_order(c)] = Edge(start, end, child)

    def find_edge(self, c: str) -> Edge | None:
        return self.outgoing[ascii_order(c)]

    def __repr__(self):
        populated = {i: e for i, e in enumerate(self.outgoing) if e is not None}
        return f"Node(suffix_start={self.suffix_start}, outgoing={populated})"


@dataclass
class Edge:
    start: int
    end: int
    child: Node | None = None

    def __repr__(self):
        return f"Edge(start={self.start}, end={self.end}, child={self.child})"


@dataclass
class AtNode:
    node: Node
    incoming_edge: Edge | None


@dataclass
class MidEdge:
    edge: Edge
    chars_into_edge: int


ExtensionPoint: TypeAlias = AtNode | MidEdge


class UkkonenNaive:
    """
    Constructs an Implicit Suffix Tree Naively (notes section 3.2)

    For construction we proceed over n phases. In each phase i we grow the
    previous implicit suffix tree I_{i-1} into I_i by performing extension j
    for each j in 1..i+1, extending the path S[j..i-1] in the tree with the
    new character S[i] via one of three rules (Rule 1, Rule 2, or Rule 3).

    Time complexity: O(n^3)
        - n phases, each with up to n extensions, and,
        - Each extension walks O(n) characters from the root to find its
          extension point.
    Space complexity: O(n)
        - Edge labels are stored implicitly as (start, end) index pairs.
        - The implicit tree has at most 2n - 1 nodes for a string of length n.
    """

    def __init__(self, S: str):
        self.S: str = S
        self.n: int = len(S)
        self.r: Node = Node()

        self._build()

    def _build(self) -> None:
        # Phases i=0..n-1 for all suffixes
        for i in range(self.n):
            # Turn I_{i-1} into I_i by accomodating the new char S[i]

            # Extensions j=0..i for all prefixes of suffix
            for j in range(i + 1):
                # Extend suffix S[j..i-1] in the tree so it becomes S[j..i]
                walk: ExtensionPoint = self._find_end_of_path(j, i)
                self._apply_extension(walk, j, i)

    def _find_end_of_path(self, j: int, i: int) -> ExtensionPoint:
        S, r = self.S, self.r

        if j >= i:
            return AtNode(node=r, incoming_edge=None)

        curr: Node = r
        k = j
        while k <= i:
            # outgoing edge starting with char S[k]
            edge: Edge = curr.find_edge(S[k])

            # walk chars in edge
            e = edge.start
            while e <= edge.end and k < i:
                e += 1
                k += 1

            # path fully consumed
            if k == i:
                if e > edge.end:
                    return AtNode(node=edge.child, incoming_edge=edge)
                else:
                    return MidEdge(edge=edge, chars_into_edge=e - edge.start)

            # consumed whole edge but still have more path to walk
            curr = edge.child

        raise AssertionError(f"walk fell through at j={j}, i={i}")

    def _apply_extension(
        self, extension_point: ExtensionPoint, j: int, i: int
    ) -> None:
        S = self.S

        match extension_point:
            case AtNode(node=u, incoming_edge=incoming):
                if u.is_leaf:
                    # Rule 1: extend u's incoming edge's end index out to pos i
                    incoming.end = i
                else:
                    if u.find_edge(S[i]) is not None:
                        # Rule 3: S[j..i] is already implicitly in the tree
                        pass
                    else:
                        # Rule 2, Case 1: new leaf edge and node from u for S[i]
                        self._new_leaf(j=j, edge_start=i, edge_end=i, parent=u)

            case MidEdge(edge=edge, chars_into_edge=chars_into_edge):
                x = S[edge.start + chars_into_edge]
                if x == S[i]:
                    # Rule 3: S[j..i] is already implicitly in the tree
                    pass
                else:
                    # Rule 2, Case 2: split the edge, then hang a new leaf off
                    # the inserted internal node u
                    u = self._split_edge(
                        edge=edge, chars_into_edge=chars_into_edge
                    )
                    self._new_leaf(j=j, edge_start=i, edge_end=i, parent=u)

    def _split_edge(self, edge: Edge, chars_into_edge: int) -> Node:
        S = self.S
        original_end = edge.end
        original_child = edge.child
        leftover_start = edge.start + chars_into_edge

        u = Node()

        # original edge becomes a shortened trunk
        edge.child = u
        edge.end = edge.start + chars_into_edge - 1

        # remaining leaf edge and node from internal node
        u.create_edge(
            S[leftover_start],
            start=leftover_start,
            end=original_end,
            child=original_child,
        )

        return u

    def _new_leaf(
        self, j: int, edge_start: int, edge_end: int, parent: Node
    ) -> None:
        """
        Create a new leaf labelled with suffix index j and attach it to
        `parent` via a new edge labelled S[edge_start..edge_end].
        """
        S = self.S
        leaf = Node(suffix_start=j)
        parent.create_edge(
            S[edge_start],
            start=edge_start,
            end=edge_end,
            child=leaf,
        )

    def __repr__(self) -> str:
        S, r = self.S, self.r
        return render_suffix_tree(
            name=type(self).__name__,
            S=S,
            root=r,
        )