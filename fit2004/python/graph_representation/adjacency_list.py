from typing import List, Tuple, Optional
from collections import deque

def build_adjacency_list(edges: List[Tuple[int, int, int]]):
    """
    Build the adjacency list of a directed, weighted graph
    
    Time Complexity: O(V + E)
    Time Complexity Analysis:
        - Scan edges to find max node ID: O(E)
        - Initialise adjcancy list of V inner lists: O(V)
        - Populate the adjacency list with entries into the inner lists: O(E)
        
    Aux Space Complexity: O(V + E)
    Aux Space Complexity Analysis:
        - A list with V entries each with inner lists of E size.
    """
    V = 0
    for u,v,_ in edges:
        V = max(V, u, v)
    V += 1
    
    adj = [[] for _ in range(V)]
    for u,v,w in edges:
        adj[u].append((v,w))
        
    return adj

def get_outgoing_edges_of_node(adj: List[List[Tuple[int, int]]], u: int) -> List[int]:
    """
    Gets the outgoing edges from a given node in an adjacency list
    
    Time Complexity: O(degree(u))
    Time Complexity Analysis:
        - Scans only the list of outgoing edges for node u
    
    Aux Space Complexity: O(degree(u))
    Aux Space Complexity Analysis:
        - The returned list contains one tuple per outgoing edge
    """
    output = []
    for v, w in adj[u]:
        output.append((v, w))
    
    return output

def in_degree(adj, u):
    """
    Returns the number of edges COMING INTO node `u`
    
    Time Complexity: O(V + E) = O(E) for connected graphs
    Time Complexity Analysis:
        - You scan each node's outgoing list once.
        
    Aux Space Complexity: O(1)
    """
    count = 0 
    
    for src_edges in adj:
        for (dest, _) in src_edges:
            if dest == u:
                count += 1
    
    return count

def has_edge(adj, u, v):
    """
    Checks whether there is an edge u -> v and returns the weight if there is.
    
    Time Complexity: O(degree(u))
    Time Complexity Analysis:
        - We scan only u node's outgoing list once to check for v.
    """
    for (neighbour, w) in adj[u]:
        if neighbour == v:
            return w
        
    return False

def bfs(adj, source):
    """BFS using adjacency list"""
    V = len(adj)
    visited = [False] * V
    
    queue = deque([source])
    visited[source] = True
    
    while queue:
        u = queue.popleft()
        
        for v, _ in adj[u]:
            if not visited[v]:
                visited[v] = True
                queue.append(v)
                
    return visited
            
def dfs(adj, source):
    """DFS using adjacency list"""
    V = len(adj)
    visited = [False] * V
    
    order = []
    stack = [source]
    
    while stack:
        u = stack.pop()
        
        if visited[u]:
            continue
        
        order.append(u)
        
        for v, _ in adj[u]:
            if not visited[v]:
                stack.append(v) 
    
    return order