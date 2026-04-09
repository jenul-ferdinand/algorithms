import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms_sorting.merge_sort import merge

'''
Design an algorithm for merging k sorted lists of total size n that runs in O(nk) time or better
'''

# ! Merge K sorted lists
def merge_k_lists(arrays: list[list]) -> list:
    '''
    Merges K Arrays
    
    Time Complexity: O(n log k) 
        - where n is the total number of elements 
        - k is the number of arrays
    Space Complexity: O(n)
    '''
    if not arrays:
        return []
    
    _arrays = arrays.copy()
    
    while len(_arrays) > 1:
        merged_arrays = []
        
        for i in range(0, len(_arrays), 2):
            if i+1 < len(_arrays):
                # Merge pair and add to results
                merged = merge(_arrays[i], _arrays[i+1])
                merged_arrays.append(merged)
            else: 
                # Odd number of arrays, add the last on as is
                merged_arrays.append(_arrays[i])
        
        _arrays = merged_arrays
        
    return _arrays[0] if _arrays else []



if __name__ == '__main__':
    arrays = [
        [4,5,6],
        [1,2,3],
        [7,8,9],
        [5,4,3]
    ]
    
    print(merge_k_lists(arrays))