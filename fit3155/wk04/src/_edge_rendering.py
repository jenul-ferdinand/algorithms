"""
Helpers for rendering suffix-tree edges in debug output.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

EndResolver = Callable[[Any], int]


def resolve_edge_end(edge: Any) -> int:
    end = edge.end
    if isinstance(end, list):
        return end[0]
    return end


def render_node_ref(node: Any | None) -> str:
    if node is None:
        return "None"

    suffix_start = getattr(node, "suffix_start", None)
    kind = f"leaf j={suffix_start}" if suffix_start is not None else "internal"
    return f"Node@{id(node):x}({kind})"


def render_edge(edge: Any, resolve_end: EndResolver = resolve_edge_end) -> str:
    end = resolve_end(edge)
    return "\n".join(
        [
            "Edge(",
            f"  label=S[{edge.start}..{end}]",
            f"  child={render_node_ref(edge.child)}",
            ")",
        ]
    )
