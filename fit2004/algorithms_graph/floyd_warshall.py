from typing import List, Tuple

Weight = int
Node = int
Edge = Tuple[Weight, Node, Node]

INF = float('inf')

def floyd_warshall(edges: List[Edge]):
    """
    Floyd Warshall All Pairs Shortest Path
    
    Time Complexity: O(V^3)
    Space Complexity (auxiliary): O(V^2)
    """
    # Find the maximum vertex
    V = 0
    for edge in edges:
        V = max(V, edge[1], edge[2])
    # No of vertices = max node + 1
    V += 1
    
    # The shortest distance matrix 
    dist: List[List[int]] = [[INF] * V for _ in range(V)]
    
    for v in range(V):
        dist[v][v] = 0
        
    print(dist)
    
    for w, u, v in edges:
        dist[u][v] = min(dist[u][v], w)
        
    for k in range(V): # Intermediate vertex
        for u in range(V): # Source vertex
            for v in range(V): # Destinatino vertex
                dist[u][v] = min(dist[u][v], dist[u][k] + dist[k][v])
                
    return dist
    
if __name__ == '__main__':
    edges = [
        (3, 0, 1),
        (8, 0, 3),
        (-4, 1, 2),
        (1, 2, 0),
        (2, 2, 0),
        (5, 3, 1)
    ]
    
    shortest_paths = floyd_warshall(edges)
    
    print("\nShortest paths matrix (Directed):")
    for row in shortest_paths:
        print([f'{x:5}' for x in row])
    
    print('\nIndividual shortest paths:')
    V = len(shortest_paths)
    for u in range(V):
        for v in range(V):
            distance = shortest_paths[u][v]
            if distance == INF:
                print(f'Shortest path from node {u} to {v} has no path')
            else: 
                print(f'Shortest path from node {u} to {v} has distance {distance}')