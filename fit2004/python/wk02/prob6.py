from typing import List, Tuple

def count_inversions(arr: list) -> int:
    '''
    Counts the number of inversions in an array.
    
    This is the exhaustive method, using two for loops to check all inversions.
    
    Time Complexity: O(n^2)
    Space Complexity: O(1)
    '''
    count = 0
    
    for i in range(len(arr)):
        for j in range(len(arr)):
            if i < j and arr[i] > arr[j]:
                count += 1
            
    return count

def better_count_inversions(arr: List) -> Tuple[List, int]:
    '''
    Counts the number of inversions in an array (divide and conquer)
    
    Time Complexity: O(nlogn)
    Space Complexity: O(n)
    '''
    
    # MERGE FUNCTION
    def merge(left: List, right: List) -> Tuple[List, int]:
        '''
        Merges two sorted arrays and counts the split inversions.
        
        Returns the merged array and the count of split inversions
        
        Time Complexity: O(n)
        Space Complexity: O(n)
        '''
        merged = []
        i, j = 0, 0
        count = 0
        
        print(f'left array: {left}')
        print(f'right array: {right}')
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            elif left[i] > right[j]:
                merged.append(right[j])
                count += len(left) - i
                j += 1
                
        merged.extend(left[i:])
        merged.extend(right[j:])
                
        print(f'merged arrays: {merged}')
        print(f'checked count: {count}')
        return merged, count
    
    # Base cases
    if len(arr) <= 0:
        return [], 0
    if len(arr) == 1:
        return arr, 0
    
    # Calculate midpoint
    mid = len(arr) // 2
    
    # Partition left and right
    left, count_left = better_count_inversions(arr[:mid])
    right, count_right = better_count_inversions(arr[mid:])
    
    # Merge left and right
    merged, split_count = merge(left, right)
    
    # Calculate total count
    total_count = count_left + count_right + split_count
    
    # Return merged array and total count
    return merged, total_count
    
     
if __name__ == '__main__':
    test = [1, 20, 6, 7, 5, 8, 11, 3]
    sorted_arr, inversions = better_count_inversions(test)
    print(f'Original array: {test}')
    print(f'Sorted array: {sorted_arr}')
    print(f'No. of inversions: {inversions}')
    
    # Verify with exhaustive method
    print(f'Verification with exhaustive method: {count_inversions(test)}')