from fit3155.common.constants import ASCII_LOWER
from fit3155.wk03.src.bwt import bwt, process_occ, process_rank
from fit3155.wk03.src.suffix_array_prefix_doubling import (
    suffix_array_prefix_doubling,
)


def bwt_search(pat: str, txt: str):
    """
    Pattern matcher with BWT backward search

    Let n = length of txt 
    Let m = length of pat 
    Let sigma = fixed alphabet size of 90

    Time complexity: O(n log n + n sigma + m) = O(n log n + m)

    Space complexity: O(n sigma) = O(n)
    """
    m = len(pat)

    L = bwt(txt) # O(n log n)
    SA = suffix_array_prefix_doubling(txt) # O(n log n)
    rank = process_rank(L) # O(n + sigma)
    occ = process_occ(L) # O(n sigma)

    sp = 0
    ep = len(SA) - 1

    for x in range(m - 1, -1, -1):
        idx = ord(pat[x]) - ASCII_LOWER
        sp = rank[idx] + occ[idx][sp]
        ep = rank[idx] + occ[idx][ep + 1] - 1

        if sp > ep:
            return []

    return SA[sp : ep + 1]


print(bwt_search("a", "aaaaaaahhfdsfdsfbdsbfaaaaadsffdsfsd"))
