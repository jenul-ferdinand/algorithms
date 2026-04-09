from typing import List, Tuple

# Types
Edge = Tuple[int, int]
Vertex = int
Boolean = bool

# Constants for the two colours
BLACK = 0
WHITE = 1

def is_two_colourable(edges: List[Edge]) -> Boolean:
    """
    Checks if a graph is two colourable.
    
    Uses a depth first search to colour each vertex of the graph. If two
    adjacent vertices have the same colour, then we know that the graph is not
    two colourable.  
    
    Args:
    - edges: A list of edges represented as tuples (u, v)
    in a list.
    
    Time Complexity: O(E + E + V+E) -> O(V+E)
    Space Complexity: O(V+E + V + V) -> O(V + E)
    - Where V is the number of vertices.
    - Where E is the number of edges.
    """
    # Find number of nodes (from edges)
    V = 0
    for u, v in edges: 
        V = max(V, u, v)
    V += 1
    
    # Create graph adjacency list
    graph = [[] for i in range(V)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
        
    # Create colour array (index = vertex id)
    colours: List[int] = [None] * V
    
    # Initial colour of starting node is BLACK (0)
    colours[0] = BLACK
    
    # Starting node is in stack
    stack = [0]
    
    # DFS
    while stack:
        # Pop a node from the stack
        curr = stack.pop()
        
        # Check each neighbour of current node
        for neighbour in graph[curr]:
            
            # Assign the opposite colour to neighbour 
            if colours[neighbour] is None:
                colours[neighbour] = 1 - colours[curr]
                stack.append(neighbour)
            
            # Not colourable if the colour of neighbour is same as ours
            elif colours[neighbour] == colours[curr]:
                return False

    # No conflicts, so colourable
    return True
            
        

if __name__ == '__main__':
    # Not two colourable (odd cycle)
    edges = [
        (0, 1),
        (1, 2),
        (2, 0)
    ]
    res = is_two_colourable(edges)
    assert res == False, f'Expected False, but got {res}'
    
    # Two colourable (even cycle)
    edges = [
        (0,1),
        (1,2),
        (2,3),
        (3,0)
    ]
    res = is_two_colourable(edges)
    assert res == True, f'Expected True, but got {res}'
    
    # Disconnected graph, each part bipartite
    edges = [
        (0,1),
        (2,3),
        (3,4)
    ]
    res = is_two_colourable(edges)
    assert res == True, f'Expected True, but got {res}'
    
    print("All tests passed")