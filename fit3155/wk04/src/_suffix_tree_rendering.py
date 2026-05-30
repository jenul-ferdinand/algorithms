"""
Helper functions to visualise suffix trees in the terminal using ASCII.

Duck-typed against any tree with these fields:
    Node.outgoing      : list[Edge | None]
    Node.suffix_start  : int | None              (None on internal nodes)
    Edge.start         : int
    Edge.end           : int | mutable one-item end reference
    Edge.child         : Node
"""

from __future__ import annotations

from typing import Any

from fit3155.common.constants import ascii_order
from fit3155.wk04.src._edge_rendering import EndResolver, resolve_edge_end


def render_suffix_tree(
    name: str,
    S: str,
    root: Any,
    resolve_end: EndResolver = resolve_edge_end,
) -> str:
    """
    Return a multi-line ASCII visualisation of the suffix tree rooted at
    `root` over string `S`, prefixed with a header derived from `name`.

    The tree is followed by a per-suffix summary listing each j's fate
    (leaf, implicit at internal node, or implicit mid-edge with a visual
    cut shown as prefix|suffix).
    """
    n = len(S)
    header = f"{name}({S!r})  n={n}"
    if n == 0:
        return f"{header}\n(empty)"

    ep_node, ep_edge, fate = _locate_suffix_endpoints(S, root, resolve_end)

    lines = [header, "(root)"]
    children = [e for e in root.outgoing if e is not None]
    for idx, edge in enumerate(children):
        _render_subtree(
            S,
            edge,
            lines,
            "",
            idx == len(children) - 1,
            ep_node,
            ep_edge,
            resolve_end,
        )

    lines.append("")
    lines.append("suffixes:")
    width = max(len(repr(S[j:])) for j in range(n))
    for j in range(n):
        suffix = repr(S[j:])
        kind = fate[j]
        if kind[0] == "leaf":
            desc = "leaf"
        elif kind[0] == "node":
            desc = "implicit at internal node"
        elif kind[0] == "mid":
            _, edge, depth = kind
            end = resolve_end(edge)
            label = S[edge.start : end + 1]
            cut = f"{label[:depth]}|{label[depth:]}"
            desc = f"implicit suffix, mid edge S[{edge.start}..{end}]: {cut}"
        else:
            desc = "unreachable (tree malformed)"
        lines.append(f"  j={j}  {suffix:<{width}}  {desc}")

    return "\n".join(lines)


def _locate_suffix_endpoints(S: str, root: Any, resolve_end: EndResolver):
    """
    For each suffix S[j..n-1], walk from `root` and record where it
    terminates. Three fates:

        ("leaf", node)         - explicit leaf with suffix_start == j
        ("node", node)         - ends exactly at an internal node
        ("mid", edge, depth)   - ends `depth` chars into `edge`'s label
    """
    n = len(S)
    ep_node: dict[int, set[int]] = {}
    ep_edge: dict[int, dict[int, set[int]]] = {}
    fate: dict[int, tuple] = {}

    for j in range(n):
        node = root
        k = j
        while True:
            if k == n:
                if node.suffix_start == j:
                    fate[j] = ("leaf", node)
                else:
                    fate[j] = ("node", node)
                    ep_node.setdefault(id(node), set()).add(j)
                break
            edge = node.outgoing[ascii_order(S[k])]
            if edge is None:
                fate[j] = ("missing",)
                break
            label_len = resolve_end(edge) - edge.start + 1
            remaining = n - k
            if remaining < label_len:
                fate[j] = ("mid", edge, remaining)
                ep_edge.setdefault(id(edge), {}).setdefault(
                    remaining, set()
                ).add(j)
                break
            k += label_len
            node = edge.child

    return ep_node, ep_edge, fate


def _render_subtree(
    S: str,
    edge: Any,
    lines: list[str],
    prefix: str,
    is_last: bool,
    ep_node: dict[int, set[int]],
    ep_edge: dict[int, dict[int, set[int]]],
    resolve_end: EndResolver,
) -> None:
    end = resolve_end(edge)
    label = S[edge.start : end + 1]
    connector = "└── " if is_last else "├── "

    child = edge.child
    leaf_marker = (
        f"  (leaf suffix j={child.suffix_start})"
        if child.suffix_start is not None
        else ""
    )
    lines.append(
        f"{prefix}{connector}{label} S[{edge.start}..{end}]{leaf_marker}"
    )

    cont = prefix + ("    " if is_last else "│   ")

    # Mid-edge implicit endpoints: shallowest cut first
    if id(edge) in ep_edge:
        for depth in sorted(ep_edge[id(edge)]):
            for j in sorted(ep_edge[id(edge)][depth]):
                cut = f"{label[:depth]}|{label[depth:]}"
                lines.append(f"{cont}  ↳ implicit suffix j={j} ends at {cut}")

    # At-node implicit endpoints: at edge.child
    if id(child) in ep_node:
        for j in sorted(ep_node[id(child)]):
            lines.append(f"{cont}  ↳ implicit suffix j={j} ends here")

    next_children = [e for e in child.outgoing if e is not None]
    for idx, ce in enumerate(next_children):
        _render_subtree(
            S,
            ce,
            lines,
            cont,
            idx == len(next_children) - 1,
            ep_node,
            ep_edge,
            resolve_end,
        )
