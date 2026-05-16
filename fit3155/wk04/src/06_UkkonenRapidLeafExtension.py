"""
Ukkonen's Algorithm with Rapid Leaf Extension (notes section 3.7)

Replaces explicit Rule 1 extensions with an implicit globalEnd pointer.
Every leaf edge stores its end as a reference to globalEnd rather than as
a concrete index, so incrementing globalEnd at the start of each phase
implicitly extends every leaf in the tree by the new character.

Combined with the lastj counter, all Rule 1 extensions in a phase are
performed in O(1) and we begin explicit extensions from j = lastj + 1.
"""

from __future__ import annotations
