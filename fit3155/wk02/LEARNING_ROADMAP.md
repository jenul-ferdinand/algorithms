# Week 2: Boyer-Moore (and KMP) - Learning Roadmap

Source material: `notes02.pdf` (19 pages), `seminar02.pdf`, `lab02.pdf`.  
Lab exercises drawn from `lab02.pdf` are woven in as checkpoints under each topic.

Legend: `[ ]` concept / theorem / proof to learn. `[ ] Lab Qx`: question from `lab02.pdf`. `[ ] Lab notes-Qx`: question embedded in `notes02.pdf`. `[ ] Impl`: implementation exercise. Goals describe what "done" looks like.

The order is the order to learn in. Each section assumes everything above it.

---

## 1. Why Boyer-Moore at all

- [x] Boyer-Moore vs Z-algorithm-based pattern matching
  - Z-based matching preprocesses `pat + $ + txt` and finds matches by reading off Z-values. Worst case O(m + n), but it never skips text characters.
  - Boyer-Moore preprocesses just the pattern and can skip whole sections of `txt` it never reads. Sublinear on average, O(m + n) worst case (with Galil's optimisation).
  - Goal: explain in one sentence why "skipping over text" is more intuitive than "computing Z-values of text".
- [x] The three ideas Boyer-Moore combines
  - Right-to-left scanning, the bad character shift rule, the good suffix shift rule.
  - Goal: state all three from memory before any preprocessing details.

---

## 2. Right-to-left scanning

- [x] The scan direction
  - Each alignment compares `pat[m]` with `txt[j + m - 1]`, then `pat[m-1]` with `txt[j + m - 2]`, etc., until mismatch or full match.
  - Goal: trace Example 1 (`pat = tpabxab`, `txt = xpbctbxabxctbpq`). Identify the matched suffix and the mismatching character.
- [x] Why the direction matters
  - When mismatch happens at pattern index k, `pat[k+1..m]` is a known matched suffix of the pattern. This is the substrate the good suffix rule eats.
  - Goal: explain why right-to-left is essential for the good suffix rule but irrelevant on its own.

---

## 3. The bad character rule

- [x] Bad character definition
  - On mismatch at pattern index k, the bad character is `x = txt[j + k - 1]`. The pattern character there is `y = pat[k]`. Shift the pattern to align the rightmost occurrence of x in `pat` with the bad character in `txt`.
  - Goal: redo Example 2 by hand (shift by 2 on the `tpabxab` pattern).
- [x] Definition of R(x)
  - R(x) = position of the rightmost occurrence of x in `pat`, else 0 if x doesn't appear.
  - Goal: compute R(x) for `tpabxab` for every x in {a, b, c, p, q, t, x}.
- [x] The shift formula
  - Three sub-cases (notes figures 2-5):
    - R(x) < k: shift by k - R(x). Aligns the rightmost x in pat with the bad x in txt.
    - R(x) = 0: x doesn't occur in pat. Shift by k. Equivalent to k - R(x).
    - R(x) > k: an occurrence to the right of the mismatch. The rule degenerates; shift by 1 (the safest fallback).
  - Compact form: `shift = max(k - R(x), 1)`.
  - Goal: prove each sub-case is safe; explain why the third case is the one that motivates the extended rule.
- [x] Lab notes-Q1: bad character preprocessing pseudocode (`questions/q01.md`)
  - Goal: O(m) construction, O(1) lookup, O(|sigma|) space (size-of-alphabet array).
- [x] Worked example
  - Reproduce Example 3 (`txt = xpbctbxabacbxtbpqa`, `pat = tbapxab`) with the R(x) table on notes pg 5.
  - Goal: every iteration's mismatch and shift matches the figure.
- [ ] Lab Q1 (bad character half): R(x) and R_k(x) tables for `pat = yzzyzxyzzyz`
  - Build the standard bad character shift array (the R(x) part).
  - Goal: produce the R(x) row by hand.
- [ ] Lab Q2 (bad character half): construction and lookup complexity for R(x)
  - Goal: O(m + |sigma|) construction, O(1) lookup, O(|sigma|) space.

---

## 4. The extended bad character rule

- [x] Why extending matters
  - Basic R(x) wastes shifts when the rightmost occurrence of x is to the right of the mismatch position k. R_k(x) constrains "rightmost" to "rightmost to the left of k".
  - Goal: explain why this fixes the R(x) > k degeneracy and removes the max(., 1) clamp.
- [x] Definition of R_k(x)
  - R_k(x) = position of the rightmost occurrence of x strictly to the left of position k in `pat`, else 0.
  - Goal: state the definition and compute it for `tbapxab` (notes Example 4 table on pg 7).
- [x] The shift formula
  - shift = k - R_k(x). Always non-negative because R_k(x) < k by definition (or R_k(x) = 0 meaning shift past).
  - Goal: explain why no max(., 1) is needed here.
- [x] 2D-array preprocessing
  - Build R_k(x) as an m by |sigma| table. Walk left-to-right; row i is row i-1 with one entry updated for `pat[i]`.
  - Goal: state the recurrence and see why it is O(m * |sigma|) time and space.
- [x] Lab notes-Q2.1: extended BC preprocessing pseudocode (`questions/q02.1.py`)
  - Goal: dynamic-programming table fill, O(m * |sigma|).
- [x] Lab notes-Q2.2: space-efficient R_k(x) (`questions/q02.2.md`)
  - For each character that appears in `pat`, store a sorted list of its positions. On mismatch, binary search for the rightmost position less than k.
  - Goal: O(m) total space (each pattern position appears once across all lists), O(log m) lookup.
- [ ] Lab notes-Q3: bad character implementation issue on full pattern match
  - When right-to-left scan finishes without mismatch (a full match), there is no bad character. Bad character rule cannot suggest a shift; the good suffix rule must.
  - Goal: state the issue precisely and note that good suffix handles it via mp[2].
- [ ] Lab Q1 (extended half): R_k(x) table for `pat = yzzyzxyzzyz`
  - Goal: produce the m by |sigma| table by hand.
- [ ] Lab Q2 (extended half): construction and lookup complexity for R_k(x)
  - Construction: O(m * |sigma|) time and space for the 2D table.
  - Lookup: O(1).
  - Goal: contrast with R(x) and call out when the extra factor is worth it.
- [x] Lab Q3: O(m + |sigma|) construction with O(log m) lookup
  - The space-efficient version from Lab notes-Q2.2: per-character sorted position lists, binary-search lookup.
  - Goal: argue O(m) space for the lists plus O(|sigma|) for the dispatch table; lookup is O(log m) (not O(1)).

---

## 5. Good suffix rule

- [x] Worst case of bad character (Example 5)
  - `txt = aaaa...a`, `pat = baa`. Right-to-left finds two matches plus a mismatch at every alignment, shifts by 1 each time, gives O(mn).
  - Goal: argue why bad character alone never breaks O(mn).
- [x] Strong good suffix rule (notes pg 9-10)
  - On mismatch at position k with matched suffix `pat[k+1..m]`, find the rightmost occurrence of this suffix elsewhere in `pat` whose preceding character differs from `pat[k]`. Shift to align it with the matched region in `txt`.
  - Goal: redo notes figures 9-11 from scratch with `pat = acababaca` (mismatch at k = 7, good suffix `aba`).
- [x] Definition 1: Z^suffix values
  - Z^suffix_i = length of the longest substring ending at position i in `pat` that matches a suffix of `pat`. Computed by reversing `pat`, running Z, reversing the array.
  - Goal: hand-compute Z^suffix for `pat = acababacaba` (notes Example 6).
- [x] Good suffix array gs(j)
  - gs(j) = right endpoint p of the rightmost substring `pat[p - Z^suffix_p + 1..p]` such that this substring equals `pat[j..m]` and is preceded by a character different from `pat[j - 1]`.
  - Goal: derive the gs values for `acababacaba`. Verify gs(7) = 5 from the worked example on notes pg 11.
- [x] Preprocessing gs from Z^suffix (pseudocode on notes pg 12)
  - Initialise gs[1..m+1] = 0. For p from 1 to m - 1, set j = m - Z^suffix_p + 1, gs[j] = p.
  - Goal: rewrite the pseudocode and explain why iterating from 1 (not m) is safe (later p overwrites earlier).
- [x] Definition 2: matched prefix mp(k+1)
  - mp(k+1) = length of the longest suffix of `pat[k+1..m]` that matches a prefix of `pat`. The fallback when gs(k+1) = 0.
  - Goal: compute mp(.) for `acababacaba` (notes Example 7); verify mp(5) = 5 since `acaba` is the prefix.
- [x] Lab notes-Q4: preprocessing mp(.) in O(m) using the Z-algorithm
  - Run Z on `pat`. For any i with i + Z_i - 1 = m (i.e. the Z-box reaches the end of `pat`), Z_i is a candidate matched prefix length for the suffix starting at i. Sweep right-to-left to fill mp(.).
  - Goal: write the pseudocode and argue O(m).
- [x] The shift formula
  - On mismatch at k: if gs(k+1) > 0, shift by m - gs(k+1). Else if mp(k+1) > 0, shift by m - mp(k+1). Else shift by m.
  - On full match: shift by m - mp(2).
  - Goal: state both shift cases from memory.
- [ ] Lab notes-Q5: good suffix on `pat = aaa`, `txt = aaaa..a`
  - Determine the alignments the good suffix rule explores. Compare to bad character.
  - Goal: confirm that even good suffix gives O(mn) on this input (motivates Galil).
- [ ] Lab Q4: hand-compute gs and mp for `pat = abaaabacbaabaaab`
  - Build the gs array (length m + 1) and the mp array (length m + 1).
  - Goal: a single table side-by-side with the pattern, gs, mp.
- [ ] Lab Q6: prove the good suffix shift gs(k+1) > 0 is safe
  - Setup: mismatch at k, matched suffix `pat[k+1..m] = txt[j+k..j+m-1]`. gs(k+1) = p > 0 means `pat[p - len + 1..p]` equals the matched suffix and `pat[p - len]` differs from `pat[k]`.
  - Argument: any shift by less than m - p would either re-cause the same mismatch (if a substring matched the suffix) or align a non-matching substring. The next valid alignment is the one at exactly m - p.
  - Goal: write the proof, explicitly invoking that gs uses the rightmost qualifying p.
- [ ] Lab Q7: prove the matched prefix shift mp(k+1) is safe when gs(k+1) = 0
  - Setup: mismatch at k, gs(k+1) = 0 so no internal occurrence of the matched suffix exists. The only possible re-alignment is to align a prefix of `pat` with a suffix of the matched region in `txt`.
  - Argument: mp(k+1) gives the longest such prefix. Shifting by m - mp(k+1) aligns it; shifting by less would skip past valid alignments.
  - Goal: produce the proof and call out the corner case mp(k+1) = 0 (shift by m).
- [ ] Lab Q8: prove the post-full-match shift m - mp(2) is safe
  - Setup: `pat[1..m] = txt[j..j + m - 1]`. The next occurrence (if any) must overlap with this one such that a prefix of `pat` aligns with a suffix of the current match.
  - Argument: mp(2) is the length of the longest proper suffix of `pat[2..m]` matching a prefix of `pat`. Shifting by m - mp(2) is the smallest shift that could realign without missing.
  - Goal: produce the proof, explicit about why we use mp(2) and not mp(1) (mp(1) would be m and miss valid overlaps).

---

## 6. Combining bad character and good suffix

- [x] Picking the larger shift
  - Both rules return safe shifts. Boyer-Moore takes max(n_badchar, n_goodsuffix) every iteration.
  - Goal: argue why max is always safe (both individual shifts are safe).

---

## 7. Galil's optimisation

- [x] Worst case of good suffix alone (Example 8)
  - `pat = aaa`, `txt = aaaa..a`. Every alignment is a full match. Shifts by 1 each time. Still O(mn).
  - Goal: identify which characters in `txt` are being needlessly re-compared.
- [x] The optimisation idea (notes pg 14-15)
  - After a good suffix or matched prefix shift, a region of the pattern is already known to match the text. The next right-to-left scan can skip that region.
  - Goal: explain why this is restricted to good suffix / matched prefix shifts and not bad character shifts.
- [x] start and stop pointers
  - After a gs(k+1) = p > 0 shift: stop = p, start = p - m + k + 1.
  - After an mp(k+1) shift: stop = mp(k+1), start = 1.
  - Right-to-left scan does `pat[stop+1..m]`, then `pat[1..start-1]`. Skips `pat[start..stop]`.
  - Goal: trace the figures on notes pg 16; verify start, stop are computed correctly for the figure-15 example.
- [x] Time complexity O(m + n) worst case
  - With Galil, each text character is compared at most a constant number of times across the whole search.
  - Sublinear on natural-language inputs is the typical case (notes pg 17 mentions O(n/m)).
  - Goal: state the bound (NOT EXAMINABLE proof) and recall that practical workloads sit closer to O(n/m).
- [ ] Lab Q5: count explicit comparisons on the periodic input
  - `txt = (abcde)^8`, `pat = (abcde)^3`. Apply Boyer-Moore with Galil and tally character comparisons across all alignments.
  - Goal: produce the count and identify how many alignments are skipped entirely by the good-suffix-with-Galil shift.

---

## 8. End-to-end Boyer-Moore (Section 1.1.6 summary)

- [x] Preprocessing in O(m)
  - R(x) or R_k(x) for the bad character.
  - Z^suffix, gs, mp for the good suffix and matched prefix.
  - Goal: list the four arrays computed and state the cost of each.
- [x] Search phase pseudocode
  - Loop alignments. Each iteration: right-to-left scan with Galil's start/stop, compute n_badchar and n_goodsuffix, shift by max.
  - Goal: write it from memory; check against notes pg 17.

---

## 9. KMP (optional, per LEARNING_INTENTIONS)

- [ ] When KMP gets used vs Boyer-Moore
  - KMP: left-to-right scan, only one shift rule (analogous to good suffix). Worst case O(m + n), no sublinear behaviour. Less practical but easier to generalise.
- [ ] Definition 3: SP_i values
  - SP_i = length of the longest proper suffix of `pat[1..i]` that matches a prefix of `pat`, with the constraint `pat[i+1] != pat[SP_i + 1]`.
  - Goal: compute SP for `bbccaebbcabd` (notes Example 9) and compare with mp values.
- [ ] Preprocessing SP from Z (pseudocode on notes pg 18)
  - Run Z on `pat`. For j from m down to 2: i = j + Z_j - 1, SP_i = Z_j.
  - Goal: explain why iterating j downwards is the correct direction (later assignments lose to earlier ones).
- [ ] KMP shift rule
  - On mismatch at position i + 1 with matched prefix `pat[1..i] = txt[j..j + i - 1]`, shift by i - SP_i. After the shift, the prefix `pat[1..SP_i]` is already known to match.
  - On full match, shift by m - SP_m.
  - Goal: trace the figure on notes pg 19; identify the analogy with mp + Galil.

---

## 10. Implementation milestones, summarised

A re-listing of the implementation steps in order. Files live in `src/`.

- [x] Step 1: think about practical optimisations before coding (Lab Impl 1).
  - Captured implicitly across the suite of `boyermoore_*.py` variants below.
- [x] Step 2: naive baseline for comparison and sanity checks.
  - Reuse the Z-algorithm-based pattern matcher from wk01 (`fit3155/wk01/lab/impl4.py`) as the reference. Tests in `tests/test_boyermoore.py`.
- [x] Step 3: basic bad character (`src/boyermoore_basic.py`).
  - R(x) preprocessing, max(k - R(x), 1) shift, right-to-left scan.
- [x] Step 4: extended bad character (`src/boyermoore_extendedbcr.py`).
  - R_k(x) 2D table, k - R_k(x) shift.
- [x] Step 5: good suffix preprocessing (`src/boyermoore_gs.py`).
  - Includes `process_z_suffix()` (Z on reversed pat then reversed) and `process_gs()`.
- [x] Step 6: matched prefix and good-suffix-only matcher (`src/boyermoore_mp.py`).
  - mp via the Z-on-pattern sweep. Combined gs + mp shift used for the search phase.
- [x] Step 7: full Boyer-Moore with Galil's optimisation (`src/boyermoore_optimised.py`, Lab Impl 2).
  - Combines extended bad character, good suffix, matched prefix, and start/stop pointers.
- [ ] Step 8 (stretch): write up Lab Qs 6-8 proofs in `lab/` as `prob6.md`, `prob7.md`, `prob8.md`.
- [ ] Step 9 (optional): KMP implementation in `src/kmp.py`. SP_i via Z, left-to-right matcher.