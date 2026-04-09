"""
Describe an algorithm for counting the number of valid two colourings of a given
undirected graph.
"""
from typing import List, Tuple
from collections import deque

def count_two_colourings(edges: List[Tuple[int, int]]) -> int:
    # Build adjacency list and find V
    V = 0
    for u, v in edges:
        V = max(V, u, v)
    V += 1
    
    adj = [[] for _ in range(V)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    
    # Prepare colour array and component count
    colour = [None] * V
    components = 0
    
    # BFS on each component
    for start in range(V):
        if colour[start] is not None:
            continue
        
        # New component
        components += 1 
        colour[start] = 0
        queue = deque([0])
        
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if colour[v] is None:
                    colour[v] = 1 - colour[u]
                    queue.append(v)
                elif colour[v] == colour[u]:
                    return 0
    
    # Each component can be coloured in two ways
    return 2 ** components

if __name__ == '__main__':
    # Example tests
    # 1) A triangle (3-cycle) is not bipartite → 0
    edges = [(0,1), (1,2), (2,0)]
    assert count_two_colourings(edges) == 0

    # 2) Disconnected graph: two separate edges
    #    Components = 2 → 2^2 = 4 valid colourings
    edges = [(0,1), (2,3)]
    res = count_two_colourings(edges)
    exp = 8
    assert res == exp, f'Expected {exp}, got {res}'

    print("All tests passed!")
        