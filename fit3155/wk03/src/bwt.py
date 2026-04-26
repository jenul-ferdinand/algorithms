from fit3155.common.constants import ALPHABET_SIZE, ASCII_LOWER, TERMINAL_CHAR
from fit3155.wk03.src.suffix_array_prefix_doubling import (
    suffix_array_prefix_doubling,
)


def bwt(txt):
    """
    Burrows Wheeler Transform (BWT)

    A re-arrangement of the string that groups similar characters together while
    preserving enough information to recover the original string.

    Time complexity: O(n log n)
        This is because we're using prefix doubling to create the suffix array.
        If we instead used Ukkonen's to create the suffix array, this would be
        O(n).

    Space complexity: O(n)
    """
    if txt[-1] != TERMINAL_CHAR:
        txt = txt + TERMINAL_CHAR

    n = len(txt)
    # Build the suffix array of the txt with terminal char
    SA = suffix_array_prefix_doubling(txt)
    L = ""
    
    for i in range(n):
        # Form the BWT by taking the char before each suffix
        # In python, SA[i]=0 will wrap to terminal via txt[-1]
        L += txt[SA[i] - 1]

    return L


def process_rank(L: str):
    """
    rank[x] = the first position where x appears in the sorted first column F
    """
    # Count how many times each char appears in L
    freq = [0] * ALPHABET_SIZE
    for c in L:
        freq[ord(c) - ASCII_LOWER] += 1

    rank = [-1] * ALPHABET_SIZE
    pos = 0
    for i in range(ALPHABET_SIZE):
        # Scanning the chars in sorted order
        # The cumulative count gives each char's start pos in F 
        if freq[i] > 0:
            rank[i] = pos
            pos += freq[i]

    return rank


def process_occ(L: str):
    """
    occ[x][i] = the number of times char x appears before index i in L
    """
    n = len(L)
    chars = list(set(L))

    # one row per unique char and one column per position
    # ALPHABET_SIZE x n + 1
    # We store n + 1 cols because we store prefix counts including empty prefix
    occ = [[0 for _ in range(n + 1)] for _ in range(ALPHABET_SIZE)]

    for i in range(n):
        # Copy previous column, then increment the row for L[i]
        for c in chars:
            occ[ord(c) - ASCII_LOWER][i + 1] = occ[ord(c) - ASCII_LOWER][i]

        occ[ord(L[i]) - ASCII_LOWER][i + 1] += 1

    return occ


def process_LF(L, rank, occ):
    """
    LF[i] = the row in F that corresponds to row i in L
    """
    n = len(L)
    LF = [-1] * n

    for i in range(n):
        # Find where L[i] appears in F
        idx = ord(L[i]) - 37
        LF[i] = rank[idx] + occ[idx][i]

    return LF


def inverse_bwt(L):
    """
    BWT Invertor

    Reconstructs the original string from the BWT string L
    """
    n = len(L)
    res = [-1] * n

    # Preprocessing
    rank = process_rank(L)
    occ = process_occ(L)
    LF = process_LF(L, rank, occ)

    # Find i in L where L[i] = "%"
    i = 0
    while i < n:
        if L[i] == TERMINAL_CHAR:
            break
        i += 1

    # Using LF mapping to build the original string
    res[n - 1] = TERMINAL_CHAR
    for k in range(n - 2, -1, -1):
        i = LF[i]
        res[k] = L[i]

    return "".join(res)
