from typing import List, Tuple

class UnionFind:
    """
    Disjoint Set Union (Union-Find)
    
    Maintains a collection of disjoint sets over elements 0..n-1.
    
    Operations:
        - find(x) -> int:
            Returns the representative (root) of the set containing x.
        
        - union(x, y) -> None:
            Merges the sets containing x and y by linking x's root to y's root.
            
    This is a basic implementation without path compression or union by rank.
    It is commonly used for connectivity queries and Kruskal's MST algorithm.
    """
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        
    def find(self, x):
        if self.parent[x] == x: 
            return x
        
        return self.find(self.parent[x])
    
    def union(self, x, y):
        self.parent[self.find(x)] = self.find(y)
        

if __name__ == '__main__':
    uf = UnionFind(5)
    # Initially, each element is its own representative
    for i in range(5):
        assert uf.find(i) == i
        
    # Union some pairs
    uf.union(0,1)
    uf.union(1,2)
    uf.union(3,4)
    
    # Check connected components
    assert uf.find(0) == uf.find(2), "0,1,2 should be in the same set"
    assert uf.find(3) == uf.find(4), "3 & 4 should be in the same set"
    
    # Check different components remain distinct
    assert uf.find(0) != uf.find(3), "Set {0,1,2} and {3,4} should be separate"
    
    print("All UnionFind tests passed")