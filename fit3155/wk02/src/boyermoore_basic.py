"""
Boyer Moore Basic is a simpler implementation of the full Boyer Moore version.

The only thing is that it ONLY uses the bad character rule. It's simpler and
easier to grasp without good suffix rule and galil's optimisation.

- k is the position in the pattern where a mismatch occurs.

- R(x) is the rightmost occurrence of a character x in the pattern P.
  The thing about this here; unlike the real BM algo, it doesn't changes.

- On each mismatch do max(k - R(x), 1) to find out how much to the alignment
  shift by.
"""

from fit3155.wk02.src.models import BMOutput


def boyermoore_basic(pat: str, txt: str) -> BMOutput:
    """
    Boyer Moore Basic

    Let m be the length of the pattern Let n be the length of the string

    Time complexity (worst): O(mn) where all shifts were one alignment.

    Time complexity (best): O(n/m) when each alignment does only one comparison,
    then shifts by m positions every time.

    Space complexity: O(m + |alphabet|)=O(m) to store the dictionary to get the
    pattern occurrence positions.
    """
    output: BMOutput = BMOutput()

    n = len(txt)
    m = len(pat)

    # Preprocess basic bad character array
    R = {pat[i]: i for i in range(m)}

    j = 0
    while j <= n - m:
        # Right to left scanning
        k = m - 1
        while k >= 0:
            output.comparisons += 1
            if pat[k] != txt[j + k]:
                break
            k -= 1

        j_before = j
        if k == -1:
            # Full match
            output.matches += 1
            output.match_positions.append(j)
            j += 1
        else:
            # Bad character rule shift
            j += max(k - R.get(txt[j + k], -1), 1)

        assert j > j_before, "Must shift by at least one"
        output.total_shifts += 1

    return output
