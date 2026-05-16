from __future__ import annotations

from dataclasses import dataclass, field

from fit3155.common.constants import ALPHABET_SIZE, TERMINAL_CHAR, ascii_order


@dataclass
class TrieNode:
    outgoing: list[TrieEdge] = field(default_factory=[None] * ALPHABET_SIZE)
    j: int | None = None

    def __repr__(self):
        outgoing = []
        for edge in self.outgoing:
            if edge is not None:
                outgoing.append(edge)
        return f"Node(suffix_start={self.j}, outgoing_edges={len(outgoing)})"


@dataclass
class TrieEdge:
    label: str
    child: TrieNode

    def __repr__(self):
        return f"Edge(label={self.label}, child={self.child})"


def naive_suffix_trie(string: str) -> TrieNode:
    """
    Constructs a Suffix Trie Naively

    Time complexity: O(n^2)
        - Iterating through each character in the original string, and,
        - Inserting all suffixes of the original string into the Trie.
    Space complexity: O(n^2)
        - Storing all suffixes of the original string in the Trie.
    """
    if string[-1] != TERMINAL_CHAR:
        string = string + TERMINAL_CHAR

    n = len(string)

    root = TrieNode()
    print(root)
    for i in range(n):
        print("Working with a new suffix")

        curr: TrieNode = root
        for char in string[i:]:
            char_order = ascii_order(char)
            if curr.outgoing[char_order] is not None:
                # Check for an existing edge
                curr = curr.outgoing[char_order].child
                print(curr)
            else:
                # Otherwise, create a new edge, with child node
                new_edge = TrieEdge(label=char, child=TrieNode())
                print(new_edge)
                curr.outgoing[char_order] = new_edge
                curr = new_edge.child

        curr.j = i
        print(curr)

    return root