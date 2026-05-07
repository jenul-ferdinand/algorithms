from fit3155.wk04.src.naive_suffix_trie import TrieNode, naive_suffix_trie


def _collect_leaves(root: TrieNode):
    stack = [root]
    leaves: list[TrieNode] = []

    while stack:
        node = stack.pop()
        available_edges = [x for x in node.outgoing if x is not None]
        if len(available_edges) <= 0:
            leaves.append(node)
        else:
            all_children_of_edges = [x.child for x in available_edges]
            stack.extend(all_children_of_edges)

    return sorted(leaves, key=lambda x: x.suffix_start)


def test_ben_langmead_example():
    string = "aba$"
    n = len(string)
    root = naive_suffix_trie(string)
    leaves: list[TrieNode] = _collect_leaves(root)

    # no. leaves = length of string
    assert len(leaves) == n

    # sorted leaves suffix start values = 0,1,2,3 correspondingly
    for i in range(n):
        assert leaves[i].suffix_start == i

    # three outgoing edges from root
    root_available_outgoing_edges = [x for x in root.outgoing if x is not None]
    assert len(root_available_outgoing_edges) == 3
