from typing import List, Tuple, Set
import heapq
import math

INF = math.inf

def prims(edges: List[Tuple[int, int, int]], root: int):
    """
    Prim's algorithm to compute a MST of a connected, undirected graph

    Time Complexity: O(E log V)
    Aux Space Complexity: O(V + E)
    """
    # Find V and build adj list
    V = 0
    for u,v,_ in edges:
        V = max(V, u, v)
    V += 1
    
    adj = [[] for _ in range(V)]
    for u,v,w in edges:
        adj[u].append((v,w))
        adj[v].append((u,w))    
    
    # Initialise dist, parent and visited set
    dist = [INF] * V
    parent = [None] * V
    dist[root] = 0
    
    visited = set()
    mst_edges = []
    
    # Priority queue of (dist, node)
    min_heap = [(0, root)]
    
    while min_heap:
        d_u, u = heapq.heappop(min_heap)
        
        # Skip outdated entries
        if u in visited or d_u > dist[u]:
            continue
        
        # Mark u as added to the MST
        visited.add(u)
        # If u is not the root, record the edge from parent[u]
        if parent[u] is not None:
            mst_edges.append((parent[u], u, int(dist[u])))
        
        # Relax edges (u,v)
        for v, weight in adj[u]:
            if v not in visited and weight < dist[v]:
                dist[v] = weight
                parent[v] = u
                heapq.heappush(min_heap, (weight, v))
                
    return visited, mst_edges

if __name__ == '__main__':
    # Example usage / simple test
    edges = [
        (0, 1, 4),
        (0, 2, 3),
        (1, 2, 1),
        (1, 3, 2),
        (2, 3, 4),
        (3, 4, 2),
        (4, 5, 6)
    ]
    vertices, mst = prims(edges, root=0)
    print("MST vertices:", vertices)
    print("MST edges:", mst)
    # Expected MST edges (order may vary):
    # [(0,2,3), (2,1,1), (1,3,2), (3,4,2), (4,5,6)]
    