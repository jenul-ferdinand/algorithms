# Week 3: Burrows-Wheeler Transform - Learning Roadmap

Source material: `seminar03.pdf`, `bwtproofs.pdf`, `lab03.pdf`.
Note: there is no `notes03.pdf` for this week. The proofs document `bwtproofs.pdf` plays the role of formal notes for the LF-mapping and backward-search update rules.

Legend: `[ ]` concept / theorem / proof to learn. `[ ] Lab Qx`: question from `lab03.pdf`. `[ ] Impl`: implementation exercise. Goals describe what "done" looks like.

The order is the order to learn in. Each section assumes everything above it.

---

## 1. Why BWT

- [x] What BWT actually is
    - A reversible permutation L of `S$` that groups similar characters together. Same information as S, but arranged so a compact search index falls out for free.
    - Goal: state in one sentence what BWT produces and what it lets you do (compression, pattern matching in O(m), part of bwa/samtools).
- [x] How BWT fits among the matching algorithms
    - Z-algorithm: preprocess `pat + $ + txt`, O(m + n) per query.
    - Boyer-Moore: preprocess pattern, O(m + n) worst case.
    - BWT: preprocess text once into an O(n) index, then any subsequent query takes O(m + occ).
    - Goal: explain why BWT is the right answer when you have many patterns to match against the same fixed text.

---

## 2. The cyclic permutation matrix M

- [x] Definition: cyclic permutation matrix
    - For `S[1..n]` (with `$` appended), M is the n by n matrix whose rows are all n cyclic rotations of S, sorted lexicographically.
    - Goal: write the definition and explain why `$` (lex-smallest) makes the sort uniquely defined.
- [x] Each column is a permutation of S
    - Every character of S appears exactly once per column, by construction.
    - Goal: justify in one sentence.
- [x] Lab Q1(a): hand-construct M for `S = mississippi$`
    - 12 rows, sorted. Use the .xopp working in `lab/prob01.xopp` as a check.
    - Goal: produce M from scratch, no peeking.
- [x] Lab Q1(d): visually confirm each column of M is a permutation of S
    - Goal: tick off character counts column by column.

---

## 3. BWT as the last column L

- [x] Definition: L = M_col(n)
    - L is the last column of M. By convention, this is "the BWT of S".
    - Goal: read off L from your M for `mississippi$`. Check it equals `ipssm$pissii`.
- [x] Naive construction time complexity
    - Build all n cyclic rotations: O(n^2) characters. Sort them: O(n^2 log n) using string comparisons that are themselves O(n).
    - Goal: state the bound and identify the dominant cost.
- [x] Lab Q1(b): worst-case time complexity of naive M-based BWT construction
    - Goal: argue O(n^2 log n) and call out the storage cost O(n^2).

---

## 4. Suffix array as the bridge

- [x] Definition: suffix array
    - SA[i] is the starting index in S of the suffix that, sorted lexicographically, occupies rank i.
    - Goal: hand-build SA for `mississippi$` and check it lines up with the row order of M.
- [x] Lab Q1(c): why does sorting suffixes match sorting cyclic rotations?
    - Because `$` is unique and lex-smallest, every cyclic rotation of `S$` is uniquely identified by its prefix up to (and including) `$`. The prefix of rotation i up to `$` equals the suffix `S[i..]$`.
    - Goal: produce the proof in one paragraph.
- [x] Lab Q1(e): BWT from SA in O(n)
    - L[i] = S[SA[i] - 1] (with SA[i] = 0 wrapping to S[n] = `$`).
    - Goal: state the formula and argue O(n) once SA is given.
- [x] Naive suffix array
    - Sort all n suffixes directly, O(n^2 log n).
    - File: `src/suffix_array_naive.py`.
- [x] Prefix-doubling suffix array
    - log n rounds, each sort doubles the prefix length compared. O(n log^2 n) with sort, O(n log n) with radix sort.
    - File: `src/suffix_array_prefix_doubling.py`.
    - Goal: explain how rank pairs (rank[i], rank[i + k]) in round k uniquely order suffixes once k >= longest LCP.
- [ ] Looking ahead: linear-time SA via Ukkonen
    - A linear-time suffix tree (Ukkonen, wk04) yields a linear-time suffix array via in-order DFS, hence linear-time BWT.
    - Goal: keep this connection in mind while learning wk04.

---

## 5. F (first column) and the rank function

- [x] F = sort(L)
    - F is the first column of M. Since each row of M is a rotation of S, F is L sorted.
    - Goal: read off F for `mississippi$` and verify it equals `$iiiimppssss`.
- [x] Definition: Rank(x)
    - Rank(x) = the position (0-indexed or 1-indexed, pick a convention) of the first occurrence of character x in F.
    - Goal: compute Rank for every character that appears in `mississippi$`.
- [x] Lab Q5: rank preprocessing pseudocode
    - Count character frequencies in L, then build the cumulative starting position of each character in F.
    - File: `process_rank()` in `src/bwt.py`.
    - Goal: O(n + |sigma|) time, O(|sigma|) space. State both bounds.

---

## 6. Inverting the BWT (LF-mapping)

- [x] The "L precedes F" property
    - Each row of M ends with the character (at position last column) that immediately precedes (cyclically) the character at the start of the row (first column).
    - Goal: visually verify on `mississippi$`. Pick a row, identify L[i] and F[1] of that row, check L[i] is the predecessor of F[i] in S.
- [x] Lab Q1(f): visual LF-mapping for `mississippi$`
    - For every L[i], identify the row p in M whose first column F[p] equals L[i] and corresponds to the same instance.
    - Goal: produce the full LF table.
- [x] Lab Q1(g): why L[p] immediately precedes L[i] in S
    - Each row of M is a rotation; the last character of row i is the one preceding the first character of row i in S. Following the LF-link reconstructs S character by character, going backwards.
    - Goal: prove in one paragraph using row p = LF[i] and the rotation definition.
- [ ] Theorem 1 (LF-mapping, `bwtproofs.pdf`): for L[i] = x, p = Rank(x) + nOcc(x, L[1..i))
    - Translation: the row in M whose F-position holds the same instance of x as L[i] is exactly Rank(x) plus the number of x's seen earlier in L (excluding position i).
    - Goal: state the theorem from memory.
- [ ] Lemma 2: order-preservation under right cyclic shift
    - For L[i_1] = L[i_2] = x with i_1 < i_2, M_row(i_1) precedes M_row(i_2) iff `rcylshift(M_row(i_1), 1)` precedes `rcylshift(M_row(i_2), 1)`.
    - Proof: since the rotations end in the same x, the lexicographic order is decided by the prefix alpha (resp beta) before x. Right-cyclic-shifting moves x to the front but leaves alpha/beta in identical positions, so the order is preserved.
    - Goal: reproduce the proof.
- [ ] Corollary 3: same order for all instances of x
    - The k instances of x in L map to k consecutive rows in F starting at Rank(x), in the same relative order.
    - Goal: state and explain why this is what gives LF-mapping its closed form.
- [ ] Lab Q2: prove Theorem 1
    - Combine Lemma 2 + Corollary 3 with the observation that nOcc(x, L[1..i)) selects the i-th instance of x.
    - Goal: write the proof.
- [x] Lab Q4: worst-case inversion without preprocessing rank/nOcc
    - Each step of the LF walk is O(n) if you scan L for rank and counts. n steps gives O(n^2) time, O(n) space.
    - Goal: state both bounds.
- [x] Lab Q6: nOcc preprocessing pseudocode (for inversion)
    - For each character that appears in L, store a single counter or build the 2D occ table once. For inversion only, you actually only need count up to position i for each i, computable in O(n |sigma|) time and space.
    - File: `process_occ()` in `src/bwt.py`.
    - Goal: write the pseudocode, justify O(n |sigma|).
- [x] Lab Q7: total inversion complexity with preprocessing
    - Preprocess rank: O(n + |sigma|). Preprocess occ: O(n |sigma|). LF walk: n steps, O(1) each. Total: O(n |sigma|) time, O(n |sigma|) space.
    - Goal: state both bounds and identify which preprocessing dominates.
- [x] Lab Q3: invert `ooolooooolwml$`
    - Run the LF walk by hand. Recover S.
    - Goal: produce the original string and verify by rebuilding M and reading off the column.
- [x] Impl: BWT inversion (Lab Impl 2, `inverse_bwt()` in `src/bwt.py`).

---

## 7. Pattern matching with BWT (backward search)

- [x] The backward search idea
    - Maintain a row range [sp, ep] of M such that the first |alpha| columns of those rows spell the current matched suffix alpha. Start with alpha empty and [1, n]. At each step, left-extend alpha by one character of the pattern (read pattern right-to-left) and update [sp, ep].
    - Goal: explain why "left-extend" is the natural direction (BWT lets you compute predecessors via L, not successors).
- [ ] Theorem 4 (`bwtproofs.pdf`): the update rules
    - sp' = Rank(x) + nOcc(x, L[1..sp))
    - ep' = Rank(x) + nOcc(x, L[1..ep]) - 1
    - Goal: state both rules from memory and derive them by applying Theorem 1 to the first and last instance of x in L[sp..ep].
- [ ] Lab Q9: prove Theorem 4
    - Identify the first instance of x in L[sp..ep] at L[i] and the last at L[j]. Apply Theorem 1 to L[i] for sp', and to L[j] for ep'. The half-open vs closed interval choice in nOcc is what flips between sp's exclusive and ep's inclusive count.
    - Goal: produce the full proof, attentive to the off-by-one (the -1 in ep').
- [ ] Corollary 5: null range when xα is absent
    - If x is not in L[sp..ep], the formulas give ep' = sp' - 1, an empty range.
    - Goal: state and verify on a worked example (search a non-existent pattern).
- [x] Corollary 6: backward search algorithm
    - Start [sp, ep] = [1, n], alpha = empty. For i from m down to 1, apply the update rules with x = pat[i]. After m steps, the surviving range gives all matches.
    - Goal: write the loop pseudocode (5 lines).
- [x] Lab Q8: hand-trace `pat = iss` against the BWT of `mississippi$`
    - Initial range [1, 12]. Apply update for s, then s, then i. Track sp, ep at each step.
    - Goal: produce the trace and read off the final range.
- [x] Lab Q8(c): number of occurrences from final range
    - occ count = ep - sp + 1.
    - Goal: state and verify against `mississippi`.
- [x] Lab Q8(d): loci of occurrences (positions in S)
    - Need the suffix array. Positions are SA[sp], SA[sp+1], ..., SA[ep].
    - Goal: explain why SA is needed (the BWT alone gives counts but not loci).
- [x] Lab Q10: nOcc preprocessing for pattern matching
    - Build the full 2D occ table indexed by character and position. For matching you need queries at arbitrary positions, not just up to i, so the trick used for inversion does not suffice.
    - File: `process_occ()` in `src/bwt.py`.
    - Goal: O(n |sigma|) time and space; O(1) lookup.
- [x] Lab Q11: total backward search complexity
    - Preprocessing: BWT O(n log n) via prefix doubling (or O(n) via Ukkonen wk04), rank O(n + |sigma|), occ O(n |sigma|), suffix array O(n log n) or O(n).
    - Per query: O(m) update steps, each O(1) given the preprocessed structures. Plus O(occ) to read out positions from SA.
    - Total query: O(m + occ).
    - Goal: state preprocessing vs per-query bounds separately. Note that preprocessing is amortised across many queries against the same text.
- [x] Impl: BWT-based pattern matching (Lab Impl 3, `src/bwt_search.py`).

---

## 8. Optional: run-length encoding and the compression view

- [x] Why BWT compresses well
    - The BWT clusters runs of identical characters. RLE on L is dramatically shorter than RLE on S for typical inputs.
    - Goal: compute the BWT of `aabbcc...` style strings and compare RLE lengths.
- [x] Impl: simple RLE encoder/decoder (`src/rle.py`).
    - Goal: round-trip an arbitrary BWT through RLE.

---

## 9. Implementation milestones, summarised

A re-listing of the implementation steps in order. Files live in `src/`.

- [x] Step 1: naive suffix array (`src/suffix_array_naive.py`).
    - Sort all n suffixes by direct string comparison. O(n^2 log n). Used as the baseline correctness check.
- [x] Step 2: prefix-doubling suffix array (`src/suffix_array_prefix_doubling.py`).
    - log n rounds with rank pairs. O(n log^2 n) with built-in sort.
- [x] Step 3: naive BWT construction via M (`src/bwt_naive.py`).
    - Build all rotations, sort, take the last column. O(n^2 log n). Used to validate `bwt.py` on small inputs.
- [x] Step 4: BWT via suffix array (Lab Impl 1, `src/bwt.py`).
    - L[i] = S[SA[i] - 1] with wrap-around. O(n log n) end-to-end via prefix doubling.
    - Tests in `tests/test_bwt.py`.
- [x] Step 5: rank and occ preprocessing (`process_rank`, `process_occ` in `src/bwt.py`).
- [x] Step 6: BWT inversion via LF-mapping (Lab Impl 2, `inverse_bwt` in `src/bwt.py`).
- [x] Step 7: BWT-based pattern matching (Lab Impl 3, `src/bwt_search.py`).
    - Backward search with [sp, ep] updates, returns SA[sp..ep].
    - Tests in `tests/test_bwt_search.py`.
- [x] Step 8 (bonus): RLE encoder for the compression view (`src/rle.py`).
- [ ] Step 9 (stretch, after wk04): swap prefix-doubling SA for an Ukkonen-derived linear-time SA. This drops BWT construction from O(n log n) to O(n).
- [ ] Step 10 (stretch): write up Theorem 1 and Theorem 4 proofs in `lab/` as `prob02.md` (LF-mapping) and `prob09.md` (backward search update rules), referring to `bwtproofs.pdf`.
