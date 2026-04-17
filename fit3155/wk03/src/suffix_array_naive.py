def suffix_array_naive(string: str) -> list[int]:
    """
    Naive method to construct a suffix array.

    Time complexity: O(n^2 log n)
    Space complexity: O(n)

    """
    if string[-1] != "$":
        string = string + "$"
        
    n = len(string)

    suffixes = [(string[i:], i) for i in range(n)]
    suffixes.sort()

    return [suffix[1] for suffix in suffixes]
