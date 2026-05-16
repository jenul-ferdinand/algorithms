"""
Naive Implicit Suffix Tree
"""

from __future__ import annotations

from dataclasses import dataclass, field

from fit3155.common.constants import ALPHABET_SIZE, ascii_order


@dataclass
class Node:
    outgoing: list[Edge] = field(default_factory=lambda: [None] * ALPHABET_SIZE)
    suffix_start: int | None = None


@dataclass
class Edge:
    start: int
    end: int
    child: Node | None = None


class NaiveImplicitSuffixTree:
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
        self.S = S
        self.n = len(S)
        self.r = Node()

        # Phases i=1..n for all suffixes
        n = self.n
        for i in range(n):
            # Turn I_{i-1} into I_i by accomodating the new char S[i]

            # Extensions j=1..i for all prefixes of suffix
            for j in range(i + 1):
                # Extend suffix S[j..i-1] in the tree so it becomes S[j..i]
                walk_result = self._find_end_of_path(j, i)
                self._apply_extension(walk_result, j, i)

    def _find_end_of_path(self, j, i):
        S, r = self.S, self.r

        if j >= i:
            return ("at_node", r, None)

        curr: Node = r
        k = j
        while k <= i:
            # outgoing edge starting with char S[k]
            edge: Edge = curr.outgoing[ascii_order(S[k])]

            # walk
            e = edge.start
            while e <= edge.end and k < i:
                e += 1
                k += 1

            # path fully consumed
            if k == i:
                if e > edge.end:
                    return ("at_node", edge.child, edge)
                else:
                    return ("mid_edge", edge, e - edge.start)

            # consumed whole edge but still have more path to walk
            curr = edge.child

    def _apply_extension(
        self, walk_data: tuple[str, Node | Edge, int | None], j, i
    ):
        S = self.S

        # Walk ended at node
        if walk_data[0] == "at_node":
            u: Node = walk_data[1]

            # Leaf
            if u.suffix_start is not None:
                # Rule 1: Extend u's incoming edge's end index out to pos i
                incoming_edge: Edge = walk_data[2]
                incoming_edge.end = i
            # Internal
            else:
                # If there is an outgoing edge for the char
                if u.outgoing[ascii_order(S[i])] is not None:
                    # Rule 3: S[j..i] is already implicitly in the tree
                    # do nothing...
                    pass
                else:
                    # Rule 2, Case 1:
                    # Create a new leaf edge and node from u for S[i]
                    new_leaf = Node(suffix_start=j)
                    u.outgoing[ascii_order(S[i])] = Edge(
                        start=i, end=i, child=new_leaf
                    )
        # Walk ended mid edge
        elif walk_data[0] == "mid_edge":
            edge: Edge = walk_data[1]
            walked: int = walk_data[2]

            x = S[edge.start + walked]
            if x == S[i]:
                # Rule 3: S[j..i] is already implicitly in the tree
                # do nothing...
                pass
            else:
                # Rule 2, Case 2: Spliting by adding internal node
                original_end = edge.end
                original_child = edge.child
                u = Node()

                # the original edge becomes a shortened trunk
                edge.child = u
                edge.end = edge.start + walked - 1

                # create the remaining edge after the internal node
                remainder = Edge(
                    start=edge.start + walked,
                    end=original_end,
                    child=original_child,
                )
                u.outgoing[ascii_order(x)] = remainder

                # create a new leaf edge and node for S[i]
                new_leaf = Node(suffix_start=j)
                u.outgoing[ascii_order(S[i])] = Edge(
                    start=i, end=i, child=new_leaf
                )
