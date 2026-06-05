"""
Ukkonen's Algorithm with Rapid Leaf Extension (notes section 3.7)

Replaces explicit Rule 1 extensions with an implicit globalEnd pointer.
Eveiry leaf edge stores its end as a reference to globalEnd rather than as
a concrete index, so incrementing globalEnd at the start of each phase
implicitly extends every leaf in the tree by the new character.

Combined with the lastj counter, all Rule 1 extensions in a phase are
performed in O(1) and we begin explicit extensions from j = lastj + 1. this
yields the final O(n) construction time.

At this point the algorithm is the complete Ukkonen's algorithm.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeAlias

from fit3155.common.constants import ALPHABET_SIZE, ascii_order
from fit3155.wk04.src._edge_rendering import render_edge
from fit3155.wk04.src._node_rendering import render_node
from fit3155.wk04.src._suffix_tree_rendering import render_suffix_tree


@dataclass
class Node:
    outgoing: list[Edge | None] = field(
        default_factory=lambda: [None] * ALPHABET_SIZE
    )
    suffix_start: int | None = None
    suffix_link: Node | None = None

    @property
    def is_leaf(self) -> bool:
        return self.suffix_start is not None

    def create_edge(self, c: str, start: int, end: int, child: Node):
        self.outgoing[ascii_order(c)] = Edge(start, end, child)

    def find_edge(self, c: str) -> Edge | None:
        return self.outgoing[ascii_order(c)]

    def __repr__(self) -> str:
        return render_node(self)


@dataclass
class Edge:
    start: int
    end: int
    child: Node | None = None

    def __repr__(self) -> str:
        return render_edge(self)


@dataclass
class ActiveState:
    node: Node
    remainder_start: int


@dataclass
class AtNode:
    node: Node


@dataclass
class MidEdge:
    edge: Edge
    chars_into_edge: int


ExtensionPoint: TypeAlias = AtNode | MidEdge


class UkkonenRapidLeafExtension:
    def __init__(self, S: str):
        self.S: str = S
        self.n: int = len(S)

        self.r: Node = Node()
        self.r.suffix_link = self.r

        self.suffix_link_source: Node | None = None

        self.global_end: int = -1
        self.last_j: int = -1

        self._build()

    def _build(self) -> None:
        n = self.n

        state = ActiveState(node=self.r, remainder_start=0)
        skip_move_to_next = True

        # Phases i=0..n-1 for all suffixes
        for i in range(n):
            # Turn I_{i-1} into I_i by accomodating the new char S[i]

            # All Rule 1 extensions in this phase (j=0..last_j) happen here,
            # implicitly, by mutating globalEnd. The single line replaces up to
            # last_j+1 explicit traversals.
            self.global_end = i

            for j in range(self.last_j + 1, i + 1):
                # S3.8 we don't follow a suffix link after a Rule 3. This also
                # covers the very first extension of all, which has no previous
                # state to advance from.
                if not skip_move_to_next:
                    state = self._move_to_next_extension(state, i)
                skip_move_to_next = False

                extension_point, state = self._walk_down(state, i)
                rule_3 = self._apply_extension(extension_point, j, i)

                if rule_3:
                    # Showstopper. Leave the state along; the next phase's
                    # walk_down picks up from the same point with the new
                    # (larger) i, naturally extending the walk by one character.
                    skip_move_to_next = True
                    break

            assert self.suffix_link_source is None, (
                f"phase {i} ended with unresolved suffix link source"
            )

    # TRAVERSAL ----------------------------------------------------------------

    def _walk_down(
        self, state: ActiveState, i: int
    ) -> tuple[ExtensionPoint, ActiveState]:
        S = self.S

        curr: Node = state.node
        k: int = state.remainder_start

        if k == i:
            # No characters available in S[k..i] to walk
            # already at the extension point
            extension_point = AtNode(node=curr)
            state = ActiveState(node=curr, remainder_start=i)
            return extension_point, state

        while k < i:
            edge_path_start = k
            # outgoing edge starting with char S[k]
            edge: Edge = curr.find_edge(S[k])
            assert edge is not None

            # counting
            edge_length = self._end(edge) - edge.start + 1
            chars_remaining = i - k
            if chars_remaining < edge_length:
                # mid-edge: remainder runs out partway down this edge
                extension_point = MidEdge(edge, chars_into_edge=chars_remaining)
                state = ActiveState(node=curr, remainder_start=edge_path_start)
                return extension_point, state
            # skipping
            k += edge_length

            if k == i:
                # path fully consumed at node
                extension_point = AtNode(node=edge.child)
                if edge.child.is_leaf:
                    # leaf: active node = parent, remainder = whole leaf edge
                    state = ActiveState(
                        node=curr, remainder_start=edge_path_start
                    )
                else:
                    # internal: active node = edge.child itself, no remainder
                    state = ActiveState(node=edge.child, remainder_start=i)
                return extension_point, state

            # consumed whole edge but still have more path to walk
            curr = edge.child

        raise AssertionError("walk down fell through")

    def _move_to_next_extension(
        self, state: ActiveState, i: int
    ) -> ActiveState:
        if state.node is self.r:
            assert state.remainder_start < i, (
                "empty remainder at root has no first char to drop"
            )
            return ActiveState(
                node=self.r,
                remainder_start=state.remainder_start + 1,
            )
        assert state.node.suffix_link is not None
        return ActiveState(
            node=state.node.suffix_link,
            remainder_start=state.remainder_start,
        )

    def _end(self, edge: Edge) -> int:
        if edge.child.is_leaf:
            return self.global_end
        return edge.end

    # EXTENSIONS ---------------------------------------------------------------

    def _apply_extension(
        self, extension_point: ExtensionPoint, j: int, i: int
    ) -> bool:
        S = self.S

        created_internal_node: Node | None = None
        suffix_link_target: Node | None = None
        did_rule_3 = False

        match extension_point:
            case AtNode(node=u):
                assert not u.is_leaf, (
                    "explicit extensions can't end at a leaf in rapid leaf"
                    "extension (Lemmas 4 & 5)"
                )
                if u.find_edge(S[i]) is not None:
                    # Rule 3: S[j..i] is already implicitly in the tree
                    suffix_link_target = u
                    did_rule_3 = True
                else:
                    # Rule 2, Case 1: new leaf edge and node from u for S[i]
                    self._new_leaf(j=j, edge_start=i, parent=u)
                    suffix_link_target = u
                    self.last_j = j

            case MidEdge(edge=edge, chars_into_edge=chars_into_edge):
                x = S[edge.start + chars_into_edge]
                if x == S[i]:
                    # Rule 3: S[j..i] is already implicitly in the tree
                    did_rule_3 = True
                else:
                    # Rule 2, Case 2: split the edge, then hang a new leaf off
                    # the inserted internal node u
                    created_internal_node = self._split_edge(
                        edge, chars_into_edge
                    )
                    suffix_link_target = created_internal_node
                    self._new_leaf(
                        j=j, edge_start=i, parent=created_internal_node
                    )
                    self.last_j = j

        if self.suffix_link_source is not None:
            assert suffix_link_target is not None, (
                "Target of suffix link should be a Node"
            )
            self.suffix_link_source.suffix_link = suffix_link_target

        # last new internal node to new internal node
        self.suffix_link_source = created_internal_node

        return did_rule_3

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

    def _new_leaf(self, j: int, edge_start: int, parent: Node) -> None:
        """
        Create a new leaf labelled with suffix index j and attach it to `parent`
        via a new edge. `end` for this leaf node's edge is a sentinel, we use
        _end() now so this value is never read.
        """
        S = self.S
        leaf = Node(suffix_start=j)
        parent.create_edge(
            S[edge_start],
            start=edge_start,
            end=-1,
            child=leaf,
        )

    def __repr__(self) -> str:
        S, r = self.S, self.r
        return render_suffix_tree(
            name=type(self).__name__,
            S=S,
            root=r,
        )
