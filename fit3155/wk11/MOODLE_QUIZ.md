# Week 11 Moodle Quiz

Topic: Hungarian algorithm.

## Questions

1. In a bipartite graph `G = (V, E)`, every cycle must contain an even number of edges.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

A cycle in a bipartite graph must alternate between the two partitions, so it must return after an even number of edges.

</details>

---

2. A matching in a bipartite graph may contain two edges sharing the same endpoint provided the shared endpoint belongs to different partitions.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

In a matching, no two chosen edges may share any endpoint.

</details>

---

3. A perfect matching in an `N x N` assignment problem always contains exactly `N` edges.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

Each of the `N` agents is matched to exactly one of the `N` tasks, so the perfect matching has `N` matched pairs.

</details>

---

4. Subtracting the same constant from every entry of a single row in the Hungarian algorithm changes the set of optimal assignments.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

Every perfect assignment uses exactly one entry from that row, so every assignment cost shifts by the same amount.

</details>

---

5. For dual variables `u_i` and `v_j` in the assignment problem, the feasibility condition `u_i + v_j <= c_ij` must hold for every pair `(i, j)`.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

This is the dual feasibility condition. Equivalently, every reduced cost `c_ij - u_i - v_j` must be non-negative.

</details>

---

6. If `c_ij = u_i + v_j` for every matched edge and `c_ij >= u_i + v_j` for every unmatched edge, then the current matching is optimal.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

This is the complementary slackness idea: matched edges are tight, and all other edges respect dual feasibility.

</details>

---

7. The Hungarian algorithm can only be applied to square matrices, so rectangular assignment problems must first be converted into square form.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

For a rectangular matrix, add dummy rows or columns so the problem becomes square.

</details>

---

8. A maximum-weight bipartite matching problem can be converted into a minimum-cost problem by negating all weights and then shifting values if necessary.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

Maximizing weights is equivalent to minimizing negative weights. A shift can make the resulting costs non-negative without changing the optimum.

</details>

---

9. If the number of independent zero entries selected during the Hungarian algorithm equals the matrix dimension `N`, then a perfect matching has been found.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

`N` independent zero entries means one selected zero in each row and each column, which gives a perfect assignment.

</details>

---

10. Adding the same constant to every entry of the entire cost matrix changes which assignment is optimal.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

Every perfect assignment uses exactly `N` entries, so every total cost is shifted by the same `N` times that constant.

</details>

---

11. Which statement correctly characterizes a bipartite graph?

- [ ] a. Every vertex must have even degree.
- [ ] b. The graph contains no cycles.
- [ ] c. Its vertices can be partitioned into two independent sets such that every edge joins vertices from different sets.
- [ ] d. Every connected component must be complete.

<details>
<summary>Answer</summary>

c. Its vertices can be partitioned into two independent sets such that every edge joins vertices from different sets.

That is the definition of a bipartite graph.

</details>

---

12. In a bipartite graph matching `M = (V', E')`, what does the cardinality `|M|` represent?

- [ ] a. The number of unmatched vertices.
- [ ] b. The number of edges in the original graph.
- [ ] c. The total number of vertices in both partitions.
- [ ] d. The number of matched edges.

<details>
<summary>Answer</summary>

d. The number of matched edges.

The size of a matching is the number of edges selected into the matching.

</details>

---

13. What is the main purpose of subtracting the minimum value from each row during the first step of the Hungarian algorithm?

- [ ] a. To maximize the number of edges in the graph.
- [ ] b. To create at least one zero in every row while preserving optimal assignments.
- [ ] c. To ensure all costs become distinct.
- [ ] d. To reduce the matrix dimension.

<details>
<summary>Answer</summary>

b. To create at least one zero in every row while preserving optimal assignments.

Subtracting a constant from a row shifts every perfect assignment by the same amount, so the optimum does not change.

</details>

---

14. Suppose a matched edge `(i, j)` satisfies `c_ij > u_i + v_j`. What can be concluded?

- [ ] a. The current solution cannot satisfy complementary slackness.
- [ ] b. The matching is guaranteed optimal.
- [ ] c. The dual solution is infeasible.
- [ ] d. The matrix must be rectangular.

<details>
<summary>Answer</summary>

a. The current solution cannot satisfy complementary slackness.

Matched edges must be tight, meaning `c_ij = u_i + v_j`.

</details>

---

15. In the linear assignment problem, what does the binary variable `x_ij` typically represent?

- [ ] a. Whether row `i` is removed during reduction.
- [ ] b. Whether worker `i` is assigned to task `j`.
- [ ] c. The dual cost associated with edge `(i, j)`.
- [ ] d. The reduced cost after normalization.

<details>
<summary>Answer</summary>

b. Whether worker `i` is assigned to task `j`.

`x_ij = 1` means the assignment is chosen, and `x_ij = 0` means it is not.

</details>

---

16. Why are dummy rows or columns added to an assignment matrix before applying the Hungarian algorithm?

- [ ] a. To increase the number of feasible solutions.
- [ ] b. To force all entries to become positive.
- [ ] c. To transform a rectangular matrix into a square matrix.
- [ ] d. To remove redundant constraints.

<details>
<summary>Answer</summary>

c. To transform a rectangular matrix into a square matrix.

The cost-matrix version of the Hungarian algorithm expects an `N x N` matrix.

</details>

---

17. A consultant wants to maximize suitability scores using the Hungarian algorithm. Which transformation is most appropriate?

- [ ] a. Square all scores.
- [ ] b. Negate the scores and optionally shift them to non-negative values.
- [ ] c. Divide all scores by the largest score.
- [ ] d. Replace every score with its reciprocal.

<details>
<summary>Answer</summary>

b. Negate the scores and optionally shift them to non-negative values.

The Hungarian algorithm is being used as a minimum-cost method, so maximum score becomes minimum negative score.

</details>

---

18. During the Hungarian algorithm, what does it imply if fewer than `N` independent zeros can be selected from an `N x N` matrix?

- [ ] a. The current zero structure is insufficient for a perfect assignment and the matrix must be adjusted further.
- [ ] b. The problem has no feasible solution.
- [ ] c. The matrix already contains an optimal solution.
- [ ] d. The graph is not bipartite.

<details>
<summary>Answer</summary>

a. The current zero structure is insufficient for a perfect assignment and the matrix must be adjusted further.

The algorithm must update the reduced cost matrix to create more useful zero entries.

</details>

---

19. Under the equality condition `c_ij = u_i + v_j` for all matched edges, the objective value of the assignment problem simplifies to:

- [ ] a. `sum_i u_i + sum_j v_j`
- [ ] b. `sum_i sum_j c_ij`
- [ ] c. `sum_i sum_j x_ij`
- [ ] d. `sum_i u_i - sum_j v_j`

<details>
<summary>Answer</summary>

a. `sum_i u_i + sum_j v_j`.

For a perfect matching, each row and column appears exactly once, so the matched cost equals the dual sum.

</details>

---

20. Which situation guarantees that a matching in a bipartite graph is not perfect?

- [ ] a. The matching contains exactly `N` edges in an `N x N` assignment graph.
- [ ] b. At least one vertex remains unmatched.
- [ ] c. Every matched edge has zero reduced cost.
- [ ] d. The graph contains weighted edges.

<details>
<summary>Answer</summary>

b. At least one vertex remains unmatched.

A perfect matching must cover every vertex.

</details>
