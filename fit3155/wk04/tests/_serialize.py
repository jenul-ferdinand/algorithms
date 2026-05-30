def _serialize(node, S, resolve_end=None):
    """Serialize a suffix tree into a comparable tuple structure.

    `resolve_end(edge) -> int` returns the actual end index for an edge.
    For implementations where `edge.end` is always a concrete int (Naive,
    SuffixLinks, SkipCount, ShowStopper), omit this argument and the
    default uses `edge.end` directly. For RapidLeafExtension, where leaf
    edges store a sentinel and the real end is `tree.global_end`, pass
    the tree's `_end` method (or an equivalent callable).
    """
    if resolve_end is None:

        def resolve_end(e):
            return e.end

    children = tuple(
        (S[e.start : resolve_end(e) + 1], _serialize(e.child, S, resolve_end))
        for e in node.outgoing
        if e is not None
    )
    return (node.suffix_start, children)
