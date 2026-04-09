from typing import List
import random

#! =============================================================================|
#! Quick Select Algorithm
#! =============================================================================|

def quick_select(array: List, lo: int, hi: int, k: int) -> float | int | str:
    """
    Quick Select (finds k-th smallest element in array)
    
    Description: 
        Similar to QuickSort, it selects a pivot and partitions the array, but 
        only recurses into one partition instead of both, giving average O(n) 
        time complexity.
    
    Args:
        array: The input array to search in
        lo: The lower index of the current subarray
        hi: The upper index of the current subarray
        k: The index of the element if the array were to be sorted (0-based)
    
    Returns:
        The k-th smallest element in the array
        
    Average Case Time Complexity: O(n)
    Worst Case Time Complexity: O(n^2)
    Time Complexity Analysis:
        1. Partitioning around pivot takes O(n) work.
        2. Average case recurrence: T(n) = T(n/2) + O(n) = O(n).
        3. Worst case recurrence: T(n) = T(n-1) + O(n) = O(n^2). This occurs 
           when bad pivot choices are made consistently.

    Space Complexity: O(log n) 
    Space Complexity Analysis: 
        - Average: balanced splits give recursion depth of approx O(log n).
        - Worst: unbalanced splits give recursion depth of approx O(n). 
    """
    if hi <= lo:
        return array[k]
    
    pivot_idx = random.randint(lo, hi)
    mid = naive_partition(array, lo, hi, pivot_idx)
    
    if k < mid: return quick_select(array, lo, mid-1, k)
    if k > mid: return quick_select(array, mid+1, hi, k)
    if k == mid: return array[k]
        


#? =============================================================================|
#? Naive Partitioning Algorithm (Lomuto)
#? =============================================================================|

def naive_partition(array: List, lo: int, hi: int, pivot_index: int = None) -> int:
    """
    Naive partitioning shceme (Lomuto)
    
    Approach Description:
        1. Choose a pivot index randomly between lo and hi if none given 
        2. Move the pivot element to the end of the subarray by swapping
        3. Let `j = lo`. This marks the boundary of elements <= pivot.
        4. For each `i` in `[lo..hi-1]`
            if `array[i] <= pivot`:
                swap `array[i]` with `array[j]`
                increment j by one
        5. Finally, swap the pivot (now at `hi`) with `array[j]`.
           The pivot is now at its correct sorted position.
        6. Return `j` as the pivot's final index.
    
    Time Complexity: O(n)
    Time Complexity Analysis:
        Each element in arr[lo..hi-1] is compared to the pivot exactly once,
        and at most one swap per comparison. Hence O(n) time where 
        n = hi - lo + 1.
    
    Space Complexity: O(1)
    Space Complexity Analysis:
        In-place partitioning uses O(1) extra space beyond input array.
    """
    if pivot_index is None: 
        pivot_index = random.randint(lo, hi)
        
    # Move the pivot to the end 
    if pivot_index != hi:
        array[pivot_index], array[hi] = array[hi], array[pivot_index]
        
    pivot = array[hi]
    j = lo
    
    for i in range(lo, hi):
        if array[i] <= pivot:
            array[i], array[j] = array[j], array[i]
            j = j + 1
    
    array[hi], array[j] = array[j], array[hi]
    
    return j



#? =============================================================================|
#? Testing
#? =============================================================================|

if __name__ == '__main__':
    # Test 1: Simple sorted array
    nums = [1, 2, 3, 4, 5]
    for i in range(len(nums)):
        result = quick_select(nums, 0, len(nums)-1, i)
        assert result == nums[i], f"Expected {nums[i]}, got {result}"
    
    # Test 2: Unsorted array
    nums = [3, 1, 4, 5, 2]
    n = len(nums)
    exp = sorted(nums) # Expected sorted order: [1, 2, 3, 4, 5]
    for i in range(n):
        result = quick_select(nums, 0, n-1, i)
        assert result == exp[i], f"Expected {exp[i]}, got {result}"
    
    # Test 3: Array with duplicates
    nums = [3, 3, 1, 2, 2, 5]
    n = len(nums)
    exp = sorted(nums) # Expected sorted order: [1, 2, 2, 3, 3, 5]
    for i in range(n):
        result = quick_select(nums, 0, n-1, i)
        assert result == exp[i], f"Expected {exp[i]}, got {result}"
    
    # Test 4: Single element array
    nums = [42]
    assert quick_select(nums, 0, 0, 0) == 42
    
    print("All tests passed!")