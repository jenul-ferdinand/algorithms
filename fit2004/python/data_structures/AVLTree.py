from typing import List, Tuple, Generic, TypeVar, List, Optional

K = TypeVar('K')

class AVLNode(Generic[K]):
    __slots__ = ('key', 'left', 'right', 'height')
    def __init__(self, key):
        self.key: K = key
        self.left: Optional[AVLNode[K]] = None
        self.right: Optional[AVLNode[K]] = None
        self.height: int = 1

class AVLTree(Generic[K]):
    def __init__(self):
        self.root: Optional[AVLNode[K]] = None
        
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.inorder()})'
    __str__ = __repr__

    def insert(self, key: K) -> None:
        self.root = self._insert(self.root, key)
    
    def delete(self, key: K) -> None:
        self.root = self._insert(self.root, key)
        
    def search(self, key: K) -> bool:
        node = self.root
        while node:
            if key == node.key: return True
            node = node.left if key < node.key else node.right
        return False
    
    def inorder(self) -> List[K]:
        res: List[K] = []
        def dfs(n: Optional[AVLNode[K]]):
            if not n: return
            dfs(n.left)
            res.append(n.key)
            dfs(n.right)
        
        dfs(self.root)
        return res
    
    def _height(self, n: Optional[AVLNode[K]]) -> int:
        return n.height if n else 0
    
    def _balance(self, n: Optional[AVLNode[K]]) -> int:
        return (self._height(n.left) - self._height(n.right)) if n else 0
    
    def _rotate_left(self, z: AVLNode[K]) -> AVLNode[K]:
        y, T2 = z.right, z.right.left # type: ignore
        y.left, z.right = z, T2
        
        z.height = 1 + max(self._height(z.left), self._height(z.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        
        return y
    
    def _rotate_right(self, z: AVLNode[K]) -> AVLNode[K]:
        y, T3 = z.left, z.left.right
        z.right, z.left = z, T3 
        
        z.height = 1 + max(self._height(z.left), self._height(z.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        
        return y
    
    def _rebalance(self, n: AVLNode[K], key: K) -> AVLNode[K]:
        bal = self._balance(n)
        # LL
        if bal > 1 and key < n.left.key: return self._rotate_right(n)
        # RR
        if bal < -1 and key > n.right.key: return self._rotate_left(n)
        # LR
        if bal > 1 and key > n.left.key:
            n.left = self._rotate_left(n.left)
            return self._rotate_right(n)
        # RL
        if bal < -1 and key < n.right.key:
            n.right = self._rotate_right(n.right)
            return self._rotate_left(n)
        
        return n
    
    def _insert(self, node: Optional[AVLNode[K]], key: K) -> AVLNode[K]:
        if not node:
            return AVLNode(key)
        
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node
        
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        return self._rebalance(node, key)
        

if __name__ == '__main__':
    avl = AVLTree[int]()
    for x in [10,5,15,3,8]:
        avl.insert(x)
    print(avl)