from typing import List, Tuple

"""
? Name: Detect Cycle in Undirected Graph

? Description:
Given an undirected graph with n vertices 0 to n-1 and a list of edges.

Determine whether the garph contains any cycle. 

A cycle in an undirected graph is a path that starts and ends at the same 
vertex, with at least one edge, and with no edge repeated.

- Track the "parent" of each DFS step to avoid falsely treating the immediate 
back-edge as a cycle.

? Input:
- n: An integer, the number of vertices.
- edges: A list of m tuples (u,v).

? Output: 
- Return True if there is at least one cycle in the graph, False otherwise.
"""

def cycle_find(n: int, edges: List[Tuple[int, int]]) -> bool:
    """
    Checks if a cycle exists in a given undirected graph.
    
    A cycle in an undirected graph is a path that starts and ends at the same
    vertex, with at least one edge, and with no edge repeated.
    
    Time Complexity: O(V + E)
    Aux Space Complexity: O(V + E)
    """
    adj = [[] for _ in range(n)]
    for u,v in edges:
        adj[u].append(v)
        adj[v].append(u)
        
    visited = [False] * n
    found = False
        
    def dfs(node: int, parent: int):
        """Depth-First Search"""
        nonlocal found
        visited[node] = True
        
        for neighbour in adj[node]:
            if not visited[neighbour]:
                dfs(neighbour, node)
                if found:
                    return
            else:
                if neighbour != parent:
                    found = True
                    return
    
    # Run DFS from every unvisited node
    for u in range(n):
        if not visited[u]:
            dfs(u, parent=-1)
            
            if found:
                return True
            
    return False

if __name__ == "__main__":
    # Example 1: Graph with a cycle
    #    n = 4
    #    edges = [(0,1), (1,2), (2,0), (2,3)]
    #    This contains the cycle 0–1–2–0, so output should be True
    n1 = 4
    edges1 = [(0, 1), (1, 2), (2, 0), (2, 3)]
    assert cycle_find(n1, edges1) == True, f'Expected True, got False'

    # Example 2: Acyclic graph (forest)
    #    n = 5
    #    edges = [(0,1), (1,2), (3,4)]
    #    No cycles exist, so output should be False
    n2 = 5
    edges2 = [(0, 1), (1, 2), (3, 4)]
    assert cycle_find(n2, edges2) == False, f'Expected False, got True'
    
    print('All tests passed!')