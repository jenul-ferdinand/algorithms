from typing import Generic, TypeVar, List, Tuple, Optional

K = TypeVar('K')

RED = True
BLACK = False

class RBNode(Generic[K]):
    __slots__ = ('key', 'left', 'right', 'color')
    def __init__(self, key: K, color: bool = RED):
        self.key: K = key
        self.left: Optional['RBNode[K]'] = None
        self.right: Optional['RBNode[K]'] = None
        self.color: bool = color # True=RED, False=Black
    
def _is_red(node: Optional[RBNode[K]]) -> bool:
    return bool(node and node.color == RED)

def _rotate_left(h: RBNode[K]) -> RBNode[K]:
    # Condition 1: right-leaning red link -> rotate left
    x = h.right; assert x is not None
    h.right = x.left
    x.left = h
    x.color = h.color
    h.color = RED
    return x

def _rotate_right(h: RBNode[K]) -> RBNode[K]:
    # Condition 2: two left-leaning reds in a row -> rotate right
    x = h.left; assert x is not None
    h.left = x.right
    x.right = h
    x.color = h.color
    h.color = RED
    return x

def _flip_colors(h: RBNode[K]) -> None:
    # Condition 3: Both children red -> flip colors
    h.color = RED
    if h.left: h.left.color = BLACK
    if h.right: h.right.color = BLACK

class RedBlackTree(Generic[K]):
    def __init__(self):
        self.root: Optional[RBNode[K]] = None
        
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.inorder()})'
    __str__ = __repr__
    
    def search(self, key: K) -> bool:
        """Standard BST search (ignore colours)"""
        node = self.root
        while node:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False
    
    def insert(self, key: K) -> None:
        """Insert key, then ensure root is always black."""
        self.root = self._insert(self.root, key)
        if self.root:
            self.root.color = BLACK
            
    def _insert(self, h: Optional[RBNode[K]], key: K) -> RBNode[K]:
        if h is None:
            # New node is always red (preserves black-height)
            return RBNode(key, RED)
        
        if key < h.key:
            h.left = self._insert(h.left, key)
        elif key > h.key:
            h.right = self._insert(h.right, key)
        else:
            # Duplicate, do nothing
            pass

        # Fixup (Conditions 1-3)
        # 1) Right-leaning and red link -> rotate left
        if _is_red(h.right) and not _is_red(h.left):
            h = _rotate_left(h)
        # 2) Two left-leaning reds in a row -> rotate right
        if _is_red(h.left) and _is_red(h.left.left):
            h = _rotate_right(h)
        # 3) both children red -> flip colours
        if _is_red(h.left) and _is_red(h.right):
            _flip_colors(h)
            
        return h
    
    def inorder(self) -> List[K]:
        """In-order traversal of keys"""
        out: List[K] = []
        def dfs(n: Optional[RBNode[K]]):
            if not n:
                return
            dfs(n.left)
            out.append(n.key)
            dfs(n.right)
        dfs(self.root)
        return out
    
if __name__ == '__main__':
    rbt = RedBlackTree[int]()
    for x in [10,5,15,1,7,12,18]:
        rbt.insert(x)
    print(rbt) # RedBlackTree([1,5,7,10,12,15,18])
    print(rbt.search(7)) # True
    print(rbt.search(8)) # False
            
