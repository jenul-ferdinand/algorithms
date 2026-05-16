"""
Ukkonen's Algorithm with Skip-Counting (notes section 3.4)

Builds on suffix links by replacing the character-by-character walk along
the remainder with skip-counting. Once we land at an internal node via a
suffix link, we know the length of the remainder we still need to traverse,
so we can jump down each edge in O(1) by comparing the remaining length
against the edge's length rather than matching characters one at a time.

This brings the per-phase cost down further but does not yet achieve linear
overall time. Rapid leaf extension and the showstopper rule are required
for the final O(n) bound.
"""

from __future__ import annotations
