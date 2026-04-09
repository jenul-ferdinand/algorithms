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


def boyermoore_extendedbcr(pat: str, string: str) -> bool:
    """
    Boyer Moore Extended BCR

    Time complexity (worst): O(mn) where all shifts were one alignment.

    Time complexity (best): O(n/m)

    Space complexity: O(m * |alphabet|) to store the 2D array
    """
    n = len(string)
    m = len(pat)

    rarr = [[-1 for _ in range(128)] for _ in range(m)]
    for k in range(1, m):
        rarr[k] = rarr[k - 1].copy()
        rarr[k][ord(pat[k - 1])] = k - 1
        pass

    x = 0
    while x <= n - m:
        k = m - 1
        while k >= 0 and pat[k] == string[x + k]:
            k -= 1
        if k == -1:
            return True

        bad = string[x + k]
        x += rarr[k][ord(bad)]

    return False
