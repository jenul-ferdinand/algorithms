# Week 10 Moodle Quiz

Topic: linear programming.

## Questions

1. Every linear programming problem in standard form must contain a linear objective function, linear constraints, and non-negativity constraints on all decision variables.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

In the unit's standard form, an LP has a linear objective, linear `<=` constraints, and all decision variables are constrained to be `>= 0`.

</details>

---

2. The feasible region of a linear program is always non-convex because it is formed by intersecting multiple constraints.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

Linear inequalities define half-spaces, and intersections of half-spaces stay convex.

</details>

---

3. Adding a slack variable to a `<=` constraint converts the inequality into an equality without changing the feasible solutions.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

The slack variable records unused capacity. For example, `x + y <= 5` becomes `x + y + s = 5` with `s >= 0`.

</details>

---

4. In the simplex method, non-basic variables are the variables currently fixed to zero.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

The slides call this terminology counter-intuitive: basic variables are free, while non-basic variables are fixed to `0`.

</details>

---

5. The exhaustive search approach for solving linear programs evaluates only feasible solutions.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

Exhaustive enumeration tries choices of non-basic variables, then some resulting basic solutions can have negative values and are infeasible.

</details>

---

6. During simplex iterations for a maximization problem, a non-basic variable with a positive coefficient in the objective function can potentially improve the objective value if increased feasibly.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

A positive coefficient means increasing that variable increases `z`, as long as the constraints can still be satisfied.

</details>

---

7. The simplex method stops once every non-basic variable would decrease the objective value or violate feasibility if adjusted.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

At that point there is no feasible direction that can improve the objective, so the current basic feasible solution is optimal.

</details>

---

8. For a linear program with a bounded feasible region, at least one optimal solution occurs at a corner point of the feasible region.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

The key LP insight is that an optimum can be found at a corner point of the feasible polyhedron.

</details>

---

9. In tableau simplex, the entering variable is always chosen as the variable with the smallest coefficient in the `Cj - Zj` row.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

For a maximization problem, we usually choose the largest positive coefficient in the `Cj - Zj` row.

</details>

---

10. A minimization objective can be converted into a maximization objective by multiplying the objective function by `-1`.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

Minimizing `z` is equivalent to maximizing `-z`.

</details>

---

11. Consider the constraint `4x + 3y <= 20`. After introducing a slack variable `s`, which equation is obtained?

- [ ] a. `4x + 3y - s = 20`
- [ ] b. `4x + 3y + s = 20`
- [ ] c. `4x + 3y + s <= 20`
- [ ] d. `4x + 3y = 20 + s`

<details>
<summary>Answer</summary>

b. `4x + 3y + s = 20`.

For a `<=` constraint, add a non-negative slack variable to the left side.

</details>

---

12. Why is the feasible region of a standard linear program convex?

- [ ] a. Because objective functions are quadratic
- [ ] b. Because every feasible point must lie on a boundary
- [ ] c. Because intersections of linear half-spaces are convex
- [ ] d. Because simplex explicitly enforces convexity

<details>
<summary>Answer</summary>

c. Because intersections of linear half-spaces are convex.

Each linear inequality cuts out a convex half-space. The feasible region is their intersection.

</details>

---

13. A linear program contains `N` decision variables and `m` constraints. After introducing slack variables, how many ways are explored in exhaustive enumeration?

- [ ] a. `N^m`
- [ ] b. `(N + m)!`
- [ ] c. `((N + m) choose N)`
- [ ] d. `2^(N + m)`

<details>
<summary>Answer</summary>

c. `((N + m) choose N)`.

There are `N + m` total variables after adding `m` slack variables. Exhaustive enumeration chooses `N` of them to fix as non-basic.

</details>

---

14. In simplex for a maximization problem, which non-basic variable is usually selected to enter the basis?

- [ ] a. The variable with the largest negative coefficient in the objective
- [ ] b. The variable with the largest positive coefficient in the objective
- [ ] c. The variable with the smallest RHS value
- [ ] d. The variable currently in the basis with maximum value

<details>
<summary>Answer</summary>

b. The variable with the largest positive coefficient in the objective.

Increasing that variable gives the steepest immediate improvement in `z`.

</details>

---

15. Why does simplex choose the minimum feasible ratio when determining the leaving variable?

- [ ] a. To maximize the number of pivots
- [ ] b. To preserve feasibility of all constraints
- [ ] c. To ensure all variables become non-basic
- [ ] d. To minimize the objective function

<details>
<summary>Answer</summary>

b. To preserve feasibility of all constraints.

The minimum ratio is the first constraint that becomes tight. Going further would make some basic variable negative.

</details>

---

16. For a maximization problem, which condition indicates that simplex has reached an optimum solution?

- [ ] a. All RHS values are equal
- [ ] b. All basic variables are zero
- [ ] c. No positive coefficient remains in the `Cj - Zj` row
- [ ] d. The tableau becomes symmetric

<details>
<summary>Answer</summary>

c. No positive coefficient remains in the `Cj - Zj` row.

No positive reduced cost means no non-basic variable can be increased to improve the objective.

</details>

---

17. Which transformation converts the constraint `5x + 2y >= 9` into canonical `<=` form?

- [ ] a. `5x + 2y - 9 <= 0`
- [ ] b. `-5x - 2y <= -9`
- [ ] c. `5x + 2y + 9 <= 0`
- [ ] d. `-5x + 2y <= -9`

<details>
<summary>Answer</summary>

b. `-5x - 2y <= -9`.

Multiplying an inequality by `-1` reverses its direction.

</details>

---

18. In a standard-form LP with `6` variables and `3` equations, how many variables are non-basic in a basic feasible solution?

- [ ] a. `2`
- [ ] b. `3`
- [ ] c. `4`
- [ ] d. `6`

<details>
<summary>Answer</summary>

b. `3`.

With `6` total variables and `3` equations, there are `3` basic variables and `6 - 3 = 3` non-basic variables.

</details>

---

19. Suppose the simplex objective equation is `z = 24 + y - 2t` where `y` and `t` are non-basic variables. Which statement is correct?

- [ ] a. Increasing `t` increases `z`
- [ ] b. Increasing `y` may improve `z` while keeping feasibility
- [ ] c. Both `y` and `t` must decrease
- [ ] d. The solution is already infeasible

<details>
<summary>Answer</summary>

b. Increasing `y` may improve `z` while keeping feasibility.

The coefficient of `y` is positive, so increasing `y` increases `z` if the constraints allow it.

</details>

---

20. Which of the following is NOT an advantage of the simplex method compared with exhaustive enumeration?

- [ ] a. It explores progressively improving solutions
- [ ] b. It avoids infeasible solutions during traversal
- [ ] c. It guarantees polynomial worst-case running time
- [ ] d. It can terminate once optimality is detected

<details>
<summary>Answer</summary>

c. It guarantees polynomial worst-case running time.

Simplex is efficient in practice, but it does not have a polynomial worst-case guarantee.

</details>
