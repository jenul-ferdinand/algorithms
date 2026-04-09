from typing import List, Tuple, Optional
from collections import deque

def build_adjacency_matrix(edges: List[Tuple[int, int, int]]):
    """
    Building an adjacency matrix of directed, weighted graph.
    
    Time Complexity: O(V^2 + E) = O(V^2)
    Time Complexity Analysis: 
        - Scan edges to find max node ID: O(E)
        - Initialise VxV matrix: O(V^2)
        - Populate matrix from edges: O(E)
    
    Aux Space Complexity: O(V^2)
    Aux Space Complexity Analysis:
        - Storing the VxV matrix
    """
    V = 0
    for v, u, _ in edges:
        V = max(V, v, u)
    V += 1
    
    # Initialise empty VxV matrix with all zeros
    matrix = [[None] * V for _ in range(V)]
    
    # Populate the matrix based on the edges input
    for u, v, w in edges:
        matrix[u][v] = w
        
    return matrix
        
def total_weight_sum_incoming(matrix: List[List[int]], node: int) -> int:
    """
    Sum the weights of all edges incoming to a node
    
    Time Complexity: O(V)
    Time Complexity Analysis:
        - One scan of the column.
    
    Aux Space Complexity: O(1)
    Aux Space Complexity Analysis:
        - Constant extra space.
    """
    V = len(matrix)
    
    total = 0
    for u in range(V):
        total += matrix[u][node] 
        
    return total
    
def check_edge_connection(matrix: List[List[int]], u: int, v: int) -> Optional[int]:
    """
    Check for the existence (and weight) of an edge u -> v
    
    Time Complexity: O(1)
    Aux Space Complexity: O(1)
    """
    return matrix[u][v]

def get_neighbours(matrix: List[List[int]], u: int) -> Optional[List[int]]:
    """
    List all outgoing neighbours of vertex u
    
    Time Complexity: O(V)
    Time Complexity Analysis:
        - Scan one row of length V
        
    Aux Space Complexity: O(V)
    Aux Space Complexity Anaysis:
        - In the worst case, every entry is a neighbour
    """
    V = len(matrix)
    neighbours = []
    
    for v in range(V):
        if matrix[u][v] is not None:
            neighbours.append(v)
    
    return neighbours

def bfs_matrix(matrix: List[List[int]], source: int):
    """
    BFS using adjacency matrix instead
    
    Time Complexity: O(V^2) instead of O(V + E) using adjacency list
    Time Complexity Analysis:
        - Each of V queue pops scans O(V) neighbours
    
    Aux Space Complexity: O(V)
    Aux Space Complexity Analysis:
        - Visited array + queue of up to V elements.
    """
    V = len(matrix)
    visited = [False] * V
    visited[source] = True
    
    queue = deque([source])
    while queue:
        u = queue.popleft()
        
        neighbours = get_neighbours(matrix, u) # O(V)
        for v in neighbours:
            if not visited[v]:
                visited[v] = True
                queue.append(v)
                
    return visited
        
if __name__ == '__main__':
    pass