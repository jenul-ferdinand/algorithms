from typing import List, Tuple

Weight = int
Node = int
Edge = Tuple[Weight, Node, Node]

def transitive_closure(edges: List[Edge]) -> List[List[bool]]:
    """ 
    ! Computes the transitive closure of a graph
    
    Args: 
        edges: A list of edges, where each edge is (weight, u, v).
                Nodes u and v are assumed to be 0-indexed.
                
    Returns:
        A 2D boolean matrix where matrix[i][j] is True if there is a path
        from node i to node j, and False otherwise.
    """
    # Find the maximum number of vertices
    V = 0
    for edge in edges:
        V = max(V, edge[1], edge[2])
    V += 1
    
    # Initialize adjacency matrix to track reachability between vertices
    connected = [[False] * V for _ in range(V)]
    
    # Vertices are connected to themselves (path of length 0)
    for node in range(V):
        connected[node][node] = True

    # Edges connect their corresponding vertices (path of length 1)
    for edge in edges:
        _, u, v = edge
        
        connected[u][v] = True
    
    # Core logic
    for k in range(V): # Intermediate vertex
        for u in range(V): # Source vertex
            for v in range(V): # Destination vertex
                # Is there a path from u to v OR a path from u to k and k to v?
                connected[u][v] = connected[u][v] or (connected[u][k] and connected[k][v])
                
    return connected

if __name__ == '__main__':
    # Example graph edges (weight is irrelevant here, set to 1)
    edges = [
        (1, 0, 1),
        (1, 1, 2),
        (1, 3, 0)
    ]
    
    # Expected paths:
    # 0 -> 1 -> 2
    # 3 -> 0 -> 1 -> 2 
    
    print("Example edges")
    print(edges)
    
    matrix = transitive_closure(edges)
    
    print('\nTransitive Closure Matrix:')
    for row in matrix:
        print([f'{x:5}' for x in row])