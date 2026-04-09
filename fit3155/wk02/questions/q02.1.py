"""
1. Describe using pseudocode, or otherwise, how to perform the preprocessing
   required for the extended bad character rule. Begin with the 2D array
   approach suggested above. Hint: you should use dynamic programming.
"""


def _printrarr(rarr: list[list[int]], pat: str, txt: str) -> None:
    chars = sorted(set(pat).union(set(txt)))
    print("   ", *[c for c in chars], sep="  ")
    for i, row in enumerate(rarr):
        print(f"{i}: ", *[row[ord(c)] for c in chars], sep="  ")


def preprocess(txt: str, pat: str) -> list[list[int]]:
    m = len(pat)

    # create 2d array |alphabet| * m
    # alphabet = 128 (ASCII chars) <- columns
    # m = pattern length <- rows note:
    # using 'x' as undefined position for this example
    rarr = [["x" for _ in range(128)] for _ in range(m)]

    _printrarr(rarr, pat, txt)

    """ 
    Use DP to allocate the positions

    - rarr[0] stays the same; there are no chars before the first char in the
      pattern
    - rarr[k] we copy rarr[k-1] and we set rarr[k][ord(pat[k-1])] to k - 1
    - repeat, this builds up the 2D array.
    """

    for k in range(1, len(rarr)):
        rarr[k] = rarr[k - 1].copy()
        rarr[k][ord(pat[k - 1])] = k - 1

    print("AFTER")
    _printrarr(rarr, pat, txt)


if __name__ == "__main__":
    preprocess(txt="abbcbbabx", pat="abaxbab")

    pass
