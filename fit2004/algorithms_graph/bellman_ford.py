from typing import List, Tuple

Weight = int
Node = int
Edge = Tuple[Weight, Node, Node]

INF = float('inf')

def bellman_ford(edges: List[Edge], s: Node) -> Tuple[List, List]:
    """
    ! Finds shortest paths from source s using Bellman-Ford
    
    Args:
        edges: List of edges in the format (weight, u, v)
        s: The source node index (0-based)
        v: Optional. The total number of vertices. If None, inferred from edges.
        
    Returns:
        A tuple (dist, pred)
        dist[i] is the shortest distance from s to i.
        pred[i] is the predecessor of i in the shortest path from s
        Raises ValueError if a negative cycle is detected
    """
    # Find maximum no. of vertices
    V = 0
    for edge in edges:
        V = max(V, edge[1], edge[2])
    V += 1
    
    # Setup distance and predecessor lists
    dist = [INF for _ in range(V)]
    pred = [None for _ in range(V)]
    
    # Starting vertex distance is zero
    dist[s] = 0
    
    # * --- Main Relaxation Phase ---
    # Iterate V-1 times
    for _ in range(V-1):
        for edge in edges:
            w, u, v = edge
            
            # Check if path through u is shorter AND path to u exists
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u
                
    # * --- Negative Cycle Detection Phase ---
    # Perform one more pass through all edges
    for edge in edges:
        w, u, v = edge
        if dist[u] != INF and dist[u] + w < dist[v]:
            # If we can still relax an edge, a negative cycle exists
            raise ValueError('Graph contains a negative-weight cycle reachable from the source')
    
    return dist, pred
    


if __name__ == '__main__':
    # Normal graph with cycle
    edges = [
        (6, 0, 1),
        (7, 0, 2),
        (5, 1, 2),
        (8, 1, 3), 
        (4, 1, 4),
        (2, 2, 3),
        (3, 3, 4), 
        (9, 3, 1), # Note: edge (3,1) creates a cycle
        (7, 4, 0), 
        (2, 4, 3) 
    ]
    source = 0
    
    try:
        distances, predecessors = bellman_ford(edges, source)
        print(f'Distances from source {source}: {distances}')
        print(f'Predecessors: {predecessors}')
        
        # Example: Reconstruct path to node 3
        path = []
        curr = 3 
        while curr is not None:
            path.append(curr)
            curr = predecessors[curr]
        path.reverse()
        print(f'Example: Shortest path to node 3: {path}')
        
    except ValueError as e:
        print(f'Error: {e}')
        
        
        
    # Graph with negative cycle
    edges = [
        (1, 0, 1),
        (1, 1, 2),
        (-3, 2, 0)
    ]
    source = 0
    print(f'\nTesting with negative cycle:')
    try:
        bellman_ford(edges, source)
    except ValueError as e:
        print(f'Caught excepted error: {e}')