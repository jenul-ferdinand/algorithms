from fit3155.wk03.src.suffix_array_prefix_doubling import (
    suffix_array_prefix_doubling,
)


def bwt(string):
    """
    Burrows Wheeler Transform

    1. Build the suffix array (SA) of S$.
    2. For each entry SA[i], the BWT character is just S[SA[i] - 1]

    Time complexity: O(n log n)
        This is because we're using prefix doubling to create the suffix array.
        If we instead used Ukkonen's to create the suffix array, this would be
        O(n).

    Space complexity: O(n)
    """
    if string[-1] != "$":
        string = string + "$"

    N = len(string)
    SA = suffix_array_prefix_doubling(string)
    bwt = ""

    for i in range(N):
        bwt += string[SA[i] - 1]

    return bwt
