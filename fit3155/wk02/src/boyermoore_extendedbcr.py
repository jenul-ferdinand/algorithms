"""
Boyer Moore using the Extended Bad Character Rule

The search phase remains the same, what's different here is the preprocessing.
Instead of a one dimensional array storing the position of each character in the
pattern which stays fixed.

We create a 2D array that stores R_k(x) which stores the position of the
character x in the pattern before k for all k.

This allows us to shift a little bit more purposely unlike with basic BCR where
if we get R(x) > k we always fall back to shifting by one because the rightmost
occurrence of the bad character is to the right of the mismatch point.

With this, we guarantee a meaningful shift everytime because it only considers
occurrences to the left of k. The shift k - R_k(x) directly aligns that
occurrence with the bad character in the text, which is also the best possible
alignment based on the bad character alone.

- Basic BCR: "Where is this character in the pattern?"
- Extended BCR: "Where is this character in the part of the pattern I haven't
  compared yet?"
"""

from fit3155.wk02.src.models import BMOutput


def boyermoore_extendedbcr(pat: str, txt: str) -> BMOutput:
    """
    Boyer Moore Extended BCR

    Time complexity (worst): O(mn) where all shifts were one alignment.

    Time complexity (best): O(n/m)

    Space complexity: O(m * |alphabet|) to store the 2D array
    """
    output = BMOutput()

    n = len(txt)
    m = len(pat)

    # Preprocess extended bad character table
    rarr = [[-1 for _ in range(128)] for _ in range(m)]
    for i in range(1, m):
        rarr[i] = rarr[i - 1].copy()
        rarr[i][ord(pat[i - 1])] = i - 1

    x = 0
    while x <= n - m:
        # Right to left scanning
        j = m - 1
        while j >= 0: 
            output.compares += 1
            if pat[j] != txt[x + j]:
                break
            
            j -= 1

        x_before = x
        if j == -1:
            # Full match
            output.matches += 1
            output.match_positions.append(x)
            x += 1
        else: 
            # Extended bad character rule shift
            bad = txt[x + j]
            x += j - rarr[j][ord(bad)]

        assert x > x_before, "Must shift forwards atleast one"
        output.shifts += 1

    return output
