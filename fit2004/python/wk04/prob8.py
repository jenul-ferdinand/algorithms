"""
Prob 8) Write a version of QuickSelect that is iterative rather than recursive.
"""
from typing import List
import random
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithms_sorting.quick_select import naive_partition

def quick_select(arr: List[int], k: int) -> int:
    N = len(arr)
    
    lo = 0
    hi = N-1
    
    while lo < hi:
        pivot = random.randint(lo, hi)
        mid = naive_partition(arr, lo, hi, pivot)
        
        if k < mid:
            lo = lo
            hi = mid-1
        
        elif k > mid:
            lo = mid+1
            hi = hi
            
        elif k == mid:
            return arr[mid]
        
    return arr[lo]

if __name__ == '__main__':
    # Simple test for smallest value
    arr = [10,9,8,7,6,5,4,3,2,1]
    k = 1
    res = quick_select(arr[:], k-1)
    exp = 1
    assert res == exp, f'Expected {exp}, got {res}'
    
    # Test iterative quick select on multiple k values
    arr = [9,3,1,4,7,2,8,5,6]
    for k in range(1, len(arr)+1):
        res = quick_select(arr[:], k-1)
        exp = sorted(arr)[k-1]
        assert res == exp, f'k={k-1}: Expected {exp}, got {res}'
        
    print('All iterative quick select tests passed!')