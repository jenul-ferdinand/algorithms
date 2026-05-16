"""
Ukkonen's Algorithm with the Showstopper Rule (notes sections 3.6 and 3.8)

Adds the extension termination criterion: once a Rule 3 extension occurs in
phase i, every subsequent extension in the phase would also be a Rule 3, so
we can skip them entirely and move on to phase i + 1. Combined with the
small bookkeeping correction from section 3.8 (active node and remainder
updates that must still occur on a Rule 3), this yields the final O(n)
construction time.

At this point the algorithm is the complete Ukkonen's algorithm.
"""

from __future__ import annotations
