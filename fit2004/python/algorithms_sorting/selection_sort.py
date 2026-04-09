from typing import List

def selection_sort(arr: List[int]) -> List:
    """
    In-Place Selection Sort
    
    Repeatedly selects the smallest element from the unsorted portion 
    and swaps it into its correct position.
    
    Returns the same list sorted in ascending order.
    
    Time Complexity: O(n^2) for best, average, and worst cases.
    Space Complexity: O(1)
    """
    n = len(arr)
    
    for i in range(n):
        # (1) Assume the smallest element in arr[1..n-1] is at index i
        min = i
        
        # (2) Find the actual index of the smallest element in arr[i..n-1]
        for j in range(i + 1, n):
            if arr[j] < arr[min]:
                min = j
        
        # (3) Swap arr[i] with arr[min] 
        arr[i], arr[min] = arr[min], arr[i]
        
    return arr

if __name__ == '__main__':
    arr = [3,2,5,3,1]
    res = selection_sort(arr)
    exp = sorted(arr)
    assert res == exp, f'Expected {exp}, got {res}'
    
    print('All tests passed!')