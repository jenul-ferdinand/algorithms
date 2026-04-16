def suffix_array_naive(S: str) -> list[int]:
    """
    Naive method to construct a suffix array.

    Time complexity: O(n^2 log n)
    Space complexity: O(n)
    
    """
    S = S + "$"
    n = len(S)

    suffixes = []

    for i in range(0, n):
        suffixes.append(S[i:])
    suffixes.sort()

    for i, suffix in enumerate(suffixes):
        sufflen = len(suffix)
        suffixes[i] = n - sufflen

    return suffixes


suffix_array_naive("googol")
