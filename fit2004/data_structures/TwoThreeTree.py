from typing import Generic, List, Tuple, Optional, TypeVar

K = TypeVar('K')

class TwoThreeNode(Generic[K]):
    __slots__ = ('keys', 'children')
    def __init__(self, keys: List[K], children: Optional[List['TwoThreeNode[K]']] = None):
        self.keys: List[K] = keys
        self.children: Optional[List['TwoThreeNode[K]']] = children or []
        
    def is_leaf(self) -> bool:
        return not self.children
    

class TwoThreeTree(Generic[K]):
    def __init__(self):
        self.root: Optional[TwoThreeNode[K]] = None

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.inorder()})'
    __str__ = __repr__
    
    def search(self, key: K) -> str:
        """Return True if key is in the 2-3 tree"""
        node = self.root
        while node:
            # Direct match in this node?
            if key in node.keys:
                return True
            # If we're at a leaf and it's not here, we're done
            if node.is_leaf():
                return False
            # Choose the correct child to descend
            if len(node.keys) == 1:
                node = node.children[0] if key < node.keys[0] else node.children[1]
            # Two keys: [k0, k1]
            else:
                if key < node.keys[0]:
                    node = node.children[0]
                elif key > node.keys[1]:
                    node = node.children[2]
                else:
                    node = node.children[1]
        return False
    
    def insert(self, key: K) -> None:
        """Insert a key into the tree, splitting any 4-nodes on the way up"""
        if not self.root:
            self.root = TwoThreeNode([key])
            return
        
        result = self._insert(self.root, key)
        if result is not None:
            mid, right = result
            self.root = TwoThreeNode([mid], [self.root, right])
        
    def _insert(self, node: TwoThreeNode[K], key: K) -> Optional[Tuple[K, TwoThreeNode[K]]]:
        # 1) If key already here, do nothing
        if key in node.keys:
            return None
        
        # 2) If leaf: absorb or split
        if node.is_leaf():
            new_keys = sorted(node.keys + [key])
            if len(new_keys) <= 2:
                node.keys = new_keys
                return None
            # Split 3 -> 4 keys into 2-nodes + promote middle
            left_keys = [new_keys[0]]
            mid = new_keys[1]
            right_keys = [new_keys[2]]
            # Update this node to become the left piece
            node.keys = left_keys
            # Right sibling
            right_node = TwoThreeNode(right_keys)
            return (mid, right_node)
        
        # 3) Internal node: recurse into correct child
        if len(node.keys) == 1:
            idx = 0 if key < node.keys[0] else 1
        else:
            idx = (0 if key < node.keys[0]
                   else 2 if key > node.keys[1]
                   else 1)
        child = node.children[idx]
        result = self._insert(child, key)
        if result is None:
            return None
        
        # 4) Child split: integrate promoted key & new right child
        mid, new_right = result
        # Insert mid into this node's keys
        all_keys = sorted(node.keys + [mid])
        node.keys = all_keys
        # Insert new_right immediately after the child we split
        node.children.insert(idx + 1, new_right)
        
        # 5) If this node now has 3 keys -> split again
        if len(node.keys) == 3:
            # Split into left-node & right-node, promote middle
            left_keys = [node.keys[0]]
            promote = node.keys[1]
            right_keys = [node.keys[2]]
            
            # Children split: first two go left, last two go right
            left_children = node.children[:2]
            right_children = node.children[2:]
            
            # Update this node to be the left place
            node.keys = left_keys
            node.children = left_children
            
            # Create right sibling
            right_node = TwoThreeNode(right_keys, right_children)
            return (promote, right_node)
        
        return None
    
    def inorder(self) -> List[K]:
        """Return sorted list of all keys (in-order)"""
        output: List[K] = []
        def dfs(n: Optional[TwoThreeNode[K]]):
            if n is None:
                return
            if n.is_leaf():
                # Just output its keys
                output.extend(n.keys)
            else:
                if len(n.keys) == 1:
                    dfs(n.children[0])
                    output.append(n.keys[0])
                    dfs(n.children[1])
                else:
                    # Two keys: three children
                    dfs(n.children[0])
                    output.append(n.keys[0])
                    dfs(n.children[1])
                    output.append(n.keys[1])
                    dfs(n.children[2])
        dfs(self.root)
        return output
                    
        
if __name__ == '__main__':
    t23 = TwoThreeTree[int]()
    for x in [10,5,15,3,8,12,18,1,4]:
        t23.insert(x)
    print(t23) # e.g. TwoThreeNode([1,3,4,5,8,10,12,15,18])
    print(t23.search(12)) # True
    print(t23.search(7)) # False
        
        