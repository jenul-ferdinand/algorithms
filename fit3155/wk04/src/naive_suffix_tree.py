from fit3155.common.constants import ALPHABET_SIZE, TERMINAL_CHAR, ascii_order


class TreeNode:
    def __init__(self, suffix_start: int = None):
        self.outgoing: list[TreeEdge] = [None for _ in range(ALPHABET_SIZE)]
        self.suffix_start = suffix_start

    def __repr__(self):
        outgoing = []
        for edge in self.outgoing:
            if edge is not None:
                outgoing.append(edge)
        return f"Node(suffix_start={self.suffix_start}, outgoing_edges={len(outgoing)})"


class TreeEdge:
    def __init__(self, start: int, end: int, child: TreeNode):
        self.start = start
        self.end = end
        self.child = child

    def __repr__(self):
        return f"Edge(start={self.start}, end={self.end}, child={self.child})"


def naive_suffix_tree(string: str) -> TreeNode:
    if string[-1] != TERMINAL_CHAR:
        string = string + TERMINAL_CHAR

    n = len(string)
    root = TreeNode()
    for i in range(n):
        curr = root
        pos = i  # where we are in the suffix
        while pos < n:
            edge = curr.outgoing[ascii_order(string[pos])]

            if edge is None:
                # First char of label doesn't match first char of suffix
                # so we create a new leaf node with long edge containing the
                # whole suffix.
                leaf_node = TreeNode(suffix_start=i)
                leaf_edge = TreeEdge(start=pos, end=n - 1, child=leaf_node)
                curr.outgoing[ascii_order(string[pos])] = leaf_edge
                break

            k = 0
            while (
                edge.start + k <= edge.end
                and string[pos + k] == string[edge.start + k]
            ):
                k += 1

            # Mismatched when comparing edge label with current suffix
            if edge.start + k <= edge.end:
                # Create a split on mismatch
                mismatch_pos = edge.start + k
                original_child = edge.child
                original_end = edge.end

                new_internal_node = TreeNode()

                # the original edge becomes a shortened trunk
                edge.child = new_internal_node
                edge.end = mismatch_pos - 1

                # add remaining edge from internal node to original node
                remainder_edge = TreeEdge(
                    start=mismatch_pos,
                    end=original_end,
                    child=original_child,
                )
                new_internal_node.outgoing[
                    ascii_order(string[mismatch_pos])
                ] = remainder_edge

                # create another node for the suffix edge
                new_start = pos + k
                new_leaf = TreeNode(suffix_start=i)
                new_edge = TreeEdge(
                    start=new_start,
                    end=n - 1,
                    child=new_leaf,
                )
                new_internal_node.outgoing[ascii_order(string[new_start])] = (
                    new_edge
                )
                break

            # Full matched the whole edge label
            # update the pos based on how much we matched
            # and update curr to child of current edge
            if edge.start + k > edge.end:
                edge_length = edge.end - edge.start + 1
                pos += edge_length
                curr = edge.child
                continue

    return root


if __name__ == "__main__":
    string = "aabaa$"
    root = naive_suffix_tree(string)
    print(root)
