# Week 8: Amortized analysis - Learning Roadmap

Source material: `seminar08.pdf` (35 slides), `lab08.pdf`.
Note: there is no `notes08.pdf` for this week. The seminar slides serve as the primary written reference.
Recommended reading: Cormen et al. _Introduction to Algorithms_, ch. 17; Robert E. Tarjan, _Amortized Computational Complexity_, SIAM J. Algebraic and Discrete Methods 6(2), 1985.

Legend: `[ ]` concept / theorem / proof to learn. `[ ] Lab Qx`: question from `lab08.pdf`. `[ ] Impl`: implementation/proof-writeup exercise. Goals describe what "done" looks like.

The order is the order to learn in. Each section assumes everything above it.

---

## 1. Why amortized analysis exists

- [x] The motivation
    - Routine use of any data structure is a sequence of operations, not a single one. We want a realistic bound on the cost of the whole sequence.
    - Goal: state in one sentence why bounding the sequence cost is the right object.
- [x] Why neither worst-case nor best-case nor average-case suffices
    - Worst-case per-op summed over n: too pessimistic (e.g. binary counter sequences rarely hit the worst case every step).
    - Best-case: too optimistic.
    - Average-case: requires a probability distribution over sequences, which is non-trivial to specify and often unrealistic.
    - Goal: explain the gap each method fails to close.
- [x] What amortized analysis provides
    - A per-operation cost averaged over any sequence of operations. Sometimes provably smaller than the worst-case per-op cost.
    - Goal: state Tarjan's definition: "to average the running times of operations in a sequence over that sequence."

---

## 2. Three methods

- [x] Aggregate method (mathematician's view)
    - Bound the total cost T(n) of any sequence of n operations directly. Amortised cost per op = T(n)/n.
    - Goal: state the procedure.
- [x] Accounting method (banker's view)
    - Assign each operation an amortised cost (an allocation of "coins"). Use surplus from cheap ops as credit to pay for expensive ops. Show the credit balance never goes negative.
    - Goal: state the procedure and the invariant (total actual cost <= total amortised cost iff credit stays non-negative).
- [x] Potential method (physicist's view)
    - Define a potential function Phi mapping each data-structure state D_i to a real number. The amortised cost of operation i is a_i = tau_i + Phi(D_i) - Phi(D_{i-1}), where tau_i is the actual cost.
    - Summing telescopes: sum of a_i = sum of tau_i + Phi(D_n) - Phi(D_0). If Phi(D_0) = 0 and Phi(D_n) >= 0, the amortised total upper-bounds the actual total.
    - Goal: derive the telescoping identity.
- [x] Why the three are equivalent
    - All three yield valid amortised bounds on the same sequence. The accounting method handles integer credits naturally; the potential method generalises to fractional credits and is the more flexible workhorse for tight bounds.
    - Goal: state the equivalence in one sentence.

---

## 3. The k-bit binary counter (running example)

- [x] Definition of the data structure
    - Boolean array A[0..k-1] storing a number in binary, A[0] is the lowest-order bit. Single operation `increment` adds 1 mod 2^k.
    - Goal: write the increment pseudocode (slide 10): set b = 0, while b < k and A[b] == 1: A[b] = 0; b += 1; if b < k: A[b] = 1.
- [x] Per-operation worst-case cost
    - True cost of one increment = (number of trailing 1s before the first 0) + 1. Worst case is k (all bits flip from 1...1 to 0...0). Naive bound on n increments is O(nk).
    - Goal: tabulate the runlengths for the first 16 counter values from slide 12.

---

## 4. Aggregate analysis on the binary counter

- [x] Bit-flip frequency by position
    - A[0] flips on every increment: n/1 flips.
    - A[1] flips every other increment: n/2 flips.
    - A[b] flips every 2^b-th increment: n/2^b flips.
    - Total flips across n increments: T(n) = n + n/2 + n/4 + ... <= 2n.
    - Goal: derive the geometric-series bound.
- [x] Amortised cost per increment
    - T(n)/n <= 2, so amortised cost is O(1).
    - Goal: contrast with the naive O(k) worst-case per-op bound.
- [x] Lab Q1(a): aggregate amortised cost of increment
    - Goal: reproduce the geometric series argument and conclude O(1) amortised.

---

## 5. Accounting analysis on the binary counter

- [x] The credit allocation rule
    - Charge 2 coins each time you set a bit (line 6 of the pseudocode). 1 coin pays for the actual write 0 -> 1; the other coin is stored as credit on that bit.
    - Each unset (line 3) is paid for by the credit stored when that bit was set. So unsets are free in amortised terms.
    - Goal: state the rule and verify the credit invariant: every set bit carries exactly 1 coin of stored credit.
- [x] Amortised cost per increment is O(1)
    - Each increment sets at most one bit (line 6 runs at most once). It pays 2 coins. Unsets are free. Hence amortised <= 2 = O(1).
    - Goal: state the bound and explain why no operation goes into debt.
- [x] Lab Q1(b): accounting amortised cost of increment
    - Goal: write the proof, identifying the credit invariant explicitly.

---

## 6. Potential analysis on the binary counter

- [x] The potential function
    - Phi(A_i) = bitsum(A_i) = number of 1-bits in the counter after the i-th increment. Phi(A_0) = 0; Phi >= 0 always; max k.
    - Goal: state the function and verify the boundary conditions.
- [x] Amortised cost derivation
    - Suppose operation i unsets l trailing 1s (turning them to 0) and possibly sets the next higher bit. True cost tau_i <= l + 1.
    - Potential change: Phi(A_i) - Phi(A_{i-1}) = -l + (1 if a higher bit was set else 0) <= -l + 1.
    - Amortised: a_i = tau_i + Phi(A_i) - Phi(A_{i-1}) <= (l + 1) + (-l + 1) = 2 = O(1).
    - Goal: produce this calculation step by step. Identify which case (b < k vs b == k) yields the tight bound.
- [x] Sequence-level bound
    - sum a_i = sum tau_i + Phi(A_n) - Phi(A_0) >= sum tau_i (since Phi(A_n) >= Phi(A_0) = 0). So total actual cost <= total amortised cost <= 2n = O(n).
    - Goal: state the bound and identify why Phi(A_0) = 0 and Phi(A_n) >= 0 are required.
- [x] Lab Q1(c): potential amortised cost of increment
    - Goal: write the proof and state the chosen Phi explicitly.

---

## 7. Application: dynamic array append

- [ ] The data structure
    - Starts empty with capacity 0. First append creates capacity 1. When full, doubling allocates a new array of double capacity, copies all elements, then appends.
    - Capacity sequence: 0, 1, 2, 4, 8, 16, ...
    - Goal: state the resize policy and explain why doubling (rather than +1 or +k) is what makes amortisation work.
- [ ] Per-operation worst case
    - Most appends cost 1 (just write to the next slot). Resize appends cost capacity_old + 1 = 2^k + 1 (copy + write). Worst case is O(n) for a single append, hence naively O(n^2) for n appends.
    - Goal: identify the resize indices in [1..n] (powers of 2).
- [ ] Lab Q3(a): aggregate analysis
    - Total cost: each plain append contributes 1, each resize at capacity 2^k contributes 2^k for the copy plus 1 for the new element. Sum: n + (1 + 2 + 4 + ... + 2^{floor(log2 n)}) <= n + 2n = 3n.
    - Amortised per append: 3n/n = O(1).
    - Goal: produce the geometric-series argument.
- [ ] Lab Q3(b): accounting analysis
    - Charge each append 3 coins. 1 pays for the immediate write. The other 2 are credit: 1 stored on the new element (pays for moving it during the next resize) and 1 stored on the slot in the upper half of the array (pays for moving the corresponding lower-half element during resize).
    - Equivalently: at the moment of resize from capacity c to 2c, the c "upper half" elements collectively carry c units of credit, exactly enough to pay for copying the c lower-half elements.
    - Goal: write the proof and verify the invariant before and after a resize.
- [ ] Lab Q3(c): potential analysis with Phi(A_i) = 2 * size(A_i) - capacity(A_i)
    - Boundary check: Phi(A_0) = 0 (size = capacity = 0). After any state, size >= capacity / 2 (the array is at least half-full after every doubling), so Phi >= 0.
    - Append without resize: size increases by 1, capacity unchanged. Delta Phi = 2. Actual cost tau = 1. Amortised a = 1 + 2 = 3.
    - Append with resize from capacity c to 2c: size goes from c to c + 1, capacity from c to 2c. Delta Phi = 2(c + 1) - 2c - (2c - c) = 2 - c. Actual cost tau = c + 1 (copy c, write 1). Amortised a = (c + 1) + (2 - c) = 3.
    - Conclusion: amortised cost is exactly 3 in both cases.
    - Goal: produce both case analyses and conclude O(1) amortised.
- [ ] Why this Phi was chosen
    - Phi is a linear combination lambda_1 * size + lambda_2 * capacity. Pick lambda_1, lambda_2 so that resize Delta Phi exactly cancels the c copy cost. Solving: lambda_1 = 2, lambda_2 = -1.
    - Goal: outline the derivation (non-examinable, but useful for intuition).

---

## 8. Application: Fibonacci heaps via the potential method

- [x] The potential function (slide 29)
    - Phi(H) = nTrees(H) + 2 * nMarked(H), where nTrees counts roots in the root list and nMarked counts marked non-root nodes.
    - Goal: state the function and compute it for the example heap on slide 29 (5 + 2*3 = 11).
- [x] Why these two terms
    - extract-min cost depends on the size of the root list (nTrees), and decrease-key cost depends on the number of cascading cuts (which depend on nMarked). Combining both into one potential lets a single Phi balance both operations.
    - Goal: explain the link between each operation's cost and one of the two terms.
- [x] Why the coefficient on nMarked is 2 (not 1)
    - A cascading cut both unmarks a node and creates a new tree. The 2 ensures Phi decreases by enough to cancel the cost of cutting.
    - Goal: derive the constant by trying lambda_1 = lambda_2 = 1 and seeing that decrease-key fails to be O(1) amortised under that choice.
- [x] Lab Q2(a): amortised cost of insert is O(1)
    - True cost: O(1). Phi change: nTrees += 1, nMarked unchanged. Delta Phi = 1.
    - Amortised: 1 + 1 = 2 = O(1).
    - Goal: produce the proof.
- [x] Lab Q2(b): amortised cost of extract-min is O(log N)
    - Pre-extract Phi = nTrees + 2 * nMarked. Post-extract: at most degree_max + 1 trees in the root list (after consolidation), and nMarked can only decrease.
    - True cost: O(degree_max + nTrees) (degree_max for orphan reinsertion, nTrees for consolidation traversal).
    - Amortised: O(degree_max) = O(log N) since degree_max <= log_phi(N) by wk07's theorem.
    - Goal: produce the calculation, importing the wk07 max-degree bound.
- [x] Lab Q2(c): amortised cost of decrease-key is O(1)
    - Suppose m nodes are promoted to the root (one cut + (m-1) cascading cuts). True cost: O(m).
    - Phi change: nTrees increases by m. nMarked decreases by at least m - 1 (the m - 1 nodes whose marks triggered cascade) and increases by at most 1 (the final unmarked parent that now gets marked).
    - 2 * Delta nMarked <= 2 * (-(m - 1) + 1) = -2m + 4.
    - Amortised: m + m + (-2m + 4) = 4 = O(1).
    - Goal: produce the calculation. The key is that the cost of cascading cuts is paid out of the potential built up by previous mark operations.
- [ ] Why Fibonacci heaps were the historical motivation
    - Tarjan and Sleator's amortised analysis was developed in part to formalise the O(1) decrease-key bound that makes Fibonacci heaps useful in Dijkstra's. This week is the analysis that wk07 deferred.
    - Goal: state the connection.

---

## 9. Putting it together

- [ ] When to reach for which method
    - Aggregate: simplest when the sequence cost has a clean closed form (binary counter, dynamic array append).
    - Accounting: best when the per-operation credit story is intuitive (each new element prepays its own copy cost).
    - Potential: most flexible. Required when the credit allocation depends on global state (Fibonacci heap nTrees + nMarked).
    - Goal: write a one-sentence selection guide.
- [ ] Common potential function shapes
    - bitsum (binary counter): counts of "expensive" features.
    - 2 * size - capacity (dynamic array): linear combination tuned so Delta Phi cancels resize cost.
    - nTrees + 2 * nMarked (F-heap): linear combination of structural features that operations alter.
    - Goal: identify the pattern: choose features whose change tracks the operation's cost.

---

## 10. Implementation and writeup milestones, summarised

This week is primarily proof writeups. Empirical simulators are optional but help build intuition.

- [x] Step 1 (Lab Q1): write up all three amortised analyses for the k-bit binary counter.
    - Files: `lab/binary_counter_aggregate.md`, `lab/binary_counter_accounting.md`, `lab/binary_counter_potential.md`.
- [x] Step 2 (Lab Q3): write up all three amortised analyses for dynamic-array append.
    - Files: `lab/dyn_array_aggregate.md`, `lab/dyn_array_accounting.md`, `lab/dyn_array_potential.md`.
- [x] Step 3 (Lab Q2): write up the Fibonacci heap amortised analyses for insert, extract-min, decrease-key under Phi(H) = nTrees + 2 * nMarked.
    - File: `lab/fib_heap_amortised.md`.
- [ ] Step 4 (optional simulator): `src/binary_counter.py`. Simulate n increments, count actual bit-flips, plot total cost vs n. Confirm the empirical slope is 2 (not k).
- [ ] Step 5 (optional simulator): `src/dynamic_array.py`. Simulate n appends with doubling, count actual writes (writes to new slot + copies during resize), confirm total cost is roughly 3n.
- [ ] Step 6 (stretch, depends on wk07 implementation): instrument the wk07 Fibonacci heap to track nTrees and nMarked over time. Run a sequence of inserts + extract-mins + decrease-keys, plot Phi(H) over time, verify the amortised cost of each operation matches the predicted bound on average.
