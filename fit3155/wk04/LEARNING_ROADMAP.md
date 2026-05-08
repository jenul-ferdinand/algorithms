# Week 4: Ukkonen's linear-time suffix tree construction - Learning Roadmap

Source material: `notes04.pdf` (40 pages), `seminar04.pdf`, `lab04.pdf`, `construction-example.pdf`, `skiptrick.pdf`, `construction-recording.mp4`.  
Lab questions are drawn from `lab04.pdf`. Notes-internal questions are tagged Lab notes-Qx.

Legend: `[ ]` concept / theorem / proof to learn. `[ ] Lab Qx`: lab question. `[ ] Lab notes-Qx`: question embedded in `notes04.pdf`. `[ ] Impl`: implementation exercise. Goals describe what "done" looks like.

The order is the order to learn in. Each section assumes everything above it. Implementation milestones are interleaved at the point where you have enough theory to write that step.

---

## 1. Suffix tree foundations

- [ ] The substring matching problem (Definition 1)
  - Pattern is unknown ahead of time, text is fixed. Preprocess `txt[1..n]` so any `pat[1..m]` answers in O(m).
  - Goal: explain why this flips the role of pattern and text vs. preprocessing-the-pattern algorithms.
- [ ] Definition 2: suffix tree (the 5 defining properties)
  - n leaves numbered 1..n; non-root internal nodes have >= 2 children; edges labelled with non-empty substrings of `str`; no two edges out of a node start with the same character; the root-to-leaf-i path spells `str[i..n]`.
  - Goal: state all 5 from memory and check a small example tree against each.
- [ ] Why a terminal character is needed (Definition 3)
  - Without `$`, a string like `abcab` produces a tree that violates property 1 (a suffix becomes a prefix of another). `$` is unique and lex-smallest.
  - Goal: explain why `abcab` fails the definition and why appending `$` fixes it.
- [x] Naive O(n^2) suffix tree construction (overview)
  - Insert suffixes longest-first; walk root-down matching characters; split an edge when you hit a mismatch inside it.
  - Goal: explain edge splitting, i.e. when you mismatch mid-edge create a new internal node u, attach the existing child below u with the trimmed edge, attach a new leaf as the second child of u with the rest of the suffix.
  - [x] Lab notes-Q1: prove the naive construction is O(n^2).
- [ ] Space-efficient edge labels (introduced here, proven later)
  - Replace each substring label with a tuple `(j, i)` referencing `str`. Each label is then O(1) space.
  - Goal: redraw the suffix tree of `abaaba$` using `(j,i)` tuples instead of substrings.
- [ ] Lab notes-Q2: prove the (j,i) representation makes the suffix tree O(n) space (assume fixed alphabet). Theorem 2 (later) is the formal version.
- [x] Impl: naive suffix trie construction.
  - File: `src/naive_suffix_trie.py` (done).
- [ ] Impl: naive O(n^2) suffix tree construction.
  - File: `src/naive_suffix_tree.py` (in progress, currently a stub).
  - Goal: handle the three insertion cases by hand: (i) suffix branches off at an existing node, (ii) suffix walks into an existing edge and the path ends mid-edge with a mismatch (split), (iii) suffix is a prefix of an existing path (only happens before adding `$`, with `$` it cannot).
  - Use TERMINAL_CHAR from `fit3155/common/constants.py`. Append `$` if not already there.
  - This is the implementation that the rest of Ukkonen will incrementally improve on.

---

## 2. Implicit suffix trees

- [ ] Definition 4: implicit suffix tree
  - Take the suffix tree of `str$`. Remove every `$`, drop edges that became empty, then path-compress any internal node left with one child.
  - Goal: produce the implicit suffix tree of `abcab` from the suffix tree of `abcab$` by hand.
- [ ] Definition 5: implicit suffix trees (alternate)
  - Build the suffix tree for `str` without first appending `$`.
  - Goal: convince yourself the two definitions yield the same tree.
- [ ] Why implicit trees are the unit of incremental construction
  - Ukkonen builds I_1, I_2, ..., I_n where I_i is the implicit suffix tree of the prefix `str[1..i]`. The final regular suffix tree is one more phase that appends `$`.
  - Goal: explain in one sentence why incremental growth is impossible if you insist on always being a regular suffix tree at every step.

---

## 3. Naive Ukkonen: phases and the three extension rules

- [ ] High level structure (Section 3.1)
  - n phases. Phase i+1 turns I_i into I_(i+1) by performing one extension for every j with 1 <= j <= i+1, in order. Extension j of phase i+1 grows the suffix `str[j..i]` into `str[j..i+1]`.
  - Goal: write the doubly nested loop pseudocode. Outer loop over phases, inner loop over j.
- [ ] Lab Q1(a): what information is stored at the end of phase i?
  - Goal: state precisely "the implicit suffix tree of `str[1..i]`", and what that means about which suffixes are present (all of them, possibly implicitly along an internal path).
- [ ] The four extension scenarios (Lab Q1(b))
  - Lab Q1(b)i: alpha = `str[j..i]` is being seen for the first time at position j (Rule 1 trigger).
  - Lab Q1(b)ii: alpha was seen before, always followed by the same y != x (Rule 2 regular trigger, leaf added at an existing internal node).
  - Lab Q1(b)iii: alpha was seen before with two or more distinct following characters all != x (Rule 2 alternate trigger, must split an edge).
  - Lab Q1(b)iv: alpha followed by x has been seen before (Rule 3 trigger).
  - Goal: for each scenario, draw the position structure on the input string, and predict which rule fires before reading the formal definitions below.
- [ ] Definition 6: Rule 1 extension
  - Path `str[j..i]` ends at a leaf. Extend the leaf edge label by `str[i+1]`.
  - Goal: justify "once a leaf, always a leaf" from this definition alone.
- [ ] Definition 7: Rule 2 case 1 (regular)
  - Path `str[j..i]` ends at an existing internal node u, and u has no outgoing edge starting with `str[i+1]`. Add a new leaf j hanging off u, with edge label `str[i+1]`.
- [ ] Definition 9: Rule 2 case 2 (alternate / split)
  - Path `str[j..i]` ends mid-edge, the next character on that edge is some x != `str[i+1]`. Split the edge, creating a new internal node u right after `str[..i]`, then hang a new leaf j off u with label `str[i+1]`.
  - Goal: explain why the split is necessary and what the two resulting edges look like in terms of (start, end) tuples.
- [ ] Definition 8: Rule 3 extension (do nothing)
  - Path `str[j..i]` does not end at a leaf, and the next character on the path already is `str[i+1]`. The extended suffix `str[j..i+1]` is already implicitly present. No action.
  - Goal: explain why this is consistent with implicit suffix trees containing all suffixes implicitly.
- [ ] Worked example: build I_1 through I_4 for `abac` by hand
  - Reproduce the example on notes pages 9-13, calling out which rule applies at each (phase, extension).
  - Goal: be able to draw I_4 for `abac` from scratch and label every extension with its rule.
- [ ] Lab notes-Q3: append `$` to `abac` and run one more phase to obtain the regular suffix tree for `abac`.
- [ ] Naive Ukkonen worst case is O(n^3) (proof in notes pg 15)
  - Each extension: O(1) once you find the path, but you re-find the path from the root in O(i+1-j) characters. Sum gives O(i^2) per phase, then O(n^3) overall via 1^2 + 2^2 + ... + n^2.
  - Goal: reproduce the proof, including the closed form for the sum of squares.
- [ ] Lab notes-Q4: prove by induction
  - 1 + 2 + ... + n = n(n+1)/2.
  - 1 + 4 + ... + n^2 = n(n+1)(2n+1)/6.
- [ ] Impl: naive Ukkonen (lab04 step 2)
  - File target: `src/ukkonen.py`.
  - Implement Rule 1, Rule 2 (case 1), Rule 2 (case 2), Rule 3, with full root-to-extension-point traversal every time. No optimisations yet. This must reproduce the same tree as `naive_suffix_tree.py` for any input.
  - Goal: a passing test that compares this against the naive suffix tree on a battery of strings including `abac$`, `abcabxabcd$`, `abacabad$`, `mississippi$`.

---

## 4. Suffix links: first speedup

- [ ] Definition 10: suffix link
  - Internal node u with root-path `xα` has a suffix link pointing to internal node v with root-path `α`. Root links to itself.
  - Goal: given the implicit suffix tree of `abacabad`, list every suffix link.
- [ ] Lemma 1: a Rule 2 is never followed by a Rule 1 (within a phase)
  - Proof structure: a Rule 2 means `str[j..i]` doesn't end at a leaf, so a longer prefix containing it was already added earlier in the phase, so `str[j+1..i]` cannot end at a leaf either.
  - Goal: reproduce the proof.
- [ ] Lemma 2: subtree below the shorter path is at least as rich as below the longer path
  - The subtree below `str[j+1..i]` always contains the subtree below `str[j..i]`, but not vice versa.
  - Goal: reproduce the proof and explain why this is what enables a Rule 2 in extension j to be followed by a Rule 3 in extension j+1.
- [ ] Theorem 1: every internal node has an outgoing suffix link
  - Proof by induction on i. Base case I_1. Inductive step: a new internal node v is only created by a Rule 2 case 2 in some extension j. By Lemmas 1 and 2 the next extension j+1 is either Rule 2 (creates the node v's suffix link target w, points v to w) or Rule 3 (target is an existing node u, points v to u). The last extension of a phase never creates a new internal node.
  - Goal: reproduce the proof. Identify why this is the linchpin that makes the algorithm sound, not just fast.
- [ ] Definition 11: active node and remainder
  - Active node: the deepest internal node on the root-to-extension-point path. Remainder: the substring still to walk below the active node before reaching the extension point.
  - Goal: in any partial state, point at the active node and remainder.
- [ ] General extension procedure (notes pg 19)
  - From the active node u of extension j-1, follow its suffix link to v, walk down the remainder to the extension point of j, apply the rule. Special case: if u is the root, drop the first character of the remainder before walking.
  - Goal: write the three-line pseudocode block.
- [ ] Why suffix links alone don't yet give a speedup
  - You still walk the remainder character by character, so a single phase can still cost O(i) per extension. Worst case stays O(n^3).
  - Goal: state this in one sentence, motivating skip-counting next.

---

## 5. Skip-counting: down to O(n^2)

- [ ] The skip-count trick (Section 3.4)
  - When walking the remainder below the active node, only check the first character of each edge. If the remaining remainder length exceeds the edge length, jump straight to the receiving node and update active node + remainder. Otherwise step into the edge by the right amount.
  - Goal: hand-trace Example 6 in the notes (remainder `zabcdefghy`).
- [ ] Lab Q5: skip-counting trick illustration
  - Use the abstract figure to confirm what active node and remainder become after the extension.
  - Goal: state both updates in one sentence each.
- [ ] Why this is O(n^2)
  - Per extension, work is now proportional to the number of internal nodes traversed, not the number of characters. Each phase visits O(i) such nodes.
  - Goal: explain why we are not yet at O(n). What still costs too much?
- [ ] Impl: skip-count traversal (lab04 step 3)
  - Replace character-by-character traversal in your naive Ukkonen with skip-count from root. Still no other optimisations.

---

## 6. Space-efficient edge labels: O(n) space

- [ ] (startIndex, endIndex) representation (Section 3.5)
  - Already introduced in Section 1. Each edge stores two ints into `str`, both O(1).
- [ ] Theorem 2: O(n) space for fixed alphabet
  - At most 2n - 1 nodes (perfect binary upper bound for n leaves), at most 2n - 2 edges, edges are O(1), nodes are O(alphabet) = O(1).
  - Goal: reproduce the n leaves -> n-1 internal nodes geometric-sum bound.
- [ ] Lab Q7 (self-study): worst-case space for the suffix tree of `S[1..n]` over alphabet sigma.
  - Goal: state the bound and identify which factor depends on sigma vs n.
- [ ] Impl: ensure your Node/Edge data structures already use (start, end). Lab04 implementation step 1 wants this from the very first naive version.

---

## 7. Showstopper rule: skipping all leftover Rule 3s in a phase

- [ ] Lemma 3: a Rule 3 is followed by Rule 3s for the rest of the phase
  - Once `str[j..i+1]` is implicitly in the tree, the same is true of every shorter suffix of it, by Lemma 2.
  - Goal: reproduce the proof.
- [ ] Definition 12: showstopper rule
  - The first time Rule 3 fires in a phase, terminate the phase immediately.
  - Goal: justify why this is sound by quoting Lemma 3.
- [ ] Worked example: phase 7 of `abacabade` (Example 7 in notes)
  - Show that extensions 5, 6, 7 are all Rule 3 and would have been wasted work.
  - Goal: hand-trace it and explain what state must be remembered to resume the next phase correctly.
- [ ] Impl: showstopper logic (lab04 step 4)
  - On a Rule 3, store enough state (active node, remainder) to resume next phase, then break out of the phase loop.

---

## 8. Rapid leaf extension: skipping all Rule 1s with globalEnd

- [ ] Lemma 4: a Rule 1 in phase i is a Rule 1 in phase i+1, same j
  - Once leaf j is created, it stays a leaf, and the path to it stays `str[j..]`. Rule 1 just extends its edge.
  - Goal: reproduce the proof.
- [ ] Lemma 5: a Rule 2 in phase i is a Rule 1 in phase i+1, same j
  - The leaf j created by the Rule 2 will, in the next phase, be extended along its leaf edge.
  - Goal: reproduce the proof.
- [ ] Definition 13: last_j
  - The last extension index that was performed via Rule 2.
  - Goal: explain why every j <= last_j is a Rule 1 in phases after last_j was set.
- [ ] The globalEnd trick
  - Every leaf edge is stored as (startIndex, globalEnd) where globalEnd is a single mutable integer shared by all leaves. Incrementing globalEnd implicitly performs every Rule 1 for the new phase in O(1).
  - Goal: explain "once a leaf, always a leaf" in terms of why this trick is sound.
- [ ] Rapid leaf extension procedure (notes pg 27)
  - Each phase: globalEnd += 1, start explicit extensions from j = last_j + 1.
  - Goal: write the pseudocode.
- [ ] Lab Q2: rule transitions
  - Q2(a): for each rule used in extension j of phase i, list which rules are possible for the same j in phase i+1. Lemmas 4 and 5 give Rule 1 -> Rule 1, Rule 2 -> Rule 1. Lemma 6 below covers Rule 3.
  - Q2(b): for each rule, list which rules are possible for j+1 in the same phase. Lemmas 1 and 3 are the source.
  - Goal: produce a 4-row, 2-column table summarising all transitions.
- [ ] Impl: globalEnd + last_j (lab04 step 5)
  - Add globalEnd and last_j. Make Rule 1 implicit. Still traverse from root for every explicit extension.

---

## 9. Rule 3 bookkeeping

- [ ] Lemma 6: a Rule 3 in phase i is a Rule 2 or Rule 3 in phase i+1, same j
  - Same proof shape as Lemmas 4 and 5.
- [ ] Lab notes-Q5: prove Lemma 6.
- [ ] Three things a Rule 3 actually has to do (notes pg 28)
  - Append `str[i]` to the remainder so it goes from `str[k..i-1]` to `str[k..i]`.
  - If the previous extension created a new internal node v, point its dangling suffix link to the current active node u.
  - Apply the showstopper rule.
  - Goal: explain why "do nothing" is misleading, and which of these is the only one that actually mutates the tree.

---

## 10. Putting suffix links and active node together

- [ ] Suffix link traversal between phases.
  - After a Rule 2, follow the suffix link out of the active node. The receiving node is the new active node. If the active node is the root, manually drop the first character of the remainder.
  - Goal: trace the figure on notes pg 18.
- [ ] Lab Q3: alpha = c beta with both alpha and beta seen before (suffix link target already exists)
  - At the start of extension j, sketch the subtree below alpha and below beta (separately). Trace what happens after extension j, then j+1. Identify the source and target of the suffix link this scenario creates.
  - Goal: produce the four-step sketch and pinpoint the suffix link.
- [ ] Lab Q4: same setup but with two distinct following characters below beta
  - Redo all parts of Q3 for this richer scenario.
  - Goal: confirm whether the suffix link is created in the same place, and whether a new internal node is created during extension j+1.
- [ ] Impl: suffix link creation (lab04 step 6)
  - Whenever a Rule 2 case 2 creates a new internal node v, mark a "pending suffix link from v" and resolve it at the very next extension when the next active/parent node is known.
- [ ] Impl: active node optimisation (lab04 step 7)
  - Replace root-restart with: start from the active node, follow its suffix link, skip-count down the remainder. This is the final speedup.

---

## 11. Worst-case O(n) time: the headline result

- [ ] The full theorem: Ukkonen runs in O(n) time and space (notes pgs 30-31)
  - Time accounting:
    - n+1 phases. Rule 1s done by globalEnd: O(n) overall.
    - Rule 2s: at most n+1 total (one leaf per suffix), each O(1) from extension point.
    - Rule 3s: at most one per phase by showstopper, O(n) overall.
    - Suffix link traversals: at most one per explicit extension, at most 2(n+1) explicit extensions overall.
    - Skip-counting: total internal nodes traversed across the whole algorithm is bounded via a telescoping argument over the index sequence p_0 <= p_1 <= ... <= p_m, with m <= 2(n+1). So O(n).
  - Goal: reproduce the full argument, particularly the telescoping bound for skip-counting (this is the cleverest piece of the proof).
- [ ] Why this matters: linear suffix arrays and BWT
  - From `LEARNING_INTENTIONS.md`: a linear-time suffix tree gives a linear-time suffix array, which gives a linear-time BWT.
  - Goal: state the chain in one sentence.

---

## 12. Putting it together: end-to-end trace

- [ ] Section 3.10: full trace of `abacabad`
  - The notes give every phase, every extension, every variable update for AN, rem, last_j, GP. Walk this end-to-end.
  - Goal: be able to reproduce the figure for any phase by hand without peeking.
- [ ] Lab notes-Q6: do one more phase on `abacabad` to insert `$` and obtain the regular suffix tree.
- [ ] Lab Q6 (self-study): manually trace Ukkonen on `abaaba$`
  - Apply every trick.
  - Goal: produce a phase-by-phase, extension-by-extension log identical in style to Section 3.10.

---

## 13. Applications of suffix trees (Lab Q8 self-study)

These are why we built the tree. Assume the suffix tree of S is precomputed.

- [ ] Lab Q8(a): given pattern alpha[1..m]
  - Count occurrences of alpha in S: walk root-down spelling alpha; once you reach the end, the number of leaves in the subtree below is the count. O(m + occ) with a leaf count cached at each node, O(m) if you just want the count and pre-store leaf counts.
  - List all positions of alpha: same walk, then DFS the subtree collecting leaf labels. O(m + occ).
- [ ] Lab Q8(b): smallest substrings of S occurring exactly k times
  - Among internal nodes whose subtree leaf-count is exactly k, find those minimising depth (in characters from the root). O(n) DFS once leaf counts are computed.
- [ ] Lab Q8(c): longest repeated substring
  - The deepest internal node (in characters) whose subtree has >= 2 leaves. O(n).
- [ ] Lab Q8(d): lexicographically smallest suffix
  - Walk root to leaf always taking the lex-smallest outgoing edge. The leaf number is the answer. O(n).
- [ ] Lab Q8(e): suffix array of S
  - In-order DFS of the suffix tree (children visited in lex order), emitting leaf labels. The sequence of leaf numbers is the suffix array. O(n).
- [ ] Lab Q8(f): BWT of S
  - From the suffix array SA, BWT[i] = S[SA[i] - 1] (with wraparound). O(n) once you have SA.

---

## 14. Implementation milestones, summarised

A re-listing of the implementation steps (lab04 structured implementation), in order, each pointing at the section above where the theory lives.

- [x] Step 0: naive suffix trie (`src/naive_suffix_trie.py`).
- [ ] Step 1: Node and Edge with (startIndex, endIndex) labels (Section 1, Section 6).
- [ ] Step 2: naive O(n^2) suffix tree by direct insertion (Section 1).
- [ ] Step 3: naive Ukkonen with all four rules, root-restart, character traversal (Section 3).
- [ ] Step 4: skip-count traversal from root (Section 5).
- [ ] Step 5: showstopper rule (Section 7).
- [ ] Step 6: globalEnd + last_j (Section 8).
- [ ] Step 7: suffix link creation on Rule 2 case 2 (Section 10).
- [ ] Step 8: active-node optimisation, no more root restart (Section 10).
- [ ] Step 9: regression tests against the naive suffix tree on a corpus including `abac$`, `abacabad$`, `abaaba$`, `mississippi$`, random strings.