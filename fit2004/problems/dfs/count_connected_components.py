from typing import List, Tuple

"""
? Problem Description:
Given an undirected graph with n vertices (labelled 0 -> n - 1) and m edges.

Count how many connected components the graph has. 

A connected component is a maximal set of vertices such that each pair of 
vertices in that set is joined by a path. 

You must implement a DFS

? Input:
n: the number of vertices
edges: a list of tuples representing edges
"""

def count_connected_components(n: int, edges: List[Tuple[int, int]]) -> int:
    """
    Counts the number of connected components in a given graph.
    
    A connected component is a maximal set of vertices such that each pair of
    vertices in that set is joined by a path.
    
    Time Complexity: O(V + E)
    Time Complexity Analysis:
    - O(E) for building the adjacency list.
    - O(V + E) for DFS.
    
    Aux Space Complexity: O(V + E)
    Aux Space Complexity Analysis:
    - O(V + E) for the adjacency list.
    - O(V) for DFS
    
    Terms:
    - V is the number of nodes.
    - E is the number of edges.
    """
    adj = [[] for _ in range(n)]
    for u,v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = [False] * n 
    components = 0 
    
    def dfs(u: int):
        visited[u] = True
        
        for neighbour in adj[u]:
            if not visited[neighbour]:
                dfs(neighbour)
    
    for vertex in range(n):
        if not visited[vertex]:
            components += 1
            dfs(vertex)

    return components

if __name__ == '__main__':
    # Example:
    #   n = 6
    #   edges = [(0,1), (1,2), (3,4), (4,5)]
    # This graph has two connected components:
    #   {0,1,2}  and  {3,4,5}
    n = 6
    edges = [(0, 1), (1, 2), (3, 4), (4, 5)]
    res = count_connected_components(n, edges)   # Expected output: 2
    assert res == 2, f'Expected 2, got {res}'
    
    print('Tests passed!')