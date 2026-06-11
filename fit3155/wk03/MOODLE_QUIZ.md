# Week 3 Moodle Quiz

Topic: Burrows-Wheeler Transform, LF-mapping, and BWT backward search.

## Questions

1. The Burrows-Wheeler Transform (BWT) of a string is obtained from the first column of the sorted cyclic permutation matrix.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

The BWT is the last column `L` of the sorted cyclic permutation matrix `M`. The first column is `F = sort(L)`.

</details>

---

2. Each column of the sorted cyclic permutation matrix `M` is a permutation of the original string.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

Each row is a cyclic rotation of the same string, so every column contains the same multiset of characters.

</details>

---

3. The suffix array stores all suffixes of a string in lexicographically sorted order.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

More precisely, the suffix array stores the starting positions of the suffixes in lexicographically sorted order.

</details>

---

4. The Burrows-Wheeler Transform is not invertible without storing the original string.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

BWT is invertible. With the terminal character and LF-mapping, we can reconstruct the original string from `L` alone.

</details>

---

5. In LF-mapping, if `L[i]` maps to `F[pos]`, then `L[pos]` precedes `L[i]` in the original string.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

Following the LF link moves one character backward in the original string.

</details>

---

6. The LF-mapping position is computed as `pos = rank(x) + nOccurrences(x, L[1..i])`.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

For `L[i] = x`, LF uses `pos = Rank(x) + nOcc(x, L[1..i))`. The count is exclusive of position `i`.

</details>

---

7. Constructing the BWT from a suffix array can be done in linear time.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

Once the suffix array is available, each BWT character is just the character cyclically before the suffix-array position.

</details>

---

8. Backward search processes the pattern from left to right.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

Backward search processes the pattern from right to left, repeatedly left-extending the matched suffix.

</details>

---

9. If `ep < sp` during BWT-based pattern matching, the pattern does not occur in the text.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

`[sp, ep]` is the current row range. If the range becomes empty, no suffix begins with the pattern processed so far.

</details>

---

10. After preprocessing, BWT-based pattern matching takes `O(m + multiplicity)` time per query.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

Backward search takes `O(m)` to find the matching suffix-array range, then `O(multiplicity)` to output the matching positions.

</details>

---

11. Which column of matrix `M` defines the Burrows-Wheeler Transform?

- [ ] a. Suffix array column
- [ ] b. Middle column
- [ ] c. First column
- [ ] d. Last column

<details>
<summary>Answer</summary>

d. Last column.

The BWT is usually denoted by `L`, the last column of the sorted cyclic permutation matrix.

</details>

---

12. What does the suffix array store?

- [ ] a. All substrings of the text
- [ ] b. Positions of suffixes in sorted order
- [ ] c. Pattern occurrences
- [ ] d. Characters of the BWT

<details>
<summary>Answer</summary>

b. Positions of suffixes in sorted order.

For example, `SA[i]` is the starting index of the suffix with lexicographic rank `i`.

</details>

---

13. Which components are required to compute LF-mapping?

- [ ] a. Rank and nOccurrences
- [ ] b. Suffix array and Z-values
- [ ] c. Prefix function
- [ ] d. Bad character rule

<details>
<summary>Answer</summary>

a. Rank and nOccurrences.

LF uses `Rank(x)` plus the number of earlier occurrences of `x` in `L`.

</details>

---

14. What is the main idea behind efficient BWT inversion?

- [ ] a. Sorting substrings repeatedly
- [ ] b. Using dynamic programming
- [ ] c. Rebuilding the full matrix `M`
- [ ] d. Using LF-mapping between `L` and `F`

<details>
<summary>Answer</summary>

d. Using LF-mapping between `L` and `F`.

The efficient method follows LF links instead of rebuilding and repeatedly sorting the cyclic matrix.

</details>

---

15. In backward search, how are `sp` and `ep` updated?

- [ ] a. Using binary search
- [ ] b. Using rank and nOccurrences
- [ ] c. Using suffix links
- [ ] d. Using prefix sums

<details>
<summary>Answer</summary>

b. Using rank and nOccurrences.

For character `x`, the update is based on `Rank(x)`, occurrences before `sp`, and occurrences up to `ep`.

</details>

---

16. What does the range `[sp, ep]` represent after processing the pattern?

- [ ] a. All rotations of the string
- [ ] b. All characters in the text
- [ ] c. All mismatches
- [ ] d. All suffixes starting with the pattern

<details>
<summary>Answer</summary>

d. All suffixes starting with the pattern.

The corresponding suffix-array entries give the text positions where the pattern occurs.

</details>

---

17. How is multiplicity computed in BWT pattern matching?

- [ ] a. `sp + ep`
- [ ] b. `sp * ep`
- [ ] c. `ep - sp + 1`
- [ ] d. `ep - sp`

<details>
<summary>Answer</summary>

c. `ep - sp + 1`.

If `[sp, ep]` is non-empty, its length is the number of pattern occurrences.

</details>

---

18. What is the preprocessing time complexity to build BWT, assuming optimal suffix array construction?

- [ ] a. `O(mn)`
- [ ] b. `O(n)`
- [ ] c. `O(n log n)`
- [ ] d. `O(n^2)`

<details>
<summary>Answer</summary>

b. `O(n)`.

With an optimal linear-time suffix array, BWT construction is also linear.

</details>

---

19. Why is the naive BWT inversion method inefficient?

- [ ] a. It ignores the suffix array
- [ ] b. It rebuilds the matrix `M` repeatedly
- [ ] c. It uses recursion
- [ ] d. It requires hashing

<details>
<summary>Answer</summary>

b. It rebuilds the matrix `M` repeatedly.

The naive method repeatedly prepends/sorts columns until the whole cyclic matrix is reconstructed.

</details>

---

20. What is a key advantage of BWT-based indexing over classical algorithms?

- [ ] a. Does not use memory
- [ ] b. Works only for small texts
- [ ] c. Faster per-query time for many short patterns
- [ ] d. No preprocessing required

<details>
<summary>Answer</summary>

c. Faster per-query time for many short patterns.

BWT indexing preprocesses the text once, then each query depends mainly on the pattern length and the number of matches.

</details>

## Quick Corrections To Remember

- BWT is the last column `L`, not the first column `F`.
- `F = sort(L)`, and LF maps a character instance in `L` to the same instance in `F`.
- LF uses `nOcc(x, L[1..i))`, excluding position `i`.
- Backward search reads the pattern from right to left.
- After backward search, multiplicity is `ep - sp + 1`; positions come from `SA[sp..ep]`.
