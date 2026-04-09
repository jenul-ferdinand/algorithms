

def binary_search(arr: list, low: int, high: int, target: int) -> int:
    """
    Binary Search (recursive)
    
    Time Complexity: O(log n)
    Space Complexity (auxiliary): O(log n)
    """
    if high < low: 
        return -1
    
    mid = (high + low) // 2
    
    if arr[mid] == target:
        return mid
    
    elif arr[mid] > target:
        return binary_search(arr, low, mid-1, target)
    
    elif arr[mid] < target:
        return binary_search(arr, mid+1, high, target)



def binary_search_iterative(arr: list, target: int) -> int:
    """
    Binary Search (iterative)
    
    Time Complexity: O(log n)
    Space Complexity (auxiliary): O(1)
    """
    low = 0
    high = len(arr)-1
    mid = 0
    
    while low <= high:
        #! LI: target is in arr[1..n] iff target is in arr[low..high]
        
        mid = (high + low) // 2 
        
        if arr[mid] < target:
            low = mid + 1
        elif arr[mid] > target:
            high = mid - 1
        else:
            return mid
    
    return -1



if __name__ == '__main__':
    # Test case 1: Target present in the array
    arr = [2,5,8,12,16,23,38,56,72,91]
    target = 23
    low = 0
    high = len(arr)-1
    result_idx = binary_search(arr, low, high, target)
    
    print(f'Array: {arr}')
    print(f'Target: {target}')
    if result_idx != -1:
        print(f'Target found at index: {result_idx}')
        assert arr[result_idx] == target, "Test failed: Incorrect index returned!"
    else:
        print("Target not found in the array")
    