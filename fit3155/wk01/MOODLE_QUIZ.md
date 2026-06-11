# Week 1 Moodle Quiz

Topic: naive exact pattern matching and Gusfield's Z-algorithm.

Attempt summary: 13/15.

## Questions

1. Let `T` be a text of length `n` and `P` a pattern of length `m`. The naive pattern matching algorithm requires `m` comparisons for each alignment with the text, in the worst case.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

In the worst case, each alignment compares every character of the pattern against the corresponding text characters.

</details>

---

2. Let `T` be a text of length `n` and `P` a pattern of length `m`. The worst-case time complexity of the naive algorithm is `O(n + m)`.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

There are `n - m + 1` valid alignments, and each can cost `m` comparisons, so the worst case is `O(mn)`.

</details>

---

3. The naive algorithm does the fewest number of comparisons when all characters in the pattern and text are the same.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

That is the maximum-comparison situation: every alignment runs for the full pattern length.

</details>

---

4. Let `S` be a string of length `n`. Then `Z[i]` is defined for `1 <= i <= n`.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

In this unit's 1-indexed convention, Z-values are defined for `2 <= i <= n`. `Z[1]` is left undefined/ignored because it is trivial.

</details>

---

5. Let `S` be a string of length `n` and let `2 <= k <= n`. If `Z[k] > 0`, then `S[k..k + Z[k] - 1] = S[1..Z[k]]`.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

This is exactly what `Z[k]` means: the substring starting at `k` matches the prefix for `Z[k]` characters.

</details>

---

6. Let `S` be a string of length `n` and let `r_k` be the value of `r` at iteration `k` of the Z-algorithm when run on `S`. Then `(r_1, r_2, ..., r_n)` is non-decreasing.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

`r` is the rightmost endpoint seen so far. It can stay still or move right, but never moves left.

</details>

---

7. Case 2a of the Z-algorithm requires explicit comparisons.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

In case 2a, `Z[k - l + 1] < r - k + 1`, so `Z[k]` can be copied from the mirrored prefix position.

</details>

---

8. Let `S` be a string of length `n`. Suppose we are in iteration `k` of the Z-algorithm when run on `S` and assume `k > r_{k-1}`. As we are in case 1, we must compute `Z[k]` using explicit comparisons.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

If `k` lies outside the current Z-box, no previous box tells us what matches at `k`, so we compare against the prefix directly.

</details>

---

9. Let `P` be a pattern of length `m` and `T` be a text of length `n`. When using the Z-algorithm for pattern matching, the pattern occurs at position `i` if and only if `Z[i] = m`.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True, using the combined-string indexing from the quiz.

For the usual construction `P + $ + T`, a Z-value of `m` in the text region means the pattern matched completely. In text coordinates, the occurrence position is offset by `m + 1`.

</details>

---

10. Z-algorithm preprocessing takes `O(n^2)` time in the worst case.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

Gusfield's Z-algorithm computes all Z-values in `O(n)` time.

</details>

---

11. The worst-case complexity of the naive algorithm occurs when:

- [ ] a. The pattern never appears in the text.
- [ ] b. The first character always mismatches.
- [ ] c. Every alignment of the pattern with the text results in nearly a full match.
- [ ] d. The pattern is longer than the text.

<details>
<summary>Answer</summary>

c. Every alignment of the pattern with the text results in nearly a full match.

The cost is bad when the algorithm almost finishes checking the pattern before discovering whether the alignment matches.

</details>

---

12. Why is the total number of matches `O(n)` in the Z-algorithm?

- [ ] a. Because each iteration makes at most one comparison.
- [ ] b. Because `r` only increases and is bounded by `n`.
- [ ] c. Because mismatches are constant time.
- [ ] d. Because `Z[k] <= 1`.

<details>
<summary>Answer</summary>

b. Because `r` only increases and is bounded by `n`.

Each explicit successful comparison extends the right boundary `r`. Since `r <= n`, this can happen only `O(n)` times.

</details>

---

13. Let `S` be a string and `k` be the current iteration of the Z-algorithm. If we are in case 2a, when `Z[k - l + 1] < r - k + 1`, then we:

- [ ] a. Do not know anything about position `k` and must compute `Z[k]` through explicit comparison.
- [ ] b. Copy `Z[k]` from a previously computed Z-value.
- [ ] c. Set `Z[k]` to the distance from `k` to the current `r` value.
- [ ] d. Return false.

<details>
<summary>Answer</summary>

b. Copy `Z[k]` from a previously computed Z-value.

Specifically, set `Z[k] = Z[k - l + 1]`; the old mismatch inside the prefix is mirrored inside the current Z-box.

</details>

---

14. Let `S` be a string. The Z-value at position `i`, `Z[i]`, is defined as:

- [ ] a. The number of occurrences of the character `S[i]` in `S`.
- [ ] b. The length of the longest substring of `S` starting at `i` that matches a prefix of `S`.
- [ ] c. The number of occurrences of a pattern `T` in `S`.
- [ ] d. The rightmost boundary of a Z-box starting before or at `i`.

<details>
<summary>Answer</summary>

b. The length of the longest substring of `S` starting at `i` that matches a prefix of `S`.

That is the core definition of a Z-value.

</details>

---

15. When using the Z-algorithm for pattern matching, we combine the pattern `P` and the text `T` to make the string `S = P + "$" + T`. Why do we include the `"$"` symbol?

- [ ] a. To reduce the space complexity of the search.
- [ ] b. To speed up the number of comparisons.
- [ ] c. To ensure that the pattern and text are separated by a character not in the alphabet.
- [ ] d. To make indexing easier.

<details>
<summary>Answer</summary>

c. To ensure that the pattern and text are separated by a character not in the alphabet.

The separator prevents a prefix match from accidentally flowing across the boundary between the pattern and text.

</details>

## Quick Corrections To Remember

- Naive matching is `O(mn)` in the worst case, not `O(n + m)`.
- In this unit, `Z[1]` is not used; the useful Z-values are `Z[2]` through `Z[n]`.
- Case 2a copies a known Z-value. Case 1 and case 2b are where explicit comparisons happen.
- Z is linear because `r` only moves right and is bounded by the end of the string.
