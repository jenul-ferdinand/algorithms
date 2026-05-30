"""
Helpers for rendering suffix-tree nodes in debug output.
"""

from __future__ import annotations

from typing import Any

from fit3155.common.constants import ALPHABET_OFFSET
from fit3155.wk04.src._edge_rendering import (
    EndResolver,
    render_edge,
    render_node_ref,
    resolve_edge_end,
)


def indent(text: str, spaces: int) -> str:
    prefix = " " * spaces
    return "\n".join(f"{prefix}{line}" for line in text.splitlines())


def render_node(node: Any, resolve_end: EndResolver = resolve_edge_end) -> str:
    suffix_link = getattr(node, "suffix_link", None)
    lines = [
        f"Node@{id(node):x}(",
        f"  suffix_start={node.suffix_start}",
        f"  has_suffix_link={suffix_link is not None}",
        f"  suffix_link_target={render_node_ref(suffix_link)}",
    ]

    outgoing = [
        (chr(i + ALPHABET_OFFSET), edge)
        for i, edge in enumerate(node.outgoing)
        if edge is not None
    ]
    if outgoing:
        lines.append("  outgoing:")
        for c, edge in outgoing:
            lines.append(f"    {c!r} ->")
            lines.append(indent(render_edge(edge, resolve_end), 6))
    else:
        lines.append("  outgoing: none")

    lines.append(")")
    return "\n".join(lines)
