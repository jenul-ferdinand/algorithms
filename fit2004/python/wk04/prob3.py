"""
Prob 3) Devise an algorithm that given a sequence of n integers and some integer
1 <= k <= n, finds the k closest numbers to the median of the sequence. Your 
algorithm should run in O(n) time. You may assume that QuickSelect runs in 
O(n) time (achievable using median of medians to find a good pivot).
"""
from typing import List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithms_sorting.quick_select import quick_select

def k_closest_to_median(arr: List[int], k: int) -> List[int]:
    """
    Finds k closest numers to median in input array
    
    1. Find the median in O(n) time
    2. Measure absolute distance to the median
    3. Select the kth smallest distance in O(n)
    4. Collect answer in one pass
    
    Time Complexity: O(n)
    Aux Space Complexity: O(n)
    """
    N = len(arr)
    
    # Find the median
    median = quick_select(arr[:], 0, N-1, N//2)
    
    # Compute absolute differences
    diffs = [abs(x - median) for x in arr]
    
    # Find k-th smallest difference
    kth_diff = quick_select(diffs[:], 0, N-1, min(k-1, N-1))
    
    # Collect all with diff < kth_diff
    result = [x for x, d in zip(arr, diffs) if d < kth_diff]
    
    # Add those == kth_diff until we have k
    for x, d in zip(arr, diffs):
        if d == kth_diff and len(result) < k:
            result.append(x)
    
    return result
        

if __name__ == '__main__':
    arr = [7,3,1,2,5,4,6]
    k = 3
    res = k_closest_to_median(arr, k)
    exp = {3,4,5}
    assert set(res) == exp, f'Expected {exp},got {set(res)}'
    print(f'{k} closest to median in {arr}: {res}')