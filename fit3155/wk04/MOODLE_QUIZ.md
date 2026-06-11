# Week 4 Moodle Quiz

Topic: suffix trees and Ukkonen's linear-time construction.

## Questions

1. A suffix tree is a compressed version of a suffix trie.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

A suffix trie stores every suffix character-by-character. A suffix tree compresses chains of single-child nodes into labelled edges.

</details>

---

2. Building a suffix tree by inserting all suffixes one by one takes `O(n)` time.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

The naive construction inserts `n` suffixes, and each insertion can walk through `O(n)` characters, giving `O(n^2)` time.

</details>

---

3. Storing edge labels explicitly as substrings results in `O(n^2)` space in the worst case.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

There are `O(n)` edges, and an explicit substring label can be length `O(n)`, so the total label storage can become quadratic.

</details>

---

4. Ukkonen's algorithm constructs suffix trees in `O(n)` time.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

With suffix links, skip-counting, showstopper, and rapid leaf extension, the total work over all phases is linear.

</details>

---

5. An implicit suffix tree includes the terminal symbol `$`.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

An implicit suffix tree is for the current prefix without appending the terminal symbol. The final explicit suffix tree is obtained by adding `$`.

</details>

---

6. Every internal node except root has a suffix link in Ukkonen's algorithm.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

If an internal node represents `x alpha`, its suffix link points to the internal node representing `alpha`.

</details>

---

7. Rule 3 in Ukkonen's algorithm requires splitting an edge.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

Rule 3 means the new character is already on the path, so no tree edge is changed. Splitting an edge is Rule 2 case 2.

</details>

---

8. The skip-count trick allows skipping multiple characters during traversal.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

Instead of comparing every character on an edge, skip-count uses the edge length to jump across whole edges when possible.

</details>

---

9. Once Rule 3 is encountered in a phase, all remaining extensions in that phase can terminate.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

True.

This is the showstopper rule: if the current suffix already has the new character, every shorter suffix will also already be present.

</details>

---

10. In Ukkonen's algorithm, a leaf node may later become an internal node.

- [ ] True
- [ ] False

<details>
<summary>Answer</summary>

False.

Once a leaf, always a leaf. If an edge to a leaf is split, a new internal node is created above it; the old leaf stays a leaf.

</details>

---

11. What is stored in a suffix tree?

- [ ] a. All suffixes of the string
- [ ] b. Only prefixes
- [ ] c. Only distinct characters
- [ ] d. All substrings of the string

<details>
<summary>Answer</summary>

a. All suffixes of the string.

Each root-to-leaf path spells one suffix of the string.

</details>

---

12. What is the worst-case time complexity of naive suffix tree construction?

- [ ] a. `O(n log n)`
- [ ] b. `O(n^2)`
- [ ] c. `O(mn)`
- [ ] d. `O(n)`

<details>
<summary>Answer</summary>

b. `O(n^2)`.

There are `n` suffixes, and inserting one suffix can take `O(n)` time.

</details>

---

13. What is the key role of suffix links?

- [ ] a. Sorting suffixes
- [ ] b. Reducing space complexity
- [ ] c. Eliminating leaves
- [ ] d. Speeding up traversal between related suffixes

<details>
<summary>Answer</summary>

d. Speeding up traversal between related suffixes.

A suffix link moves from `x alpha` to `alpha`, so the next extension does not restart from the root.

</details>

---

14. Each phase in Ukkonen's algorithm corresponds to:

- [ ] a. Adding one character of the string
- [ ] b. Deleting nodes
- [ ] c. Sorting edges
- [ ] d. Adding a suffix

<details>
<summary>Answer</summary>

a. Adding one character of the string.

Phase `i + 1` turns the implicit suffix tree for `str[1..i]` into the one for `str[1..i+1]`.

</details>

---

15. Which rule applies when a mismatch occurs during extension and requires splitting an edge?

- [ ] a. Rule 2
- [ ] b. Rule 3
- [ ] c. Rule 1 and 3
- [ ] d. Rule 1

<details>
<summary>Answer</summary>

a. Rule 2.

More specifically, this is Rule 2 case 2: split the edge, create an internal node, then add the new leaf.

</details>

---

16. Why does Rule 3 allow early termination of a phase?

- [ ] a. Because all suffixes are processed
- [ ] b. Because the current character already exists on the path
- [ ] c. Because suffix links are exhausted
- [ ] d. Because a new node is created

<details>
<summary>Answer</summary>

b. Because the current character already exists on the path.

The extended suffix is already implicitly present, so the later shorter suffixes in the same phase will also be present.

</details>

---

17. What ensures `O(n)` time in Ukkonen's algorithm?

- [ ] a. Binary search
- [ ] b. Sorting suffixes
- [ ] c. Suffix links + skip-count + implementation tricks
- [ ] d. Dynamic programming

<details>
<summary>Answer</summary>

c. Suffix links + skip-count + implementation tricks.

Suffix links avoid root restarts, skip-count avoids character-by-character walking, and the showstopper/global-end tricks avoid wasted extensions.

</details>

---

18. When converting an implicit suffix tree into an explicit suffix tree, what is required?

- [ ] a. Removing suffix links
- [ ] b. Adding terminal symbol `$`
- [ ] c. Sorting nodes
- [ ] d. Compressing edges

<details>
<summary>Answer</summary>

b. Adding terminal symbol `$`.

The terminal symbol makes every suffix end at its own leaf, so no suffix is hidden as a prefix of another suffix.

</details>

---

19. Why does storing edge labels as `(start, end)` indices reduce space complexity?

- [ ] a. It avoids storing duplicate substrings explicitly
- [ ] b. It compresses the tree height
- [ ] c. It reduces the number of nodes
- [ ] d. It removes suffix links

<details>
<summary>Answer</summary>

a. It avoids storing duplicate substrings explicitly.

Each edge stores two indices into the original string instead of copying the whole substring.

</details>

---

20. Which of the following best explains why Ukkonen's algorithm is linear time?

- [ ] a. Each suffix is processed independently
- [ ] b. Total number of explicit extensions is `O(n)`
- [ ] c. Tree height is bounded by `log n`
- [ ] d. Each phase processes all suffixes fully

<details>
<summary>Answer</summary>

b. Total number of explicit extensions is `O(n)`.

Rule 1s are handled by the global end, Rule 3 stops the phase, and only `O(n)` Rule 2-style explicit work remains.

</details>

---

21. In Ukkonen's algorithm, what happens immediately after following a suffix link during extension?

- [ ] a. Restart from root
- [ ] b. Delete the current node
- [ ] c. Recompute all suffixes
- [ ] d. Continue traversal using the remainder substring

<details>
<summary>Answer</summary>

d. Continue traversal using the remainder substring.

The suffix link moves to the next active node, then the remainder is walked down to find the next extension point.

</details>

---

22. What is the "remainder" in Ukkonen's algorithm?

- [ ] a. The remaining suffixes not yet inserted
- [ ] b. The depth of the tree
- [ ] c. The number of suffixes left
- [ ] d. The substring that still needs to be traversed after reaching the active node

<details>
<summary>Answer</summary>

d. The substring that still needs to be traversed after reaching the active node.

In the unit's notation, the active node is the deepest internal node already reached, and the remainder is what is left below it.

</details>

---

23. Which scenario corresponds to Rule 1?

- [ ] a. A character already exists on the path
- [ ] b. A mismatch occurs in the middle of an edge
- [ ] c. A suffix link is followed
- [ ] d. The path ends at a leaf and we extend the edge

<details>
<summary>Answer</summary>

d. The path ends at a leaf and we extend the edge.

Rule 1 is the leaf-extension rule. With the global end trick, all such leaf extensions happen implicitly.

</details>

---

24. Why can leaves be extended in `O(1)` time using the global end trick?

- [ ] a. Leaves are never updated
- [ ] b. Each leaf stores full substring
- [ ] c. All leaf edges share a common end pointer
- [ ] d. Suffix links update them automatically

<details>
<summary>Answer</summary>

c. All leaf edges share a common end pointer.

Incrementing that one shared `globalEnd` value extends every leaf edge at once.

</details>

---

25. Which statement about suffix links is MOST accurate?

- [ ] a. They connect leaves to root
- [ ] b. They connect nodes representing substrings differing by the first character
- [ ] c. They connect nodes with identical substrings
- [ ] d. They are only used once per phase

<details>
<summary>Answer</summary>

b. They connect nodes representing substrings differing by the first character.

A suffix link goes from the node for `x alpha` to the node for `alpha`.

</details>

---

26. What is the main benefit of the skip-count trick?

- [ ] a. Reduces number of nodes
- [ ] b. Avoids character-by-character comparisons during traversal
- [ ] c. Avoids suffix links
- [ ] d. Ensures balanced tree

<details>
<summary>Answer</summary>

b. Avoids character-by-character comparisons during traversal.

It jumps over full edge labels using their lengths, instead of checking each character on the edge.

</details>

---

27. Why does Rule 3 imply that subsequent extensions also use Rule 3?

- [ ] a. Because no nodes remain
- [ ] b. Because suffix links stop working
- [ ] c. Because tree becomes full
- [ ] d. Because all smaller suffixes will also have the same continuation

<details>
<summary>Answer</summary>

d. Because all smaller suffixes will also have the same continuation.

If `str[j..i+1]` is already present, then each shorter suffix `str[j+1..i+1]`, `str[j+2..i+1]`, and so on is already present too.

</details>

---

28. Which of the following best describes the active node?

- [ ] a. Always the root
- [ ] b. Last created node
- [ ] c. A random internal node
- [ ] d. The node where the next extension is applied

<details>
<summary>Answer</summary>

d. The node where the next extension is applied.

More precisely, it is the deepest internal node on the path to the next extension point.

</details>
