from typing import List, Tuple
from heapq import heappop
from heapq import heappush

def dijkstra(edges: List[Tuple[int, int, int]], start):
    # Find the no of nodes
    max_node = 0
    for edge in edges:
        max_node = max(max_node, edge[0], edge[1])
    
    # Build the adjacency matrix
    adj = {}
    for i in range(max_node):
        adj[i] = []
        
    for u, v, weight in edges:
        adj[u].append([v, weight])
        
    # Map of shortest paths from source to node (init as infinity)
    shortest = {i: float('inf') for i in range(max_node)}
    shortest[start] = 0
    
    # Priority queue to explore nodes, starting from the source
    min_heap = [(start, 0)] # (node, weight)
    
    while min_heap:
        node, weight = heappop(min_heap)

        # Only proceed if the current path is still relevant
        if weight > shortest[node]:
            continue
        
        for new_node, new_weight in adj[node]:
            new_dist = weight + new_weight
            if new_dist < shortest[new_node]:
                shortest[new_node] = new_dist
                heappush(min_heap, (new_node, new_dist))
        
        # Check for any nodes that were not reachable
        for i in range(max_node):
            if shortest[i] == float('inf'):
                shortest[i] = -1
                
    return shortest
        
    
    

if __name__ == '__main__':
    pass