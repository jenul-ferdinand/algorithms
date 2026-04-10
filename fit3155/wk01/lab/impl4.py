"""
Implement the Z-algorithm based exact pattern matching discussed in lectures.
Your code should accept a text and a pattern as inputs and return all positions
in the text where the pattern matches exactly.
"""

from fit3155.wk01.src.zalg import zalg


def zalgmatcher(pattern: str, string: str) -> list[bool]:
    """
    Matches some pattern with a string giving an array of size P where True
    values indicate a full pattern match.

    P is the length of the pattern.
    """
    patstring = pattern + "$" + string
    seplen = len(pattern) + 1
    patlen = len(pattern)
    n = len(patstring)

    z = zalg(patstring)
    return [z[i] == patlen for i in range(seplen, n)]


if __name__ == "__main__":
    matcharr = zalgmatcher("ab", "ababab")
    answer = [True, False, True, False, True, False]
    assert matcharr == answer, f"\nExpected: {answer}\nGot: {matcharr}"
    print(answer)
