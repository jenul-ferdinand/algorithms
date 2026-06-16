# Week 9: B-trees - Learning Roadmap

Source material: `seminar09.pdf` (64 slides), `lab09.pdf`.
Note: there is no `notes09.pdf` for this week. The seminar slides serve as the primary written reference.
Recommended reading: Cormen et al. _Introduction to Algorithms_, ch. 18; Bayer and McCreight, _Organization and Maintenance of Large Ordered Indices_, Boeing Sci Res Labs Report No. 20, 1970; Bayer, _Binary B-Trees for Virtual Memory_, ACM-SIGFIDET 1971.

Legend: `[ ]` concept / theorem / proof to learn. `[ ] Lab Qx`: question from `lab09.pdf`. `[ ] Impl`: implementation exercise. Goals describe what "done" looks like.

The order is the order to learn in. Each section assumes everything above it.

---

## 1. Why B-trees

- [x] The disk-based search problem
    - Large dynamic dictionaries (databases, filesystems) cannot fit in RAM. Cost model: minimise the number of disk page reads, not the number of comparisons. Pages are 4-64 KB; a single random disk read is ~5 orders of magnitude slower than a RAM access.
    - Goal: state the cost model and explain why a balanced binary search tree is wrong here (each node access is potentially a disk page read; tree height log_2 N is too tall).
- [x] Why multi-way trees help
    - If each node holds many keys (and many child pointers) and is sized to a disk page, the tree height becomes log_t N for a node fan-out of t. With t = 1000 and N = 10^9, height is only ~3.
    - Goal: argue why "many branches per node" is the correct generalisation of BSTs for the disk setting.
- [x] Real-world uses
    - Database index structures (PostgreSQL, MySQL InnoDB), filesystems (ext4 htree, NTFS, Btrfs).
    - Goal: name two examples.

---

## 2. B-tree properties

- [x] Definition: B-tree
    - Rooted tree. Each node holds n sorted keys k_1 < k_2 < ... < k_n and n + 1 child subtree pointers T_1, ..., T_{n+1} interleaved with the keys. BST structural property generalised: T_i contains keys < k_i, T_{i+1} contains keys > k_i.
    - Goal: draw the abstract node layout and state the inter-key BST inequality.
- [x] Property: all leaves at the same depth
    - This is what makes B-trees "balanced" by construction (insert/delete grow/shrink at the leaves but rebalance via splits/merges that propagate upward).
    - Goal: state the property; explain why it forces every search path to visit exactly height + 1 nodes.
- [x] Definition: minimum degree t (with t >= 2)
    - Every non-root node has at least t - 1 keys (so at least t children).
    - Every node has at most 2t - 1 keys (so at most 2t children). A node with 2t - 1 keys is full.
    - The root may have as few as 1 key (but is allowed to be empty if the tree is empty).
    - Goal: state both bounds. Note the [t-1, 2t-1] key-count interval.
- [x] Special case: 2-3-4 tree
    - When t = 2, every internal node has 2, 3, or 4 children (1, 2, or 3 keys). This is the simplest non-trivial B-tree.
    - Goal: state which non-binary-but-balanced trees are 2-3-4 trees.
- [x] Lab Q4: lower bound on height
    - The tree is densest when every node is full (2t - 1 keys). With root holding 2t - 1 keys and a full tree of height h, total keys = (2t - 1) * (1 + 2t + (2t)^2 + ... + (2t)^h) = (2t - 1) * ((2t)^{h+1} - 1) / (2t - 1) = (2t)^{h+1} - 1.
    - So N <= (2t)^{h+1} - 1, giving h >= log_{2t}(N + 1) - 1.
    - Goal: produce the geometric sum argument and state the bound.
- [x] Lab Q5: upper bound on height
    - The tree is sparsest when every non-root has the minimum t - 1 keys (so t children). Root has 1 key. Total keys >= 1 + 2(t - 1) * (1 + t + t^2 + ... + t^{h-1}) = 1 + 2(t - 1) * (t^h - 1) / (t - 1) = 2 * t^h - 1.
    - So N >= 2 * t^h - 1, giving h <= log_t((N + 1) / 2).
    - Goal: produce the geometric sum and state the bound. The standard CLRS form is h <= log_t((N + 1) / 2) = O(log_t N).
- [ ] Lab Q6: can all nodes be simultaneously full or simultaneously minimum-occupancy?
    - All full: only at very specific values of N (where N = (2t)^{h+1} - 1 for some h). Generally no.
    - All minimum: only at specific values of N (where N = 2 * t^h - 1). Generally no.
    - Goal: argue this carefully. Insert/delete cycles can transition between near-full and near-minimum but cannot in general realise the boundaries simultaneously across all nodes.
- [ ] Lab Q9: worst-case space complexity
    - O(N) overall (each key occupies O(1) space, plus O(N/t) child pointers across nodes). Per-node space is O(t).
    - Goal: state O(N) total.

---

## 3. Search

- [x] Multi-way search inside a node
    - Within a node holding sorted keys k_1 < ... < k_n, binary search for x in O(log n) = O(log t) comparisons. If x is found, return. Otherwise determine the unique i such that k_i < x < k_{i+1} (or x < k_1, or x > k_n) and recurse into T_i.
    - Goal: state the per-node work as O(log t).
- [ ] Lab Q1: search(P, x) pseudocode
    - Binary search keys of P. If found, return true. Otherwise: if P is a leaf, return false. Otherwise recurse on the appropriate child T_i.
    - Termination: each recursive call descends one level; the depth is bounded by the height h = O(log_t N).
    - Goal: produce the pseudocode and the termination justification.
- [ ] Total search cost
    - O(h * log t) = O(log_t N * log t) = O(log N) comparisons. But more importantly, only O(log_t N) disk page reads.
    - Goal: state both the comparison cost and the I/O cost (the latter is the one B-trees actually optimise).

---

## 4. Insert (with proactive splitting)

- [x] The split primitive
    - To split a full node N (with 2t - 1 keys) on its way to inserting a new key, take the median k_t. The keys k_1, ..., k_{t-1} stay in N; the keys k_{t+1}, ..., k_{2t-1} move into a new sibling N'. The median k_t moves up to the parent.
    - The parent gains one key (the median) and one child pointer (to N').
    - Goal: draw the split for a node with 7 keys at t = 4 (slide 21-22) and confirm both halves now have t - 1 = 3 keys, the median moves up.
- [x] Why the parent must not be full at split time
    - The parent gains a key during the split. If the parent were already at 2t - 1 keys, the split would overflow it.
    - Goal: explain the invariant.
- [x] Proactive splitting on the way down
    - Insert traverses from root to leaf. Before stepping into any node along the path, if that node is full, split it first. By the time we reach the target leaf, the entire path is non-full, so a leaf insert never needs to propagate upward.
    - Goal: state the invariant and explain why proactive splitting avoids the cascading recursive split that a naive bottom-up insert would need.
- [x] Special case: root split
    - If the root is full at the start of insert, allocate a new root with no keys, make the old root its only child, then split. The tree height grows by 1. This is the only place height grows.
    - Goal: identify root splits as the unique mechanism for height growth.
- [x] Worked example: insert sequence (slide 23-36)
    - Step through inserting B, Q, L, F into a t=3 tree of consonants. Identify when each split fires.
    - Goal: redo the example and predict each split.
- [x] Lab Q2: insert {S, Z, G, Y, B, N, D, E, F, U, I, V, M, X, H} into an empty t=3 tree
    - Draw the tree state after each insertion.
    - Goal: produce 15 snapshots, identifying every split.
- [x] Lab Q8: bounds on number of nodes when inserting {1, 2, ..., n} at t = 2
    - Sequential inserts always add at the rightmost leaf and split as needed. At t = 2 (2-3-4 tree), the splits follow a deterministic pattern; both bounds can be derived from N = 2 * t^h - 1 (sparsest) and N = (2t)^{h+1} - 1 (densest).
    - Goal: produce tight upper and lower bounds and identify the values of n where each is realised.

---

## 5. Delete (with proactive merging / borrowing)

- [x] The deletion problem
    - Remove key x from the B-tree. If x is in a leaf, simply remove it (provided the leaf still has >= t - 1 keys after removal). If x is in an internal node, things get harder.
    - Goal: identify the three cases below.
- [x] Case 1: x is in a leaf
    - Just remove x. Works only if the leaf has > t - 1 keys before removal.
    - Goal: state the precondition.
- [x] Case 2: x is in an internal node N
    - 2a: the child T_i to the left of x has >= t keys. Replace x with its predecessor (rightmost key of the subtree T_i), then recursively delete the predecessor from T_i.
    - 2b: the child T_{i+1} to the right of x has >= t keys. Replace x with its successor (leftmost key of T_{i+1}), then recursively delete from T_{i+1}.
    - 2c: both T_i and T_{i+1} have only t - 1 keys. Merge T_i, x, and T_{i+1} into a single node of 2t - 1 keys, remove x from N, then recursively delete x from the merged child.
    - Goal: state all three subcases and explain why merge is the fallback.
- [x] Case 3: x is in a subtree T_i but T_i has only t - 1 keys
    - Before descending, ensure T_i has at least t keys.
    - 3a: a sibling of T_i has >= t keys. Borrow: rotate one key from sibling through the parent into T_i.
    - 3b: both siblings (where applicable) have only t - 1 keys. Merge T_i with one sibling and the corresponding parent key, dropping the parent key into the merged child.
    - Now descend into T_i (or the merged result) and recursively delete.
    - Goal: state both subcases. Note that case 3b can shrink the parent, potentially propagating upward; the proactive top-down enforcement prevents this from cascading uncontrollably.
- [x] Proactive merging on the way down
    - Mirror of proactive splitting: before stepping into any node with only t - 1 keys, fix it first via case 3.
    - Goal: state the symmetry between insert and delete.
- [x] Tree shrinks when the root empties
    - If the root has 1 key and a merge consumes it (case 2c at the top level, or case 3b when both children of the root merge), the root becomes empty and the merged child becomes the new root. Tree height drops by 1.
    - Goal: identify root merge as the unique mechanism for height shrinkage.
- [x] Lab Q3: delete {1, 22, 16, 8, 18, 5} from the given t=2 tree
    - Draw the tree state after each deletion.
    - Goal: produce 6 snapshots, identifying every borrow / merge / replace-with-predecessor-or-successor.

---

## 6. Time and space complexity

- [ ] Lab Q10: search, insert, delete time complexities
    - Search: O(log_t N) disk reads, O(log N) comparisons.
    - Insert: O(log_t N) disk reads (root to leaf), O(log N) comparisons. Each node visited may trigger a split (constant work per split). Worst case: a split on every level, plus a leaf insert.
    - Delete: O(log_t N) disk reads. Each node may trigger a borrow (O(1)) or merge (O(t)). Worst case: a merge on every level.
    - Goal: state all three bounds in both metrics (I/O and comparisons).
- [ ] Why disk-I/O bounds matter more than comparison bounds
    - For databases on disk, the comparison count is irrelevant; what matters is the number of pages read. B-trees are tuned to minimise that.
    - Goal: state in one sentence.

---

## 7. Amortised analysis: split and merge counts

- [ ] Lab Q7: the potential function Phi(B) = sum over P in B(t) of ((2t - 1) - nKeys(P))
    - Each node contributes 0 when full (2t - 1 keys) and up to t when minimum (t - 1 keys, except root which can be even less). Boundary checks: Phi >= 0 always; Phi(empty tree) = 0.
    - Goal: state the function and verify the boundaries.
- [ ] Lab Q7(a): bound the total number of splits during n insertions
    - A split takes a full node (Phi contribution 0) and creates two non-full nodes (each contributing t to Phi via 2t - 1 - (t - 1) = t for each), plus adds one key to the parent (decreasing the parent's Phi contribution by 1).
    - Net Delta Phi per split: +t + t - 1 = 2t - 1 (an increase). Each insert increases Phi by at most O(1) outside of splits (one new key in some leaf increases that leaf's contribution by -1). So sum of Delta Phi over n insertions is O(n).
    - Sum of Delta Phi >= (number of splits) * (2t - 1) - O(n), so number of splits <= O(n / (2t - 1)) = O(n).
    - Goal: produce the analysis. The bound is amortised O(1) splits per insertion.
- [ ] Lab Q7(b): bound the total number of merges during n deletions
    - Symmetric argument. A merge consumes two minimum-occupancy nodes (each contributing t) plus a parent key (contributing 1) and produces one full node (contributing 0). Delta Phi per merge: -2t - 1 + t = -t - 1, but actually need to re-derive carefully.
    - Goal: produce the analysis. The conclusion is the same: O(n) total merges over n deletions, i.e. amortised O(1) merges per deletion.

---

## 8. Implementation milestones, summarised

A re-listing of the implementation steps in order. New files live in `src/`.

- [ ] Step 1: data structures.
    - `src/btree_node.py` (or in the same file): BTreeNode class with fields keys (sorted list), children (list of child pointers, length = len(keys) + 1 for internal, empty for leaf), is_leaf flag.
- [ ] Step 2: search.
    - `src/btree.py`: BTree class with __init__(t), search(x). Implement the recursive descent with binary search inside each node (Lab Q1).
- [ ] Step 3: insert with proactive splitting.
    - Method `insert(x)`. If root is full, split first (allocate new root). Then recursive `insert_nonfull(node, x)` that splits any full child before descending into it.
- [ ] Step 4: delete with proactive merging/borrowing.
    - Method `delete(x)`. Cases 1, 2 (a/b/c), 3 (a/b). The trickiest is case 2c plus case 3 fixups.
- [ ] Step 5 (Lab Impl Q1): full test battery.
    - Property tests: insert random sequences, then delete random subsequences, verify the in-order traversal matches sorted(remaining_keys). Include the Lab Q2 and Lab Q3 sequences as deterministic regression tests.
- [ ] Step 6 (stretch, optional): plot height vs N for a sequence of inserts at various t values. Confirm log_t N scaling matches Lab Q5's upper bound.
- [ ] Step 7 (stretch, optional): instrument the tree to count splits over n inserts and merges over n deletes. Confirm the empirical O(n) bounds from Lab Q7.
