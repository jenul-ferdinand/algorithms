# Week 7: Fibonacci heaps - Learning Roadmap

Source material: `notes07.pdf` (21 pages), `seminar07.pdf`, `lab07.pdf`, `max_degree_bound_proof.pdf` (the formal max-degree proof).
Recommended reading: Fredman and Tarjan, _Fibonacci Heaps and Their Uses in Improved Network Optimization Algorithms_, J. ACM 34(3) 596-615 (1987); CLRS, _Introduction to Algorithms_, ch. 19.

Legend: `[ ]` concept / theorem / proof to learn. `[ ] Lab Qx`: question from `lab07.pdf`. `[ ] Lab notes-Qx`: question embedded in `notes07.pdf`. `[ ] Impl`: implementation exercise. Goals describe what "done" looks like.

The order is the order to learn in. Each section assumes everything above it.

---

## 1. Priority queues

- [ ] What a priority queue is
    - An abstract data type maintaining a set with a key per element. Supports insert, min (or max), extract-min, decrease-key. Used for scheduling, sorting (heapsort), and inside Prim's, Dijkstra's, etc.
    - Goal: list the operations and explain why ordering by key is not an equivalence relation (no symmetry).
- [ ] Heaps as the canonical implementation
    - "Heap" and "priority queue" are often used interchangeably. The rest of the topic is about heap variants.
    - Goal: state in one sentence why heaps fit priority queues (cheap min + cheap insert).

---

## 2. Binary heaps (review)

- [ ] Definition 1: binary heap
    - Structure: complete binary tree (every level full except possibly the last, which fills left to right). Order (min-heap): each node's key <= each child's key.
    - Goal: state both properties; identify which is needed for correctness vs which is needed for the array trick.
- [ ] Array representation
    - Node at array index i has children at 2i and 2i + 1, parent at floor(i/2). Possible because of the structural completeness.
    - Goal: hand-verify the array `[A,B,E,F,H,K,L,M,T,X]` against the tree on notes pg 3.
- [ ] Operation costs (table on notes pg 3)
    - make-new-heap: O(1). min: O(1). extract-min: O(log N). decrease-key: O(log N). delete: O(log N). insert: O(log N) worst, O(1) amortised.
    - Goal: write the table from memory; argue each bound (sift-up / sift-down).
- [ ] Why merge is slow on binary heaps
    - Two heaps of size N each must be combined into a 2N array. Just copying is O(N). Merging without preserving the heap property is fine; restoring it via heapify is O(N) too. So merge is O(N).
    - Goal: argue why the array representation is the very thing that makes merge slow, motivating an explicit-pointer mergeable heap.

---

## 3. Fibonacci heaps: overview

- [ ] Why Fibonacci heaps exist
    - To make Dijkstra's run in O(|E| + |V| log |V|) instead of O((|E| + |V|) log |V|). The win comes from an O(1) amortised decrease-key.
    - Goal: state the Dijkstra speedup goal in one sentence.
- [ ] Definition 3: Fibonacci heap
    - A forest of rooted trees, each tree min-heap ordered, each tree "almost binomial" (binomial tree with at most one child missing per node). Plus an `H.min` pointer to the global minimum, plus a "marked" bit on each non-root node.
    - Goal: state the order property, the structure constraint, and the bookkeeping (H.min + marks).
- [ ] Lazy evaluation philosophy
    - Insert and merge defer all consolidation work to extract-min. Decrease-key cuts and promotes nodes lazily, then defers cleanup. The amortised analysis shows this all balances out.
    - Goal: explain the tradeoff: amortised wins on decrease-key cost some work each extract-min.

---

## 4. Binomial trees (non-examinable supplement)

- [ ] Definition 2: B_k recursive
    - B_0 is a single node. B_k is two B_{k-1} trees with one as a subtree of the other's root.
    - Goal: draw B_0 through B_3.
- [ ] Five properties of B_k
    - Contains 2^k nodes. Has height k. Root has k children. Removing root yields B_{k-1}, B_{k-2}, ..., B_0. Number of nodes at depth d is the binomial coefficient C(k, d).
    - Goal: verify properties 1-4 against your B_3 drawing.
- [ ] Why this matters for Fibonacci heaps
    - Fibonacci heap trees are binomial trees that have lost at most one child per node (due to decrease-key cuts). The "Fibonacci" name comes from the size lower bound F_{d+2} on a tree of root-degree d (see Section 11).
    - Goal: state the connection: F-heap trees are "binomial-with-cuts".

---

## 5. Representing Fibonacci heaps

- [ ] Node structure (notes pg 6)
    - Per node x: key, payload, degree, mark, parent, children (pointer to any one child), leftSibling, rightSibling. Siblings form a circular doubly linked list. Each level (root list and each set of siblings) is a circular DLL.
    - Goal: list every field and justify each one.
- [ ] Why circular DLLs everywhere
    - Allows O(1) splice, O(1) insert anywhere, O(1) detach. These primitives are what make insert and merge O(1).
    - Goal: explain why an array-based representation is incompatible with O(1) merge.
- [ ] H.min and the root list
    - The root list is a circular DLL containing all tree roots. H.min points to the root with the smallest key.
    - Goal: explain why H.min is needed (no other invariant tells us which root is the min).

---

## 6. Easy operations: min, merge, insert

- [ ] min: O(1)
    - Return H.min.key.
    - Goal: write the one-line pseudocode.
- [ ] merge: O(1)
    - Splice the two root lists into one circular DLL by updating exactly four sibling pointers. Set new H.min to the smaller of the two old H.mins.
    - Goal: write the four-pointer-update pseudocode (notes pg 9). Trace it on notes example 4.
- [ ] insert: O(1)
    - Make a new singleton heap with the new node, then merge into H. Equivalently, splice the new node into the root list and update H.min if needed.
    - Goal: write the pseudocode that calls merge.

---

## 7. extract-min

- [ ] Three steps (notes pg 10)
    - 1. Remove H.min from the root list. Its children become orphans. Form them into a temporary heap H_1 and merge into H. Update parent pointers to None.
    - 2. Set H.min temporarily to any other root (e.g. H.min's old right sibling) so we can traverse the root list.
    - 3. Consolidate: merge same-degree trees in the root list until at most one tree of any given degree remains.
- [ ] Consolidation via auxiliary array A
    - Walk the root list once. For a node x of degree d: if A[d] is empty, store x there. Otherwise merge A[d] with x (smaller key becomes parent), clear A[d], and re-examine the merged tree's new degree d+1, etc.
    - Goal: trace the worked example on notes pgs 12-15. Track the auxiliary array at each step.
- [ ] Edge cases during consolidation
    - The traversal must use a fixed start/last node, set before mutation, because mutating sibling pointers mid-walk breaks naive iteration.
    - When a marked root becomes a non-root child during a merge, unmark it.
    - After the walk, scan A to find the new H.min.
    - Goal: list these three subtleties from memory.
- [ ] Tree-merge primitive (notes pg 16)
    - Lab notes-Q1: write pseudocode to merge two trees of the same degree given the F-heap representation. Carefully sequence the pointer updates so nothing is overwritten before it is read.
    - Goal: produce the pseudocode (3-4 lines): make the smaller-key root the parent, append the larger-key root to its child list, increment degree.
- [ ] Worst case vs amortised
    - Worst case O(N): the root list can hold N nodes if you only ever inserted. Amortised O(log N): consolidation reduces the root list to at most log_phi(N) trees.
    - Goal: state both bounds. The full amortised analysis is wk08 territory (potential function), but acknowledge it now.

---

## 8. decrease-key

- [ ] Why we cannot bubble up
    - Bubbling would be O(log N) (tree depth). To get O(1) amortised, we cut the offending node and promote its subtree to the root list.
    - Goal: state the design choice in one sentence.
- [ ] Case 1: heap property not violated
    - x.key still >= x.parent.key. Do nothing structural. O(1).
    - Goal: trace the worked example on notes pg 17 (decrease 35 to 30).
- [ ] Case 2a: violated, parent unmarked
    - Cut x's subtree, promote to root list, unmark x, mark the parent. O(1).
    - Goal: trace the example on notes pg 18 (decrease 46 to 15).
- [ ] Case 2b: violated, parent marked (cascading cut)
    - Cut x as in 2a, then recursively cut and promote the parent because it has now lost a second child. Cascades up until reaching an unmarked node (which gets marked) or a root (no marking).
    - Goal: trace the example on notes pgs 18-19 (decrease 35 to 5, two-step cascade).
- [ ] Subtleties
    - Roots are never marked. If a marked node is cut and promoted to the root, unmark it. H.min may need updating if the new root has the smallest key.
    - Goal: list these from memory.
- [ ] O(1) amortised, O(log N) worst case
    - Worst case is the depth of a cascade, which is O(log N) since the tree is "almost binomial". Amortised O(1) because each cascade step pays for one mark created earlier.
    - Goal: state the bound. The proof is wk08.

---

## 9. delete

- [ ] Reduction to decrease-key + extract-min
    - decrease-key(x, -infinity) makes x the new H.min; extract-min(H) removes it. Total O(log N) amortised.
    - Goal: write the two-line pseudocode.
- [ ] Why -infinity (or any small enough sentinel) works
    - Anything strictly less than every key in the heap suffices. -infinity is a convenient choice for integer keys.
    - Goal: explain why deleting an arbitrary x can be reduced to deleting the minimum.

---

## 10. Why mark nodes?

- [ ] The two competing goals (notes pg 21)
    - Need 1: every tree of root-degree d has size at least exponential in d. This bounds the number of trees in the root list after consolidation, keeping extract-min cheap.
    - Need 2: the number of cascading cuts in any sequence of operations must be bounded by the number of decrease-key/delete calls. Keeps decrease-key amortised O(1).
    - Goal: state both needs and explain how marking after losing one child (and cutting after losing two) balances them.
- [ ] Why "after two" and not "after one"
    - Cutting after one loss would invalidate need 1: trees would shrink too aggressively, breaking the size lower bound.
    - Goal: argue this in one paragraph.

---

## 11. The maximum degree bound (`max_degree_bound_proof.pdf`)

- [ ] Lab Q6: prove sum from i=0 to n of F_i = F_{n+2} - 1 by induction
    - Base: n = 0 gives 0 = 1 - 1.
    - Step: assume true at n, then sum to n+1 = F_{n+2} - 1 + F_{n+1} = F_{n+3} - 1 by the Fibonacci recurrence.
    - Goal: write both steps.
- [ ] Lab Q7: prove F_{n+2} >= phi^n by induction, where phi = (1 + sqrt 5)/2
    - Base: F_2 = 1 >= phi^0 = 1.
    - Step: F_{n+3} = F_{n+2} + F_{n+1} >= phi^n + phi^{n-1} = phi^{n-1}(phi + 1) = phi^{n-1} * phi^2 = phi^{n+1}, using phi^2 = phi + 1.
    - Goal: produce the proof, calling out the algebraic identity phi^2 = phi + 1.
- [ ] Theorem 1: size(x) >= F_{degree(x) + 2} for any node x
    - Proof by induction on tree depth (bottom-up). Base: degree 0 leaf has size 1 = F_2. Step: combine the inductive hypothesis on each child c_i (size(c_i) >= F_{degree(c_i)+2}) with Lemma 1 below to get size(x) >= 1 + F_0 + F_1 + sum from i=2 to d of F_i = 1 + (F_{d+2} - 1) = F_{d+2}.
    - Goal: reproduce the proof, including the partial-sum identity from Lab Q6.
- [ ] Lemma 1: degree(c_i) >= i - 2 for i >= 2
    - When c_i became a child of x, x already had at least i - 1 children, so c_i had degree at least i - 1 at that moment (merges require equal degrees). Since c_i can have lost at most one child since then (the F-heap structural invariant), degree(c_i) >= i - 2.
    - Goal: reproduce the proof.
- [ ] Lab Q8 / Lab notes-Q2: corollary, degree(x) = O(log N)
    - From Theorem 1: N >= size(x) >= F_{degree(x)+2} >= phi^{degree(x)} (by Q7). Take log_phi of both sides: degree(x) <= log_phi(N) = O(log N).
    - Goal: produce the corollary; state log base is phi (~ 1.618).

---

## 12. Putting it together: summary and Dijkstra

- [ ] Summary table (notes pg 21)
    - make-new-heap: O(1) both. min: O(1) both. extract-min: O(log N) amortised vs O(log N) worst. merge: O(1) vs O(N). decrease-key: O(1) amortised vs O(log N). delete: O(log N) amortised vs O(log N). insert: O(1) vs O(log N) worst, O(1) amortised.
    - Goal: write the table from memory.
- [ ] Lab Q1: Dijkstra running time in terms of T_extract-min and T_decrease-key
    - The algorithm performs |V| extract-min calls (one per vertex) and at most |E| decrease-key calls (one per edge relaxation). Total: O(|V| * T_extract-min + |E| * T_decrease-key).
    - With binary heap (T_extract-min = T_decrease-key = log N): O((|V| + |E|) log V).
    - With Fibonacci heap (T_extract-min = log V amortised, T_decrease-key = O(1) amortised): O(|V| log V + |E|).
    - Goal: produce the parameterised expression and instantiate both heap types.
- [ ] Lab Q4: worst-case time complexities of insert and extract-min
    - insert: O(1) worst case (just splice into root list).
    - extract-min: O(N) worst case (root list could contain N nodes if only inserts have happened). But O(log N) amortised.
    - Goal: state both with clear distinction worst-case vs amortised.

---

## 13. Hands-on tracing exercises

- [ ] Lab Q2: insert {3, 8, 10, 11, 1, 12, 2, 17}, then extract-min
    - Each insert is a splice into the root list. After 8 inserts, root list contains 8 trees of degree 0, with H.min = 1. Extract-min removes 1 and triggers consolidation.
    - Goal: draw the heap before extract-min and after consolidation. Identify the resulting tree shapes.
- [ ] Lab Q3: extract-min on the given heap
    - Heap drawn on lab pg 1 with H.min = 7 and several roots of varying degree.
    - Goal: produce the post-extract-min heap step by step (remove 7, merge orphans into root list, consolidate).
- [ ] Lab Q5: sequence of decrease-key operations + extract-min
    - 5(a) decrease-key 45 to 40. 5(b) 40 to 12. 5(c) 35 to 1. 5(d) extract-min.
    - Goal: draw the heap after each step. Identify which case (1, 2a, 2b) each decrease-key falls into.

---

## 14. Implementation milestones, summarised

A re-listing of the implementation steps in order. New files live in `src/`.

- [ ] Step 1: data structures.
    - `src/fib_node.py` (or in the same file): Node class with key, payload, degree, mark, parent, leftSibling, rightSibling, child. Doubly-linked circular DLL helpers (splice, detach).
- [ ] Step 2: trivial operations.
    - `src/fib_heap.py`: FibHeap class with min(), make-new-heap, insert(), merge(other). All O(1).
- [ ] Step 3: extract-min.
    - Includes the consolidation routine with the auxiliary array A indexed by degree. Test against a binary-heap reference for correctness on insert + extract sequences.
- [ ] Step 4: decrease-key with cascading cuts.
    - Implement the three cases. Mark/unmark logic, H.min update, root-list reinsertion.
- [ ] Step 5: delete.
    - Wraps decrease-key(x, -infinity) followed by extract-min.
- [ ] Step 6 (Lab Impl Q1): full test battery.
    - Property-based tests: build random sequences of operations, mirror them on a sorted list, assert equivalence of min and extract-min outputs.
- [ ] Step 7 (stretch): Dijkstra using the Fibonacci heap.
    - Compare empirical times against a binary-heap-based Dijkstra on dense graphs to observe the |V| log V vs (|V| + |E|) log V difference.
