"""
You are given the keys x1, x2, x3, ... xn.

a) Design an algorithm that creates a binary search tree of minimal height
in O(n log n) time.

- First we sort the input keys
- Then we use the divide and conquer approach to insert median keys in the 
    sorted array.

b) Prove that your algorithm produces a BST of height at most log(n)

The height is <= log(n) because:
- If at each recursive step we split the array as evenly as possible.

h(n) = height of the tree we build on n keys

Base:
h(0) = 0

Reccurrence for n >= 1:
h(n) = 1 + max(h(n-1)/2), h(n-1)/2) <= 1 + h(n/2)
h(n) <= 1 + h(n/2)
h(1) = 1

h(n) <= 1 + 1 + h(n/4)
     <= 2 + 1 + h(n/8)
     <= logn + 1 = O(logn)

c) Prove that the fastest algorithm for this problem in the comparison-based
model has time complexity Θ(n log n).

Θ(nlogn) is optimal in the comparison model:
- Since producing a minimal height BST requires knowing the order of the keys.
Sorting is required. And sorting is O(nlogn) 
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures.BinarySearchTree import BinarySearchTree

def create_bst(keys: list[int]):
    """
    Creates a BST of minimal height in O(n log n time).
    
    This uses the divide and conquer approach to keep inserting the median 
    element so that our BST.
    
    """
    def build(arr: list[int]):
        """Divide and conquer inserting median keys"""
        if not arr:
            return
        
        mid = len(arr) // 2
        bst.insert(arr[mid])
        
        build(arr[:mid]) # Left half
        build(arr[mid + 1:]) # Right half
    
    # Empty BST
    bst = BinarySearchTree[int]()
    
    # Sort the keys first
    sorted_keys = sorted(keys) 
    
    # Use the build helper to recursively insert median keys
    build(sorted_keys)
        
    return bst
    

if __name__ == '__main__':
    tree = create_bst([54, 3, 100, 30])
    print(tree)