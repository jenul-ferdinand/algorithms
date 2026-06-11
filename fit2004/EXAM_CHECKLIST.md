# Page 1

# FIT2004 Exam Checklist

[x] [x] [x] CONFIDENT and ready! 😎  
[x] [x] [ ] Intermediate 😐  
[x] [ ] [ ] Novice 😌  
[ ] [ ] [ ] Not ready at all... 😤  

## W1: Divide and Conquer Paradigm

[ ] [ ] [ ] Karatsuba’s Multiplication Algorithm  
[x] [x] [x] Time Complexity  
[x] [x] [x] Space Complexity and Auxiliary Space Complexity  
[x] [x] [x] Recurrence Relations  
[x] [ ] [ ] Master Theorem / standard recurrences  
[x] [x] [x] Recurrence “back-substitution” / induction examples (beyond just Karatsuba)  

## W2: Correctness Proof

[x] [x] [ ] Loop Invariants  
[x] [x] [ ] Comparison-based Sorting and its Lower Bound  
[x] [x] [x] Counting Sort  
[x] [x] [x] Radix Sort  
[ ] [ ] [ ] Proof techniques for “lower-bounds on comparison sorts” (decision-tree argument)  

# Page 2

## W3: QuickSort Review

[x] [ ] [ ] Partition out of place/in place/stable  
[x] [ ] [ ] Complexity Analysis of QuickSort (best/worst/average)  
[x] [x] [x] K-th Order Statistic  
[x] [x] [x] QuickSelect  
[x] [x] [ ] Median of Medians  
[x] [ ] [ ] Detailed partition variants (Hoare vs. Lomuto vs. DNF) and when each is stable/in-place  
[x] [x] [ ] “Expected vs. worst-case” analysis of QuickSort (why random pivots give Θ(nlogn) on average)  

## W4: Graph Definitions

[x] [x] [x] Graph Representation (adjacency matrix vs adjacency list)  
[x] [x] [x] BFS  
[x] [x] [x] DFS  
[x] [x] [x] Applications of BFS and DFS  
[x] [x] [ ] Adjacency-matrix vs. Adjacency-list tradeoffs (space O(V^2) vs. O(V+E) operation costs)  
[x] [x] [x] Undirected vs. Directed terminology (in-degree, out-degree)  
[x] [x] [x] Edge-weight implications (unweighted => BFS; positive weights => Dijkstra; negative weights => Bellman-Ford)  

# Page 3

## W5: Greedy Algorithms

[x] [x] [x] Dijkstra’s Algorithm  
[x] [x] [x] Minimum Spanning Trees  
[x] [x] [x] Prim’s Algorithm  
[x] [x] [x] Kruskal’s Algorithm  
[x] [x] [ ] Union-Find Data Structure  
[ ] [ ] [ ] How to prove the correctness of greedy algorithms  
[x] [ ] [ ] Union-Find  
- Amortized α(n) proof sketch  
- Why path-compression + union-by-rank is nearly constant  

[ ] [ ] [ ] Correctness sketches: “cut” vs. “cycle” properties (MST proofs for Kruskal/Prim)  

# Page 4

## W6: Introduction to Dynamic Programming

[x] [x] [ ] Memoization vs. Bottom-up (table-filling) comparison (pros/cons of each)  
[x] [x] [ ] Fibonacci (top-down vs. bottom-up)  
[ ] [ ] [ ] Coin Change  
[ ] [ ] [ ] Unbounded Knapsack  
[ ] [ ] [ ] 0/1 Knapsack (two-dimensional table or “rolling array” trick)  
[ ] [ ] [ ] Edit Distance (Levenshtein)  
[ ] [ ] [ ] Constructing Optimal Solutions (backtracking vs decision array)  
[x] [x] [x] “Space-saving trick” (when you only need the previous row/column in a DP table)  

## W7: Dynamic Programming Graph Algorithms

[x] [x] [x] Bellman-Ford  
- Shortest paths on graphs with negative weights  
- Detecting negative-weight cycles  
- Runtime O(V * E)  

[x] [x] [x] All pairs shortest paths  

[x] [x] [ ] Floyd-Warshall  
- All pairs shortest paths  
- Simple triple nested loops  
- Runtime O(V^3)  

[ ] [ ] [ ] Transitive Closure  

[ ] [ ] [ ] Critical Path problem on a DAG  
- Longest path in an acyclic graph via topological order  

# Page 5

## W8: Flow Network Properties and Max-Flow Problem

[x] [x] [x] Ford-Fulkerson Algorithm  
- Ford-Fulkerson vs. Edmonds-Karp  
- Why BFS-based augmenting path choice yields O(VE^2)  

[x] [x] [x] Augmenting Paths in the Residual Network  
- Reverse edges semantics  

[x] [ ] [ ] Complexity Analysis of Ford-Fulkerson Algorithm  
[x] [x] [x] Cuts  
[x] [x] [ ] Connection between max-flow and min-cut problems  
[x] [ ] [ ] Proof of Correctness of Ford-Fulkerson Algorithm  

## W9: Circulation with Demands

[x] [x] [x] Bipartite Matching  
- Matching via flow  
- Build a unit-capacity network  

[x] [x] [x] Circulation with Demands  
[x] [x] [x] Circulation with Demands and Lower Bounds  
- Feasible flow check via super-source / sink trick  

[x] [x] [x] Applications of Network Flow techniques to solve combinatorial problems  
- Edge-disjoint paths  
- Vertex-cover  
- Matching  

# Page 6

## W10: Retrieval Data Structures for Strings

[x] [x] [x] Trie (retrieval tree) / Prefix Trie  
- Node-links + end of word flag  
- Space vs. time trade offs  

[x] [x] [ ] Suffix Trie  
- Naive O(n^2) construction / pattern search in O(m)  

[x] [x] [ ] Suffix Tree  
- Ukkonen’s linear-time construction idea (optional)  
- But at least know suffix links / edge-label compression  

[x] [x] [x] Suffix Array  
- Naive O(n^2 log n) via sorting all suffixes vs. prefix-doubling O(n log n)  
- Pattern matching using suffix array + LCP array (O(m + log n))  

## W11: Search Trees

[x] [x] [ ] Problems with Imbalanced Binary Search Trees  
- Degenerate Θ(n) for sorted input  

[x] [x] [x] AVL Trees  
- AVL balance criteria  
- Rotations: LL, RR, LR, RL  

[x] [x] [x] Perfectly Balanced 2-3 Search Trees  
- 3-way nodes  
- Guaranteed height log(n)  

[x] [x] [ ] Left-Leaning Red-Black Trees  
- Colour-link invariants  
- Single- and double-rotations  