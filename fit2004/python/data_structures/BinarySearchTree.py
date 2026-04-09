from typing import List, Optional, TypeVar, Generic

K = TypeVar('K')

class BSTNode(Generic[K]):
    __slots__ = ('key', 'left', 'right')
    def __init__(self, key: int):
        self.key: int = key
        self.left: Optional[BSTNode] = None
        self.right: Optional[BSTNode] = None

class BinarySearchTree(Generic[K]):
    def __init__(self):
        self.root: Optional[BSTNode[K]] = None
        
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.inorder()})'
    __str__ = __repr__
    
    def insert(self, key: K) -> None:
        """Insert key into the BST."""
        self.root = self._insert(self.root, key)
            
    def _insert(self, node: Optional[BSTNode[K]], key: K) -> BSTNode[K]:
        if node is None:
            return BSTNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
            
        return node
    
    def search(self, key: int) -> bool:
        node = self.root
        while node:
            if key == node.key:
                return True

            node = node.left if key < node.key else node.right
            
        return False
    
    def inorder(self) -> List[K]:
        res: List[K] = []
        
        def dfs(n: Optional[BSTNode[K]]):
            if not n: return
            dfs(n.left)
            res.append(n.key)
            dfs(n.right)
            
        dfs(self.root)
        
        return res
        
if __name__ == '__main__':
    bst = BinarySearchTree[int]()
    for x in [10,5,15,3,8]:
        bst.insert(x)
    print(bst)