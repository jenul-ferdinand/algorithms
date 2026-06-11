# Week 8 Moodle Quiz

Topic: amortized analysis.

## Questions

1. Amortized analysis guarantees that every individual operation runs in `O(1)` time.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

Amortized analysis bounds the average cost over a sequence. One operation can still be expensive.

</details>

---

2. Summing worst-case costs of each operation always yields a tight bound for a sequence of operations.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

It is always an upper bound, but often too pessimistic. The binary counter is the classic example.

</details>

---

3. In aggregate analysis, the amortized cost is obtained by dividing the worst-case cost of a single operation by `n`.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

Aggregate analysis bounds the total cost of `n` operations, then divides that total by `n`.

</details>

---

4. The worst-case cost of a single increment in a `k`-bit binary counter is `Theta(k)`.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

In the worst case, all `k` bits are `1`, so the increment flips every bit.

</details>

---

5. The total cost of `n` increments in a binary counter is `Theta(nk)`.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

Across `n` increments, bit `b` flips only about `n / 2^b` times, so the total number of flips is at most `2n`.

</details>

---

6. In the accounting method, credits stored during operations can be used to pay for future operations.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

Cheap operations can overpay and store credit, which later pays for expensive operations.

</details>

---

7. If the accounting method never goes into debt, then total actual cost is bounded by total amortized cost.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

Non-negative stored credit means the amortized charges have always paid for all actual work so far.

</details>

---

8. The potential function must always strictly increase after every operation.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

Potential may increase, decrease, or stay the same. What matters is that the total amortized cost upper-bounds the total actual cost.

</details>

---

9. For amortized cost to upper bound actual cost, it is sufficient that `Phi(D_n) - Phi(D_0) >= 0`.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

Since `sum amortized = sum actual + Phi(D_n) - Phi(D_0)`, a non-negative final potential difference makes amortized cost an upper bound.

</details>

---

10. The potential function `Phi(H) = nTrees(H) + 2 * nMarked(H)` assigns equal weight to trees and marked nodes.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

Trees have coefficient `1`, while marked nodes have coefficient `2`.

</details>

---

11. Which statement best describes amortized analysis?

- [ ] a. It averages over all possible inputs
- [ ] b. It averages over a sequence of operations
- [ ] c. It assumes uniform probability
- [ ] d. It bounds best-case performance

<details>
<summary>Answer</summary>

b. It averages over a sequence of operations.

Unlike average-case analysis, amortized analysis does not require a probability distribution over inputs.

</details>

---

12. What is the key step in aggregate analysis?

- [ ] a. Analyzing each operation independently
- [ ] b. Bounding total cost over `n` operations
- [ ] c. Assigning credits to operations
- [ ] d. Choosing a potential function

<details>
<summary>Answer</summary>

b. Bounding total cost over `n` operations.

After bounding the sequence cost `T(n)`, the amortized cost per operation is `T(n) / n`.

</details>

---

13. What determines the cost of an increment in a binary counter?

- [ ] a. Number of bits set to `0`
- [ ] b. Runlength of trailing `1`s
- [ ] c. Position of most significant bit
- [ ] d. Total number of bits

<details>
<summary>Answer</summary>

b. Runlength of trailing `1`s.

The increment flips each trailing `1` to `0`, then possibly flips the next `0` to `1`.

</details>

---

14. Why is `lambda = 2` sufficient in the accounting method for the binary counter?

- [ ] a. Each bit flips twice
- [ ] b. One coin pays for set and one is stored for unset
- [ ] c. It minimizes total cost
- [ ] d. It ensures constant worst-case cost

<details>
<summary>Answer</summary>

b. One coin pays for set and one is stored for unset.

When a bit becomes `1`, one coin pays now and one coin is saved to pay when that bit later becomes `0`.

</details>

---

15. What happens if the accounting method runs out of credit?

- [ ] a. Analysis fails
- [ ] b. Runtime increases
- [ ] c. Operations stop
- [ ] d. Potential decreases

<details>
<summary>Answer</summary>

a. Analysis fails.

The proof relies on never going into debt. Negative credit means the chosen amortized charges were too small.

</details>

---

16. What does the term `Phi(D_i) - Phi(D_{i-1})` represent?

- [ ] a. Actual cost
- [ ] b. Future cost
- [ ] c. Change in stored credit
- [ ] d. Worst-case cost

<details>
<summary>Answer</summary>

c. Change in stored credit.

In the potential method, potential is stored credit encoded as a function of the data-structure state.

</details>

---

17. Which is a valid property of a potential function?

- [ ] a. Must always be zero
- [ ] b. Must always decrease
- [ ] c. Can be chosen flexibly
- [ ] d. Must equal actual cost

<details>
<summary>Answer</summary>

c. Can be chosen flexibly.

The function is chosen to make the analysis work, as long as the final potential condition gives a valid upper bound.

</details>

---

18. What is the potential function used for the binary counter?

- [ ] a. Number of zeros
- [ ] b. Number of bits
- [ ] c. Sum of bits set to `1`
- [ ] d. Position of MSB

<details>
<summary>Answer</summary>

c. Sum of bits set to `1`.

Equivalently, `Phi(A)` is the number of `1` bits currently stored in the counter.

</details>

---

19. Why is the coefficient `2` used for marked nodes in `Phi(H)`?

- [ ] a. To simplify notation
- [ ] b. To eliminate dependence on `m`
- [ ] c. To reduce tree count
- [ ] d. To balance trees

<details>
<summary>Answer</summary>

b. To eliminate dependence on `m`.

In a cascading cut with `m` promoted nodes, the `2 * nMarked` term drops enough to pay for the cascade, leaving `O(1)` amortized cost.

</details>

---

20. What dominates the true cost of `extract-min`?

- [ ] a. Number of inserts
- [ ] b. Maximum degree and number of trees
- [ ] c. Number of marked nodes
- [ ] d. Heap size only

<details>
<summary>Answer</summary>

b. Maximum degree and number of trees.

`extract-min` promotes the old minimum's children and consolidates the root list, so the cost depends on max degree and root-list size.

</details>
