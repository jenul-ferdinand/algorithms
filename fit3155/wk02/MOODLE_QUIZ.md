# Week 2 Moodle Quiz

Topic: Boyer-Moore pattern matching.

## Questions

1. The Boyer-Moore algorithm compares characters in the pattern from right to left during each alignment.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

For an alignment of `pat[1..m]` against the text, Boyer-Moore starts at `pat[m]` and scans leftward.

</details>

---

2. Right-to-left scanning alone guarantees faster performance than the naive algorithm.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

Scanning direction alone does not save work. The speed-up comes from using the information gained by the scan to make safe shifts.

</details>

---

3. In the bad character rule, `R(x)` stores the position of the rightmost occurrence of character `x` in the pattern.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

If `x` is not in the pattern, the unit's 1-indexed convention sets `R(x) = 0`.

</details>

---

4. If the mismatched character does not appear in the pattern, the pattern can be shifted past that character entirely.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

If `R(x) = 0`, no pattern character can match that text character, so shifting past it is safe.

</details>

---

5. If the rightmost occurrence of the mismatched character lies to the right of the mismatch position, the bad character rule shifts the pattern by one position.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

For the basic bad character rule, if `R(x) > k`, then `k - R(x)` is negative, so the rule falls back to a safe shift of 1.

</details>

---

6. The extended bad character rule uses `R_k(x)` to store occurrences of characters to the left of position `k` in the pattern.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

`R_k(x)` stores the rightmost occurrence of `x` strictly to the left of position `k`, or `0` if no such occurrence exists.

</details>

---

7. The good suffix rule shifts the pattern based on the portion of the pattern that matched before a mismatch.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

Because Boyer-Moore scans right to left, the matched region before a mismatch is a suffix of the pattern.

</details>

---

8. The good suffix rule alone guarantees linear time complexity for pattern matching.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

Good suffix shifts help, but Galil's optimisation is what gives Boyer-Moore its worst-case `O(m + n)` guarantee in this unit.

</details>

---

9. Matched prefix values represent the longest prefix of the pattern that matches a suffix of a matched region.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

When `gs(k + 1) = 0`, the matched prefix value tells us how much of the pattern prefix can be aligned with a suffix of the matched text region.

</details>

---

10. With Galil's optimisation, Boyer-Moore has worst-case complexity `O(m + n)`.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

Galil's optimisation avoids re-comparing regions already known to match.

</details>

---

11. Which scanning direction is used by the Boyer-Moore algorithm?

- [ ] a. Both directions simultaneously
- [ ] b. Random order
- [ ] c. Right to left
- [ ] d. Left to right

<details>
<summary>Answer</summary>

c. Right to left.

Boyer-Moore compares from the end of the pattern back toward the start.

</details>

---

12. In practical applications, the average running time of Boyer-Moore is often:

- [ ] a. Exponential
- [ ] b. Sublinear in the text length
- [ ] c. Constant
- [ ] d. Quadratic

<details>
<summary>Answer</summary>

b. Sublinear in the text length.

In many real text-search settings, Boyer-Moore skips enough text that it does not inspect every character.

</details>

---

13. What does `R(x)` represent in the bad character rule?

- [ ] a. The first occurrence of `x` in the text
- [ ] b. The rightmost occurrence of `x` in the pattern
- [ ] c. The number of times `x` appears in the pattern
- [ ] d. The number of mismatches encountered

<details>
<summary>Answer</summary>

b. The rightmost occurrence of `x` in the pattern.

This is what lets the bad character rule align that pattern occurrence with the mismatched text character.

</details>

---

14. If a mismatch occurs at position `k` and `R(x) < k`, how many positions does the basic bad character rule shift?

- [ ] a. `R(x) - k`
- [ ] b. `m - R(x)`
- [ ] c. `k + R(x)`
- [ ] d. `k - R(x)`

<details>
<summary>Answer</summary>

d. `k - R(x)`.

This aligns the rightmost occurrence of the bad character in the pattern with the bad character in the text.

</details>

---

15. What improvement does the extended bad character rule provide?

- [ ] a. It removes preprocessing
- [ ] b. It uses the closest occurrence of the bad character to the left of the mismatch
- [ ] c. It compares characters from left to right
- [ ] d. It ignores mismatches

<details>
<summary>Answer</summary>

b. It uses the closest occurrence of the bad character to the left of the mismatch.

That is the purpose of `R_k(x)`: avoid falling back to a one-position shift when `R(x)` lies to the right of `k`.

</details>

---

16. The good suffix rule shifts the pattern using information about:

- [ ] a. The alphabet size
- [ ] b. The first character in the pattern
- [ ] c. The mismatched character
- [ ] d. The matched suffix

<details>
<summary>Answer</summary>

d. The matched suffix.

After a right-to-left scan mismatches at `k`, the region `pat[k + 1..m]` has already matched the text.

</details>

---

17. If `gs(k + 1) > 0` after a mismatch, the shift is:

- [ ] a. `m - gs(k + 1)`
- [ ] b. `gs(k + 1) - m`
- [ ] c. `k + gs(k + 1)`
- [ ] d. `k - gs(k + 1)`

<details>
<summary>Answer</summary>

a. `m - gs(k + 1)`.

`gs(k + 1)` stores the right endpoint of the rightmost usable copy of the matched suffix.

</details>

---

18. If `gs(k + 1) = 0`, which value is used to determine the shift?

- [ ] a. Alphabet size
- [ ] b. Matched prefix
- [ ] c. Z value
- [ ] d. `R(x)`

<details>
<summary>Answer</summary>

b. Matched prefix.

When no internal good-suffix copy is usable, we align the longest prefix that matches a suffix of the matched region.

</details>

---

19. Boyer-Moore typically runs faster than naive matching because:

- [ ] a. It processes characters randomly
- [ ] b. It ignores mismatches
- [ ] c. It always checks every character
- [ ] d. It skips portions of the text using shift rules

<details>
<summary>Answer</summary>

d. It skips portions of the text using shift rules.

Both bad character and good suffix shifts are designed to move over alignments that cannot produce a match.

</details>

---

20. Which two shift rules are combined in Boyer-Moore?

- [ ] a. Bad character and good suffix rules
- [ ] b. Prefix and suffix rules
- [ ] c. Left and right scanning rules
- [ ] d. Naive and Z rules

<details>
<summary>Answer</summary>

a. Bad character and good suffix rules.

Boyer-Moore computes both safe shift amounts and shifts by the larger one.

</details>

## Quick Corrections To Remember

- Right-to-left scanning enables Boyer-Moore's shift rules, but does not help by itself.
- Basic bad character: `shift = max(k - R(x), 1)`.
- Extended bad character: use `R_k(x)`, the closest `x` strictly left of `k`, so `shift = k - R_k(x)`.
- Good suffix uses the already-matched suffix; matched prefix is the fallback when `gs(k + 1) = 0`.
- Galil's optimisation is what stops Boyer-Moore from re-comparing regions already known to match.
