"""
? 323. Number of Connected Components in an Undirected Graph

? Description
You have a graph of n nodes.
You are given an integer n and an array edges where edges[i] = [a_i, b_i]
indicates that there is an edge between a_i and b_i in the graph.

Return the number of connected components
"""
def count_connected_components(n: int, edges: list[list[int]]) -> int:
    """
    Count connected components using UnionFind
    """
    par = [i for i in range(n)]
    rank = [1] * n
    
    def find(n1):
        res = n1
        
        while res != par[res]:
            par[res] = par[par[res]]
            res = par[res]
            
        return res
    
    def union(n1, n2):
        p1, p2 = find(n1), find(n2)
        
        if p1 == p2:
            return 0
        
        if rank[p2] > rank[p1]:
            par[p1] = p2
            rank[p2] += rank[p1]
        else:
            par[p2] = p2
            rank[p1] += rank[p2]
            
        return 1
    
    # Everytime a union is made, decrement 
    res = n
    for n1, n2 in edges:
        res -= union(n1, n2)

if __name__ == '__main__':
    pass