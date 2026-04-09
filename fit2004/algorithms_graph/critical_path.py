from typing import List, Tuple, Optional

Weight = int
Vertex = int
Edge = Tuple[Weight, Vertex, Vertex]
AdjacencyList = List[List[Tuple[Weight, Vertex]]]
Memo = List[Optional[Weight]]

def critical_path(edges: List[Edge], start_vertex: Vertex):
    """
    Calculates the length of the longest path (critical path) in a DAG
    starting from a given node using recursion with memoisation.
    
    Args:
        edges: A list of edges, where each edge is (weight, u, v).
                Nodes u and v are assumed to be 0-indexed.
                
        start_node: The node from which to start finding the longest path.
        
    Returns:
        The length of the longest path starting from start_node.
        Returns 0 if the start_node has no outgoing paths or doesn't exist.
        Raises ValueError if the graph contains cycles (not checked here, 
        assumes DAG)
        
    Time Complexity: O(V + E)
        The dominant factors are O(V + E) for graph construction and O(V + E)
        for the memoised recursion.
        
    Space Complexity: O(V + E)
    Space Complexity (auxiliary): O(V + E)
        The space is dominated by the adjacency list and potentially the call
        stack/memo table.
    """
    # Find n (number of vertices = max_index + 1)
    n = -1
    for edge in edges:
        n = max(n, edge[1], edge[2])
    n += 1
    
    # Init graph as an adjacency list
    graph: AdjacencyList = [[] for _ in range(n)]
    for edge in edges:
        w, u, v = edge
        graph[u].append((w, v))
        
    # Initialise memoisation table (using dictionary here)
    longest: Memo = [None] * n
    
    def find_longest_path(curr_vertex: Vertex, graph: AdjacencyList, longest: Memo) -> Weight:
        """Recursive helper function to find the longest path starting from curr_node"""
        # * 1. Check memoisation table (base case for recursion)
        if longest[curr_vertex] is not None:
            return longest[curr_vertex]
        
        # * 2. Recursive step: Calculate longest path from this vertex
        # Longest path *from* this vertex is 0 if it's a sink
        max_len = 0 
        # Iterate through outgoing edges from curr_vertex
        for weight, neighbour in graph[curr_vertex]:
            # Recursively find the longest path starting from the neighbour
            path_from_neighbour = find_longest_path(neighbour, graph, longest)
            
            # Update the maximum length found so far starting from curr_vertex
            max_len = max(max_len, weight + path_from_neighbour)
                
        # * 3. Store result in memoisation table before returning
        longest[curr_vertex] = max_len
        return max_len
    
    # Start the recursive calculation from the start_vertex
    result = find_longest_path(start_vertex, graph, longest)
    return result




if __name__ == '__main__':
    # Example DAG edges: (weight, u, v)
    dag_edges = [
        (5, 0, 1),
        (3, 0, 2),
        (6, 1, 3),
        (7, 1, 4),
        (4, 2, 3),
        (2, 2, 4),
        (1, 3, 5),
        (8, 4, 5)
    ]
    start = 0
    longest = critical_path(dag_edges, start)
    # Expected paths from 0:
    # 0 -> 1 -> 3 -> 5: 5 + 6 + 1 = 12
    # 0 -> 1 -> 4 -> 5: 5 + 7 + 8 = 20
    # 0 -> 2 -> 3 -> 5: 3 + 4 + 1 = 8
    # 0 -> 2 -> 4 -> 5: 3 + 2 + 8 = 13
    # Longest is 20
    print(f"Longest path (critical path) starting from node {start}: {longest}") # Expected: 20

    start = 1
    longest = critical_path(dag_edges, start)
    # Expected paths from 1:
    # 1 -> 3 -> 5: 6 + 1 = 7
    # 1 -> 4 -> 5: 7 + 8 = 15
    # Longest is 15
    print(f"Longest path (critical path) starting from node {start}: {longest}") # Expected: 15
    
    start = 5 # Sink node
    longest = critical_path(dag_edges, start)
    print(f"Longest path (critical path) starting from node {start}: {longest}") # Expected: 0