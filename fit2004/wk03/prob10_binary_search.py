"""
Write an iterative Python function that implements binary search on a sorted,
non-empty list, and returns the position of the key, or None if it doesn't 
exist.

(a) If there are multiple occurrences of the key, return the position of the
final one. Identify an useful invariant of your program and explain why
your algorithm is correct.

"""
from typing import List, Optional

def binary_search_last(arr: List[int], target) -> Optional[int]:
    """
    Return the index of the last occurrence of target in sorted arr.
    Or None if not found.
    """
    n = len(arr)
    lo = 0
    hi = n-1
    
    while (lo < hi):
        mid = (lo + hi+1) // 2
        
        if arr[mid] > target:
            hi = mid + 1
        if arr[mid] <= target:
            lo = mid

    if arr[lo] == target:
        return lo
    
    return None

def binary_search_first(arr: List[int], target: int) -> Optional[int]:
    """
    Return the index of the first occurrence of target in sorted arr.
    Or None if not found.
    """
    n = len(arr)
    lo = 0
    hi = n - 1
    
    while (lo < hi):
        mid = (lo + hi) // 2 
        
        if arr[mid] < target:
            lo = mid + 1
        if arr[mid] >= target:
            hi = mid
    
    if arr[lo] == target:
        return lo
        
    return None
            

if __name__ == '__main__':
    arr = [1,2,3,4,5,6,6]
    res = binary_search_last(arr, target=6)
    exp = 6
    assert res == exp, f'Expected position {exp}, got {res}'
    
    res = binary_search_first(arr, target=6)
    exp = 5
    assert res == exp, f'Expected position {exp}, got {res}'
    
    print('All tests passed!')