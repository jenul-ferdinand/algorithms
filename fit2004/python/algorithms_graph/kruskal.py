
#? =============================================================================|
#? PACKAGES
#? =============================================================================|

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_structures.UnionFind import UnionFind

from typing import List, Tuple

#! =============================================================================|
#! KRUSKAL'S ALGORITHM
#! =============================================================================|

def kruskal(edges: List[Tuple[int,int,int]]) -> List[Tuple[int,int,int]]:
    """
    Kruskal's MST algorithm
    
    Description:
        Given an undirected, weighted graph representted as a list of edges
        (u,v,w) over vertices labelled 1..n, this function computes a minimum
        spanning forest. If the graph is connected, the result is its unique
        (modulo equal-weight ties) minimum spanning tree.
        
    Approach:
        1. We first determine the maximum vertex label n to size UnionFind.
        2. Sort all edges by weight once in O(E log E)
        3. Iterate edges in ascending order:
            - use `find` the check connectivity: O(a(V))
            - If in different sets, `union` them and append to MST.
        4. At most V-1 edges are added to the MST.
    
    Args:
        - edges: List of undirected edges (u,v,w), 1-based vertices

    Returns:
        List of edges (u,v,w) in the minimum spanning tree.
    
    Time Complexity: O(E log V)
    Time Complexity Analysis:
        Let V = number of vertices and E = number of edges.
        - Sorting edges by weight: O(E log E)
        - Union-Find operations for each edge: O(E * a(V))
        where a(V) is the inverse Ackermann function (pretty much constant).
    
    Auxiliary Space Complexity: O(E + V)
    Auxiliary Space Complexity Analysis:
        - Storing input edges and sorted list: O(E)
        - Union-Find parent array: O(V)
        - Output MST list: O(V)
    """
    n = 0
    for u,v,_ in edges:
        n = max(n, u, v)
    n += 1
    
    # Sort edges ascending by weight
    sorted_edges = sorted(edges, key = lambda x: x[2])
    
    forest = UnionFind(n)
    mst = []
    
    for u,v,w in sorted_edges:
        # If u and v are in different components, take this edge
        if forest.find(u) != forest.find(v):
            forest.union(u,v)
            mst.append((u,v,w))
    
    return mst



#? =============================================================================|
#? TESTING
#? =============================================================================|

if __name__ == '__main__':
    # Simple test graph:
    #   1—2 (1)
    #   1—3 (4)
    #   2—3 (2)
    #   2—4 (7)
    #   3—5 (3)
    #   4—5 (5)
    edges = [
        (1, 2, 1),
        (1, 3, 4),
        (2, 3, 2),
        (2, 4, 7),
        (3, 5, 3),
        (4, 5, 5),
    ]

    mst = kruskal(edges)
    print("MST edges:", mst)
    exp = [(1,2,1), (2,3,2), (3,5,3), (4,5,5)]
    print("Expected edges:", exp)
    assert mst == exp, f'Expected {exp}, got {mst}'
    # Expected MST (total weight = 1+2+3+5 = 11), order may vary:
    # [(1,2,1), (2,3,2), (3,5,3), (4,5,5)]
    print('All tests passed')