from typing import List, Tuple
from collections import deque

"""
? Name:
Shortest Distances in an Unweighted Graph

? Description:
Given an undirected graph with n vertices (0 to n-1) and a list of edges.

Compute the shortest distance (in number of edges) from a given source vertex
to every other vertex. 

If a vertex is not reachable from the source, its distance should be -1. 

You must implement a BFS without using python dicts or sets. Only lists, and a 
queue

? Input:
- n: the number of vertices (integer)
- edges: a list of tuples (u,v) representing the edges.
- source: the source node to start the BFS (integer)

? Output
A list `dist` of length n, where dist[i] is the shortest distance (no. of edges)
from `source` to vertex `i`. 

If vertex `i` is unreachable from `source`, then `dist[i]=-1`
"""

def shortest_distances(
    n: int, 
    edges: List[Tuple[int, int]], 
    source: int
) -> List[int]:
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u,v in edges:
        adj[u].append(v)
        adj[v].append(u)
    
    # Initialise states
    visited = [False] * n
    dist = [-1] * n
    queue = deque(); 
    
    # Set the initial states
    visited[source] = True
    dist[source] = 0
    queue.append(source)
    
    # BFS while queue not empty
    while queue:
        current = queue.popleft()
        
        # Adding neighbours to queue
        for neighbour in adj[current]:
            if not visited[neighbour]:
                visited[neighbour] = True
                dist[neighbour] = dist[current] + 1
                queue.append(neighbour)
                
    return dist

if __name__ == '__main__':
    # Example Test Case:
    #
    # n = 6
    # edges = [
    #   (0, 1),
    #   (1, 2),
    #   (2, 3),
    #   (3, 4),
    #   (4, 5)
    # ]
    # source = 0
    #
    # The graph is a simple path: 0–1–2–3–4–5.
    # Distances from source=0:
    #   dist[0] = 0
    #   dist[1] = 1
    #   dist[2] = 2
    #   dist[3] = 3
    #   dist[4] = 4
    #   dist[5] = 5
    #
    # If we pick source=3 instead, distances become:
    #   dist = [3, 2, 1, 0, 1, 2]
    #
    # Let’s test both scenarios.

    # First scenario: source = 0
    n = 6
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]
    source = 0
    dist_from_0 = shortest_distances(n, edges, source)
    exp = [0,1,2,3,4,5]
    assert dist_from_0 == exp, f'Expected {exp}, got {dist_from_0}'

    # Second scenario: source = 3
    source = 3
    dist_from_3 = shortest_distances(n, edges, source)
    # Expected: [3, 2, 1, 0, 1, 2]
    assert dist_from_3 == [3,2,1,0,1,2]

    # A more complex example with two components:
    #   n = 7
    #   edges = [(0,1),(1,2),(3,4),(4,5),(5,3)]
    #   source = 0
    # Component {0,1,2} is a path; component {3,4,5} is a triangle; vertex 6 is isolated.
    # Distances from source=0:
    #   dist[0]=0, dist[1]=1, dist[2]=2, dist[3]=dist[4]=dist[5]=dist[6]=-1
    n2 = 7
    edges2 = [(0,1), (1,2), (3,4), (4,5), (5,3)]
    source2 = 0
    assert shortest_distances(n2, edges2, source2) == [0,1,2,-1,-1,-1,-1]
    
    print('All tests passed!')