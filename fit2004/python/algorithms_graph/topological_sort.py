from typing import List

def topological_sort(adj: List[List[int]]) -> List[int]:
    """
    Perform a topological sort on a directed acyclic graph using DFS.
    """
    V = len(adj)
    visited = [False] * V
    res = []
    
    def dfs(u: int):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs(v)
                
        res.append(u)
        
    for u in range(V):
        if not visited[u]:
            dfs(u)
            
    return res[::-1]

if __name__ == '__main__':
    # Graph:
    # 5 → 2 → 3
    # 5 → 0
    # 4 → 0, 4 → 1
    adj = {
        5: [2, 0],
        4: [0, 1],
        2: [3],
        3: [],
        1: [],
        0: []
    }
    # Convert dict to list-of-lists
    V = max(adj) + 1
    adj_list: List[List[int]] = [[] for _ in range(V)]
    for u, nbrs in adj.items():
        adj_list[u] = nbrs

    order = topological_sort(adj_list)
    print("Topological order:", order)
    # Possible valid output: [4,5,1,2,0,3] (or any order respecting dependencies)