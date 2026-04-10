"""
Write psuedocode for an algorithm that takes two strings S[1..M] and T[1..N] and
returns the length of the longest suffix of S that exactly matches a prefix
of T.

+ What is the worst case time complexity of your algorithm.
"""

from fit3155.wk01.src.zalg import zalg


def get_suffix_prefix_length(suffstring: str, prestring: str) -> int:
    """
    Returns the length of the longets suffix of suffstring that exactly matches
    the prefix of prestring.

    Let S be the length of suffstring
    Let P be the length of prestring
    Let N be the combined length of both S and P

    Time complexity: O(N + N) = O(N)
        We pass the combined string of size N into zalg, which in turn takes N
        iterations to complete the Z array.
        Then we iterate through the Z array to return the correct z value as our
        answer.

    Space complexity: O(N)
        We store an array of size N for the z array.
    """
    string = prestring + "$" + suffstring
    n = len(string)

    z = zalg(string)
    z[0] = 0

    # Return the match starting position z value that reaches the end of the
    # whole string we inputted into zalg.
    return next((z[k] for k in range(n) if k + z[k] == n), 0)


if __name__ == "__main__":
    length = get_suffix_prefix_length(suffstring="aab", prestring="baa")
    correct = 1
    assert length == correct, f"\nExpected {correct},\nGot {length}"

    del length
    del correct

    length = get_suffix_prefix_length(suffstring="aab", prestring="aab")
    correct = 3
    assert length == correct, f"\nExpected {correct},\nGot {length}"

    del length
    del correct

    length = get_suffix_prefix_length(suffstring="aab", prestring="abaa")
    correct = 2
    assert length == correct, f"\nExpected {correct},\nGot {length}"

    del length
    del correct

    length = get_suffix_prefix_length(suffstring="abab", prestring="abab")
    correct = 4
    assert length == correct, f"\nExpected {correct},\nGot {length}"

    del length
    del correct

    length = get_suffix_prefix_length(suffstring="aab", prestring="xyz")
    correct = 0
    assert length == correct, f"\nExpected {correct},\nGot {length}"

    del length
    del correct

    length = get_suffix_prefix_length(suffstring="abcabc", prestring="abcx")
    correct = 3
    assert length == correct, f"\nExpected {correct},\nGot {length}"
