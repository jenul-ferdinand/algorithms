"""
Ukkonen's Algorithm with Suffix Links (notes section 3.3)

Adds suffix links to the naive implicit suffix tree construction. Each
internal node u (whose path from root spells xa) gets a suffix_link pointer
to the internal node whose path spells a. This lets us jump between
consecutive extensions within a phase without restarting the walk from the
root.

The walk along the remainder below the active node is still character by
character at this stage. Skip-counting comes in the next file.
""" 

from __future__ import annotations
