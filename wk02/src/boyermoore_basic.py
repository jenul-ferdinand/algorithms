"""
Boyer Moore Basic is a simpler implementation of the full Boyer Moore version.

The only thing is that it ONLY uses the bad character rule. It's simpler and
easier to grasp without good suffix rule and galil's optimisation.

- k is the position in the pattern where a mismatch occurs.

- R(x) is the rightmost occurrence of a character x in the pattern P.
    The thing about this here; unlike the real BM algo, it doesn't change.

- On each mismatch do max(k - R(x), 1) to find out how much to the alignment
  shift by.
"""


def boyermoore_basic(pat: str, txt: str) -> bool:
    """
    Boyer Moore Basic

    Let m be the length of the pattern Let n be the length of the string

    Time complexity (worst): O(mn) where all shifts were one alignment.

    Time complexity (best): O(n/m) when the last character of the pattern
    doesn't appear in the string.

    Space complexity: O(m + |alphabet|)=O(m) to store the dictionary to get the
    pattern occurrence positions.
    """
    n = len(txt)
    m = len(pat)

    rdict = dict([(pat[i], i) for i in range(m)])

    def r(char):
        return rdict.get(char, 0)

    x = 0
    while x <= n - m:
        k = m - 1
        while k >= 0 and pat[k] == txt[x + k]:
            k -= 1

        if k == -1:
            return True

        x += max(k - r(txt[x + k]), 1)

    return False


if __name__ == "__main__":
    txt = "sphoorythy"
    pat = "thy"
    res = boyermoore_basic(pat, txt)
    tru = True
    assert res == tru, f"Expected {tru}, got {res}"

    txt = "xyzsomething"
    pat = "abc"
    res = boyermoore_basic(pat, txt)
    tru = False
    assert res == tru, f"Expected {tru}, got {res}"

    txt = "xxxxxxxxxabc"
    pat = "abc"
    res = boyermoore_basic(pat, txt)
    tru = True
    assert res == tru, f"Expected {tru}, got {res}"
