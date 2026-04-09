import sys
import os
from typing import List, Optional, Tuple

class Edge:
    def __init__(self, to: int, capacity: int):
        self.to = to
        self.capacity = capacity
        self.flow = 0
        self.reverse: Optional[Edge] = None
        
Graph = List[List[Edge]]
INFINITY = float('inf')

def _build_graph(num_vertices: int, edges: List[Tuple[int, int, int]]) -> Graph:
    """Builds the residual graph structure with forward and backward edges"""
    graph: Graph = [[] for _ in range(num_vertices)]
    for u, v, capacity in edges:
        # Create forward edge
        forward_edge = Edge(to=v, capacity=capacity)
        # Create backward edge (capacity 0, flow will be negative of forward)
        backward_edge = Edge(to=u, capacity=0)
        
        # Link the edges
        forward_edge.reverse = backward_edge
        backward_edge.reverse = forward_edge
        
        # Add edges to the adjacency list
        graph[u].append(forward_edge)
        graph[v].append(backward_edge)
    return graph

def _dfs(u: int, t: int, bottleneck: float, graph: Graph, visited: List[bool]) -> float:
    """
    Performs DFS to find an augmenting path and augments flow simultaneously.
    
    Args:
        u: Current vertex.
        t: Target (sink) vertex.
        bottleneck: The maximum flow that can be pushed through the path found so far.
        graph: The residual graph (adjacency list).
        visited: List to keep track of visited nodes in the current DFS traversal.
        
    Returns:
        The amount of flow augmented by the path found (0 if no path found from u)
    """
    # Base case: Reached the sink
    if u == t:
        return bottleneck
    
    visited[u] = True

    # Explore neighbours
    for edge in graph[u]:
        residual_capacity = edge.capacity - edge.flow
        v = edge.to
        
        # Check if we can push flow and haven't visited the neighbour yet
        if residual_capacity > 0 and not visited[v]:
            # Recursively call DFS on the neighbour
            # The new bottleneck is the minimum of the current bottleneck and the residual capacity
            augment = _dfs(v, t, min(bottleneck, residual_capacity), graph, visited)
            
            # If we found an augmenting path from the neighbour (augment > 0)
            if augment > 0:
                # Augment the flow on the current edge
                edge.flow += augment

                # Decrease the flow on the reverse edge (maintaining invariant)
                # Ensure reverse edge exists before acccessing its flow
                if edge.reverse:
                    edge.reverse.flow -= augment
                else:
                    # This case should ideally not happen if graph is built correctly
                    print(f'Warning: Reverse edge not found for edge to {edge.to} from {u}')
                    
                return augment # Return the augmented flow
    
    # No augmenting path found from this vertex u
    return 0 

def ford_fulkerson(num_vertices: int, edges: List[Tuple[int, int, int]], s: int, t: int) -> float:
    """
    Calculates the maximum flow from source s to sink t using Ford-Fulkerson with DFS
    
    Args:
        num_vertices: The total number of vertices in the graph (labeled 0 to n-1)
        edges: A list of tuples representing directed edges: (u, v, capacity)
        s: The source vertex index
        t: The sink (target) vertex index
        
    Returns:
        The maximum flow value from s to t
    """
    graph = _build_graph(num_vertices, edges)
    max_flow = 0.0
    
    while True:
        # Reset visited array for each new DFS path search
        visited = [False] * num_vertices

        # Try to find an augmenting path from s to t with infinite inital bottleneck
        augmented_flow = _dfs(s, t, INFINITY, graph, visited)
        
        # If no augmenting path was found, we are done
        if augmented_flow == 0:
            break
        
        # Add the flow found in this path to the total max flow
        max_flow += augmented_flow
        
    return max_flow
        
        
if __name__ == '__main__':
    # Example from Michael Sambol's YT Video: https://youtu.be/Tl90tNtKvxs
    n = 6
    edges = [
        (0, 1, 10),
        (1, 2, 4),
        (2, 5, 10),
        (1, 3, 2),
        (1, 4, 8),
        (3, 4, 9),
        (4, 5, 10),
        (4, 2, 6)
    ]
    source = 0
    sink = 5
    max_flow = ford_fulkerson(n, edges, source, sink)
    print(f'Example from Michael Sambols YT Video')
    print(f'Number of vertices: {n}')
    print(f'Edges (u, v, capacity): {edges}')
    print(f'Source: {source}, Sink: {sink}')
    print(f'Maximum Flow: {max_flow}\n\n')
    
    # Example from Kindson's YT Video: https://youtu.be/MIauBXEu3BU
    n = 4
    edges = [
        (0, 1, 20), (0, 2, 10),
        (1, 2, 30),
        (1, 3, 10), (2, 3, 20)
    ]
    source = 0
    sink = 3
    max_flow = ford_fulkerson(n, edges, source, sink)
    print(f'Example from Kindsons YT Video')
    print(f'Number of vertices: {n}')
    print(f'Edges (u, v, capacity): {edges}')
    print(f'Source: {source}, Sink: {sink}')
    print(f'Maximum Flow: {max_flow}\n\n')
    
    # Example from W9 Preparation Sheet
    n = 6
    edges = [
        (0, 1, 3), (0, 2, 4),
        (1, 2, 1),
        (1, 3, 5), (2, 4, 4),
        (4, 1, 4),
        (3, 4, 1),
        (3, 5, 5), (4, 5, 3)
    ]
    source = 0
    sink = 5
    max_flow = ford_fulkerson(n, edges, source, sink)
    print(f'Example from W9 Preparation Sheet')
    print(f'Number of vertices: {n}')
    print(f'Edges (u, v, capacity): {edges}')
    print(f'Source: {source}, Sink: {sink}')
    print(f'Maximum Flow: {max_flow}')    
    

