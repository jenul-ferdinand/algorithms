# Week 7 Moodle Quiz

Topic: Fibonacci heaps.

## Questions

1. A Fibonacci heap is a collection of trees that each satisfy the min-heap property.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

A Fibonacci heap is a forest of heap-ordered trees. Each parent key is at most the key of each child.

</details>

---

2. Nodes in a Fibonacci heap are connected using circular doubly linked lists at each level.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

The root list and each sibling list are circular doubly linked lists, which makes splicing and cutting cheap.

</details>

---

3. The merge operation in Fibonacci heaps requires restructuring trees to maintain degree constraints.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

Merge is lazy: it just concatenates the root lists and updates the minimum pointer. Degree cleanup is delayed until `extract-min`.

</details>

---

4. Extract-min always immediately restores a strict binomial structure.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

Consolidation leaves at most one root of each degree, but the trees are still Fibonacci heap trees, not necessarily strict binomial trees.

</details>

---

5. Insert in a Fibonacci heap is implemented by merging a single-node heap.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

Insert can create a singleton heap and splice it into the root list, updating `H.min` if needed.

</details>

---

6. After consolidation, there is at most one tree of any given degree in the root list.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

Consolidation repeatedly links roots of equal degree until no two root-list trees have the same degree.

</details>

---

7. If decrease-key violates heap order, the node is cut and moved to the root list.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

If the decreased key becomes smaller than its parent's key, the node is cut from its parent and promoted to the root list.

</details>

---

8. A node is marked after it loses two children.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

A non-root node is marked after losing one child. If it later loses another child, it is cut.

</details>

---

9. Cascading cuts stop when an unmarked node is encountered or the root is reached.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

An unmarked non-root parent is marked and the cascade stops; roots are never marked, so reaching a root also stops the cascade.

</details>

---

10. The degree of a node in a Fibonacci heap is bounded by `O(log N)`.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

A degree-`d` node has subtree size at least Fibonacci in `d`, so `d <= log_phi(N) = O(log N)`.

</details>

---

11. What is stored in each Fibonacci heap node?

- [ ] a. Key only
- [ ] b. Key, degree, mark, and pointers
- [ ] c. Only children pointers
- [ ] d. Array index

<details>
<summary>Answer</summary>

b. Key, degree, mark, and pointers.

The pointers include parent, child, left sibling, and right sibling links.

</details>

---

12. Why is merge `O(1)` in Fibonacci heaps?

- [ ] a. Trees are balanced
- [ ] b. No nodes are moved
- [ ] c. Root lists are concatenated
- [ ] d. Sorting is avoided

<details>
<summary>Answer</summary>

c. Root lists are concatenated.

Circular doubly linked root lists can be spliced together with constant pointer updates.

</details>

---

13. What happens to the children of the minimum node during extract-min?

- [ ] a. They are deleted
- [ ] b. They remain attached
- [ ] c. They are added to the root list
- [ ] d. They are sorted

<details>
<summary>Answer</summary>

c. They are added to the root list.

The minimum root is removed, and its children become new roots before consolidation.

</details>

---

14. What triggers merging of two trees during consolidation?

- [ ] a. Same key
- [ ] b. Same degree
- [ ] c. Same depth
- [ ] d. Same parent

<details>
<summary>Answer</summary>

b. Same degree.

Consolidation links roots of equal degree; the smaller-key root becomes the parent.

</details>

---

15. What happens when a node violates heap order after decrease-key?

- [ ] a. Nothing
- [ ] b. Node is deleted
- [ ] c. Node is cut and added to root list
- [ ] d. Heap is rebuilt

<details>
<summary>Answer</summary>

c. Node is cut and added to root list.

This preserves heap order locally while keeping `decrease-key` cheap amortised.

</details>

---

16. What does a marked node indicate?

- [ ] a. It has no children
- [ ] b. It lost one child
- [ ] c. It is root
- [ ] d. It is minimum

<details>
<summary>Answer</summary>

b. It lost one child.

Marks remember that a non-root node has already lost one child since it became a child of its current parent.

</details>

---

17. What triggers cascading cuts?

- [ ] a. Node becomes root
- [ ] b. Parent is marked
- [ ] c. Degree is zero
- [ ] d. Node has many children

<details>
<summary>Answer</summary>

b. Parent is marked.

If a cut makes an already-marked parent lose another child, that parent is also cut, and the process may continue upward.

</details>

---

18. Which operation is `O(1)` amortized in Fibonacci heaps?

- [ ] a. `extract-min`
- [ ] b. `delete`
- [ ] c. `decrease-key`
- [ ] d. `consolidate`

<details>
<summary>Answer</summary>

c. `decrease-key`.

The actual cascade can be longer, but the marking scheme pays for it amortised, giving `O(1)` amortised time.

</details>

---

19. Why is the degree of a node logarithmic?

- [ ] a. Tree is balanced
- [ ] b. Binary structure
- [ ] c. Fibonacci growth property
- [ ] d. Sorting constraint

<details>
<summary>Answer</summary>

c. Fibonacci growth property.

The minimum subtree size for degree `d` grows like a Fibonacci number, so `N >= F_{d+2}` implies `d = O(log N)`.

</details>

---

20. `Delete(x)` is implemented using which sequence?

- [ ] a. `extract-min` then `merge`
- [ ] b. `decrease-key` then `extract-min`
- [ ] c. `merge` then `delete`
- [ ] d. Rebuild heap

<details>
<summary>Answer</summary>

b. `decrease-key` then `extract-min`.

Decrease `x` to `-infinity` so it becomes the minimum, then remove it with `extract-min`.

</details>
