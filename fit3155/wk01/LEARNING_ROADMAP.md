# Week 1: Gusfield's Z-algorithm - Learning Roadmap

Source material: `notes01.pdf` (16 pages), `seminar01.pdf`, `lab01.pdf`.  
Lab exercises drawn from `lab01.pdf` are woven in as checkpoints under each topic.

Legend: `[ ]` concept / theorem / proof to learn. `[ ] Lab Qx`: question from `lab01.pdf`. `[ ] Lab notes-Qx`: question embedded in `notes01.pdf`. `[ ] Impl`: implementation exercise. Goals describe what "done" looks like.

The order is the order to learn in. Each section assumes everything above it.

---

## 1. The exact pattern matching problem

- [x] Definition 1: exact pattern matching
  - Given `txt[1..n]` and `pat[1..m]`, find every starting position in `txt` where `pat` occurs.
  - Goal: state the input/output cleanly and give one or two real-world consumers (grep, find-in-file, search engines).
- [x] Why it gets hard at scale
  - Try m = 1000, n = 10,000,000. Anything quadratic is unusable.
  - Goal: justify in one sentence why O(n + m) is the bar to clear.

---

## 2. Naive pattern matching

- [x] The naive algorithm
  - Slide `pat` left-to-right over `txt`. At each alignment, compare characters left-to-right until mismatch or full match.
  - Goal: write the doubly-nested-loop pseudocode (notes pg 3).
- [x] Worst case: O(mn)
  - Each of n - m + 1 alignments can do up to m character comparisons. Realised by `txt = aaaa...a`, `pat = aaa`.
  - Goal: derive (n - m + 1) * m and explain when that bound is actually tight.
- [x] Why every comparison really happens
  - In the all-`a` example no alignment terminates early because every character matches until pat is exhausted.
  - Goal: explain why early termination doesn't save you on this input.

---

## 3. Towards a smarter algorithm

- [x] Smarter shifts after a partial match
  - When `pat[1..k]` matched but `pat[k+1]` mismatched, you can sometimes shift by more than 1 and still be guaranteed not to miss an occurrence (notes pg 5).
  - Goal: redo Example 3 from the notes (`pat = abxyabxz`, `txt = xabxyabxyabxz`) and reproduce both the naive 20-comparison and the smarter 17-comparison alignments.
- [x] Skipping comparisons inside the next alignment
  - If you already know `pat[1..3] = pat[5..7]` and `pat[5..7] = txt[6..8]`, then after the shift you already know `pat[1..3] = txt[6..8]` and skip those comparisons. Drops to 14 comparisons.
  - Goal: explain in one sentence why preprocessing the pattern is the lever that makes both ideas cheap.
- [x] Why preprocessing has to be itself fast
  - "It is pointless to avoid comparisons if computing which to avoid costs more than just doing them." (notes pg 6)
  - Goal: state this constraint and use it to motivate why the preprocessor must be O(m).

---

## 4. Z-values and Z-boxes

- [x] Definition 2: Z-values
  - For each i > 1, Z_i is the length of the longest substring starting at i that matches a prefix of `str`. Formally `str[i..i+Z_i-1] = str[1..Z_i]`.
  - Goal: state the definition without looking and compute Z-values for `aabcaabxaay` from scratch (notes Example 4).
- [x] Lab notes-Q1: does Z_1 matter?
  - Goal: argue Z_1 is always n (the prefix matches itself fully) and explain why this trivial value carries no useful structural information.
- [x] Definition 3: Z-boxes
  - For i > 1 with Z_i > 0, the Z_i-box is the interval [i .. i + Z_i - 1] of `str`.
  - Goal: draw all Z-boxes for `aabcaabxaay` (notes figure 1) and explain why undefined Z-boxes correspond to Z_i = 0.
- [x] Definition 4: r_i, the right-most endpoint
  - r_i is the largest value of j + Z_j - 1 over all 1 < j <= i with Z_j > 0. The right end of the rightmost Z-box that begins at or before position i.
  - Goal: compute r_i for every i in `aabcaabxaay` (notes Example 6).
- [x] Definition 5: l_i, the matching left end
  - l_i is the left end of the Z-box that ends at r_i. If multiple Z-boxes end at r_i, any of their left ends is a valid choice.
  - Goal: compute l_i for every i in `aabcaabxaay` and check the worked Example 7.
- [x] Self-study: full (Z_i, Z_i-box, l_i, r_i) table for `aabaabcaxaababcy`
  - Goal: reproduce the table on notes pg 8 from scratch. This is the gymnastics required before the algorithm makes sense.

---

## 5. Naive Z-value computation

- [x] The naive procedure
  - For each i, compare `str[i..]` with `str[1..]` character by character until mismatch.
  - Goal: write the two-line pseudocode and confirm it produces the same Z-values as the worked example.
- [x] Lab notes-Q2: worst-case time complexity of naive Z computation
  - Goal: argue O(n^2). Worst case realised by `aaaa..a`, where each i does up to n - i comparisons.

---

## 6. Z-algorithm: state and base case

- [x] What state we keep across iterations (notes pg 9)
  - The full Z-array Z_2..Z_(k-1), and a single (l, r) pair holding the most recent l_i, r_i. The Z_l-box is reconstructable in O(1) from l and r.
  - Goal: explain why we don't need to store every (l_i, r_i) pair; just the most recent.
- [x] Base case: compute Z_2
  - Compare `str[2..]` with `str[1..]` until mismatch. If Z_2 > 0 set l = 2, r = Z_2 + 1; else l = r = 0.
  - Goal: hand-trace Z_2 on `aabcaabxaay`.

---

## 7. The general case: Case 1 (k > r)

- [x] Setup: inductive hypothesis
  - We have correct Z_2 .. Z_(k-1), and (l, r) = (l_(k-1), r_(k-1)).
  - Goal: state the invariant precisely, since both cases below depend on it.
- [x] Case 1: k is outside the rightmost Z-box (notes figure 2)
  - Previously computed Z-values give us no information about `str[k..]`. Compare explicitly against the prefix until mismatch at some q >= k.
  - If Z_k > 0, set r = q - 1 and l = k. Otherwise leave (l, r) unchanged.
  - Goal: write the pseudocode and explain why `l = k` (not k - 1 or anything else).

---

## 8. The general case: Case 2 (k <= r)

- [x] Why k <= r lets us reuse work (notes figures 3-5)
  - Z_l-box implies `str[l..r] = str[1..Z_l]`. Substring `str[k..r]` matches `str[k - l + 1..Z_l]` as a consequence.
  - Goal: redraw figures 3-5 from scratch. The whole algorithm rests on this geometry.
- [x] Case 2a: Z_(k-l+1) < r - k + 1 (notes figure 7)
  - The mirrored Z-box ends strictly before the right end of the Z_l-box, so the same mismatch character that bounded it bounds Z_k. Set Z_k = Z_(k-l+1). l, r unchanged.
  - Goal: prove this without looking at the figure; the key step is identifying the witness mismatch character x in the green region.
- [ ] Lab notes-Q3: case 2a index wrangling on `abcabdeabcabd`
  - Compute Z_5 and Z_8. Define l, k, r, p for both. Verify the algebra of p - k + l and p + l - 1 against the figure-7 derivation.
  - Goal: be able to instantiate every variable in the case 2a proof on a concrete worked example.
- [x] Case 2b: Z_(k-l+1) >= r - k + 1 (notes figures 8-9)
  - The mirrored Z-box reaches at least to the right end of the Z_l-box, so we know Z_k >= r - k + 1. Beyond r we have no information; explicitly compare `str[r+1..]` against `str[r - k + 2..]` until mismatch at q. Set Z_k = q - k, r = q - 1, l = k.
  - Goal: write the pseudocode. Explain why the explicit comparisons start at r + 1 and not k.
- [x] Lab Q4: split Case 2b into 2b.1 (strict >) and 2b.2 (=)
  - Goal: prove that Z_(k-l+1) > r - k + 1 forces Z_k = r - k + 1 with no character comparisons. The argument: if Z_k were larger, the mismatch that bounded Z_(k-l+1) at position k - l + 1 + Z_(k-l+1) - 1 would have to also bound the prefix at position Z_l, contradicting the Z_l-box being maximal.
  - Goal: only Z_(k-l+1) = r - k + 1 actually requires explicit comparisons.

---

## 9. Worked traces and case identification

- [x] Lab Q1: trace `abbabcabbabbababc`
  - Identify which case fires at k = 7, 10, 13, 15.
  - Goal: get the case identification right at every k, not just those four.
- [x] Lab Q2: if Z_2 = Len > 0, all Z_k for 3 <= k <= Len + 2 are resolvable without explicit comparisons
  - Goal: argue that within the initial Z-box every k uses Case 2a or Case 2b.1, neither of which compares characters.
- [x] Lab Q3: identify which exact case (1, 2a, or 2b) handles each of the Z_k values from Q2
  - Goal: produce a per-k table for the worked Q2 string.

---

## 10. O(n) time and O(n) space (the headline result)

- [x] Lab Q5 (= the proof on notes pg 13): Z-algorithm runs in O(n) time and O(n) space
  - Space: store the Z-array of size n plus O(1) extras.
  - Time: total work = iterations + character comparisons. Iterations: n - 1, each doing O(1) bookkeeping. Comparisons: at most n - 1 mismatches (one per iteration) plus at most n matches across the whole run (because each match strictly advances r, and r is monotone in [0, n]).
  - Goal: reproduce the proof, particularly the r-is-monotone-and-bounded amortised argument.
- [x] Self-study: where the matching budget is spent
  - Match work happens only inside Case 1 and Case 2b. Case 2a never compares characters.
  - Goal: identify which case is amortised against r and which is amortised against n - 1 mismatches.

---

## 11. Application: linear-time exact pattern matching

- [x] The construction (notes pg 15)
  - Build `str = pat + $ + txt`. Run Z on `str`. Any position i > m + 1 with Z_i = m corresponds to a match of `pat` in `txt` at position i - (m + 1).
  - Goal: explain why `$` (a character not appearing in either `pat` or `txt`) is required. What goes wrong without it?
- [x] Why the bound is O(n + m)
  - `|str| = m + 1 + n`, Z runs in O(|str|), matches read off from a single linear scan.
  - Goal: state the bound without looking and explain why it improves on naive O(mn).
- [ ] Lab notes-Q4: space complexity of pattern matching via Z
  - The literal construction stores `pat + $ + txt` and a Z-array of size m + 1 + n, giving O(m + n) space. Can you do better?
  - Goal: identify whether the Z-array entries for indices <= m + 1 are needed after the preprocessing phase, and whether the algorithm can be streamed so only O(m) auxiliary space is used past the pattern preprocessing.

---

## 12. Pseudocode summary (Section 4.2)

- [x] The full algorithm in one block
  - Base case: explicit comparison for Z_2.
  - Loop over k from 3 to n: Case 1 if k > r, Case 2a if k <= r and Z_(k-l+1) < r - k + 1, Case 2b otherwise.
  - Goal: write the entire algorithm from memory in under 30 lines, in a single take, then check against notes pg 14.

---

## 13. Applications and variants (lab Qs)

- [ ] Lab Q6: cyclic rotation detection
  - Given S, T of length n, decide if one is a cyclic rotation of the other. Standard trick: T is a rotation of S iff T occurs in S + S. Use Z on `T + $ + S + S`.
  - Goal: produce the construction, the matching condition, and the O(n) bound.
- [x] Lab Q7: longest suffix of S matching a prefix of T (`lab/prob7.py`)
  - Build `T + $ + S`. Run Z. The answer is the largest Z_k such that k + Z_k - 1 reaches the end of the combined string, i.e. the suffix of S extends all the way to the right boundary.
  - Goal: explain why "reaches the end" is the right condition.
- [ ] Lab Q8: Z^suffix array
  - Define Z^suffix[i] as the length of the longest substring of S **ending** at i that matches a suffix of S of equal length.
  - Approach: reverse S, run Z on the reverse, reverse the resulting array. Each Z^suffix[i] equals Z[n - i + 1] of the reversed string.
  - Goal: write the pseudocode and argue O(n) time + space.
- [ ] Lab Q9: matching prefix array MP[i]
  - MP[i] is the length of the longest suffix of S[i..n] that matches the prefix of S.
  - Approach: this is exactly Z[i] applied to indices where the Z-box reaches the right end. Or compute via a single Z pass and a right-to-left sweep.
  - Goal: write the pseudocode, justify O(n).

---

## 14. Implementation milestones, summarised

- [x] Step 1: think about practical optimisations before coding (Lab Impl 1, `lab/impl1.md`).
  - Done: the optimisation note in `impl1.md` collapses Cases 2a and 2b into a single `min(Z[k-l], r-k+1)` write, with explicit comparisons only triggered when Z[k-l] == r - k + 1 (Case 2b.2).
- [x] Step 2: implement the Z-algorithm (Lab Impl 2, `src/zalg.py`).
  - 0-based indexing in code despite the 1-based notes; counters track Case 1, Case 2a (reuse), Case 2b.1 (clamp), Case 2b.2 (extend).
  - Tests in `tests/test_zalg.py`.
- [x] Step 3: linear-time exact pattern matching (Lab Impl 3, `lab/impl4.py`).
  - Construct `pat + $ + txt`, run zalg, return positions where Z equals pattern length.
- [x] Step 4: Lab Q7 longest-suffix-of-S-matching-prefix-of-T (`lab/prob7.py`).
- [ ] Step 5: Lab Q6 cyclic rotation detector. New file `lab/prob6.py`. Build `T + $ + S + S`, run zalg, return any position with Z == n.
- [ ] Step 6: Lab Q8 Z^suffix array. New file `lab/prob8.py`. Reverse, zalg, reverse the result.
- [ ] Step 7: Lab Q9 MP[] array. New file `lab/prob9.py`.