def find_first_occur_idx_target(arr: list, target: int) -> int:
    """
    Find First Occurrence Index of Target (bad solution)
    
    This function implements a modified binary search. It first uses binary
    search to locate an index where the element equals the target. Once found,
    it performs a linear scan backwards from that index to find the earliest
    (first) index where the element is still equal to the target.
    
    Args:
        - arr: A list of integers sorted in increasing order.
        - target: The integer value to search for
    
    Returns:
        The index of the first occurrence of the target in the array,
        or -1 if the target is not found.
        
    Time Complexity:
        - Best case: O(log n)
        If the first element found by binary search is the actual first 
        occurrence.
        
        - Worst case: O(n)
        If the target element occupies a large portion of the array, requiring
        a longer linear scan backwards.

        - Average case: O(log n)
        
    Space Complexity (aux): O(1)
    """
    lo = 0
    hi = len(arr)-1
    
    while lo <= hi:
        mid = (lo + hi) // 2
        
        if arr[mid] == target:
            # Store index
            idx = mid
            
            # Linear scan backwards checking for more targets in LHS
            i = 1
            while mid-i >= 0 and arr[mid-i] == target:
                idx = mid - i
                i += 1
            
            # Return index
            return idx
        
        elif arr[mid] > target:
            hi = mid - 1
        
        elif arr[mid] < target:
            lo = mid + 1
            
    return -1

def find_first_occur_idx_target(arr: list, target: int) -> int:
    """
    Find First Occurrence Index of Target (optimal solution)
    
    Implements modified binary search that finds the first occurrence of the 
    target's index. This is done when we find a value that matches our target,
    we save that potential index but we keep searching the LHS of the array for
    more of the same target.
    
    Time Complexity: O(log n)
    Space Complexity (aux): O(1)
    """
    lo = 0
    hi = len(arr)-1
    potential_index = -1
    
    while lo <= hi:
        mid = (lo + hi) // 2
        
        if arr[mid] == target:
            # Store potential target
            potential_index = mid
            
            # Keep searching LHS for more targets
            hi = mid - 1

        elif arr[mid] > target:
            hi = mid - 1
            
        elif arr[mid] < target:
            lo = mid + 1
            
    return potential_index

if __name__ == '__main__':
    # Test 1: Target is earlier in the array
    arr = [2,5,5,5,8,12,12,16]
    target = 5
    idx = find_first_occur_idx_target(arr, target)
    assert idx == 1, f'Test failed, got {idx}, should be 1'
    print('Test case 1 passed!')
    
    # Test 2: Target is later in the array
    arr = [1,1,1,2,3,4,4,5]
    target = 4
    idx = find_first_occur_idx_target(arr, target)
    assert idx == 5, f'Test failed, got {idx}, should be 5'
    print('Test case 2 passed!')
    
    # Test 3: Target not present
    arr = [10,20,30,40,50]
    target = 25
    idx = find_first_occur_idx_target(arr, target)
    assert idx == -1, f'Test failed, got {idx}, should be -1'
    print('Test case 3 passed!')
    
    # Test 4: All targets array
    arr = [7,7,7,7,7]
    target = 7
    idx = find_first_occur_idx_target(arr, target)
    assert idx == 0, f'Test failed, got {idx}, should be 0'
    print('Test case 4 passed!')